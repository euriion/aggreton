# -*- coding: utf8 -*-
import json

__author__ = 'euriion'

import sys
import os

# ndash_home = os.environ["NDASH_HOME"]
ndash_home = "/Users/euriion/Documents/workspace/nexr-infra/Ndash"
sys.path.append("%s/modules" % ndash_home)
sys.path.append("%s/models" % ndash_home)

timestamp_filename = "%s/data/kt_users/last_timestamp.dat" % ndash_home
last_timestamp = open(timestamp_filename).read().strip()
tree_filename = "%s/data/kt_users/kt_org_tree.%s.json" % (ndash_home, last_timestamp)
org_filename = "%s/data/kt_users/kt_orgs.%s.json" % (ndash_home, last_timestamp)
tree = json.loads(open(tree_filename).read())
orgs = json.loads(open(org_filename).read())

orgs_index = {}
idx = 0
for org in orgs:
    org_id =  org[0]
    # org_name org[1]
    if not orgs_index.has_key(org_id):
        orgs_index[org_id] = idx
    idx += 1
new_tree = {}
def convert_tree(id, old_parent_tree):
    custom_tree = {}
    if id == 'KTGROUP':
        custom_tree['name'] = 'KT그룹'
    else:
        custom_tree['name'] = orgs[orgs_index[id]][1].encode('utf8')
    custom_tree['size'] = 1
    if len(old_parent_tree[id].keys()) > 0:
        custom_tree['_children'] = []
        for child_id in sorted(old_parent_tree[id].keys()):
            custom_tree['_children'].append(convert_tree(child_id, old_parent_tree[id]))
    return custom_tree

whole_tree = convert_tree('KTGROUP', tree)
json_content = json.dumps(whole_tree, indent=2, ensure_ascii=False)
open("./tree_new.json", "w").write(json_content + "\n")