# -*- coding: utf-8 -*-
import pprint

__author__ = 'aiden.hong'


import json
import urllib

a = r"""
[-44,
16,
15,
14,
13,
52,
51,
47,
50,
1,
-42,
29,
0,
-2,
49,
1,
0,
0,
-52,
-70,
-51,
0,
-58,
0,
0,
1,
0,
0,
0,
16,
0,
0,
1,
23,
-46,
0,
0,
0,
0,
0,
48,
47,
1,
0,
47,
46,
45,
21,
0,
'Twrowxa',
25,
44,
41
]
"""

aa = eval(a)
pprint.pprint(aa)
# a = a.replace('//OK[', '[')
# a = a.decode('utf-8')
#print json.loads(a)
# a = urllib.unquote(a)
# b = a.decode("utf-8")
# json.loads(a)
# print json.loads('[1,[1,2,"\x3Dsadfsdafasdf"]]')