#!/usr/bin/env python

import pprint
import httplib2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run

from apiclient.discovery import build

import re

CLIENT_SECRETS = 'client_secrets.json'
OAUTH2_STORAGE = 'oauth2.dat'
GCE_SCOPE = 'https://www.googleapis.com/auth/admin.directory.group'
PROJECT_ID = 'nexr.com:nexr-infra'
API_VERSION = 'v1'
# GCE_URL = 'https://www.googleapis.com/admin/directory/%s/groups/' % (API_VERSION)
GCE_URL = 'https://www.googleapis.com/admin/'
# DEFAULT_ZONE = 'us-central1-a'

def main():
  # Perform OAuth 2.0 authorization.
  flow = flow_from_clientsecrets(CLIENT_SECRETS, scope=GCE_SCOPE)
  storage = Storage(OAUTH2_STORAGE)
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run(flow, storage)
  http = httplib2.Http()
  auth_http = credentials.authorize(http)

  # Build the service
  gce_service = build('admin', 'directory_v1')
  # pprint.pprint(dir(gce_service))
  project_url = '%s%s' % (GCE_URL, PROJECT_ID)
  request = gce_service.groups().list(domain="nexr.com")
  response = request.execute(auth_http)
  # pprint.pprint(response)
  # keys=[u'kind', u'description', u'adminCreated', u'email', u'id', u'name']
  # u'kind': u'admin#directory#group', u'description': u'ZooKeeper Client \uad00\ub828', u'adminCreated': True, u'email': u'zkclient@nexr.com', u'id': u'023ckvvd3wb8nnj', u'name': u'zkclient'}
  if response and 'groups' in response:
    ggroups = response['groups']
    for ggroup in ggroups:
      # print ggroup
      # pprint.pprint(ggroup.keys())
      print "%s\t%s\t%s\t%s" % (ggroup['email'], ggroup['name'], re.sub("[\n\r]", " ", ggroup['description']), ggroup['adminCreated'])
      # break
  else:
    print 'No groups to list.'

if __name__ == '__main__':
  main()
