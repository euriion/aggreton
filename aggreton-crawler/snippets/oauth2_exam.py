from oauth2client.client import OAuth2WebServerFlow

flow = OAuth2WebServerFlow(client_id='182451245744.apps.googleusercontent.com',
                           client_secret='bTcBbw2hz_JNKJFzL3_bBcQ_',
                           scope='https://www.googleapis.com/auth/calendar',
                           redirect_uri='urn:ietf:wg:oauth:2.0:oob')
#
#
# from oauth2client.client import flow_from_clientsecrets
# # flow = flow_from_clientsecrets('./client_secrets.json',
# #                                scope='https://www.googleapis.com/auth/calendar',
# #                                redirect_uri='urn:ietf:wg:oauth:2.0:oob')
#
# auth_uri = flow.step1_get_authorize_url()
# print "auth_uri: %s" % auth_uri
#
# import sys
# sys.exit(1)

# code = "4/C0Vp1ebAJ19A6_oLe-g6cj3TSHA6.YmWNBmV0TiQTgrKXntQAax3EMOUVgAI"
# credentials = flow.step2_exchange(code)
# print "credentials: %s" % credentials

from oauth2client.file import Storage
storage = Storage('./credentials')
# storage.put(credentials)
credentials = storage.get()

import httplib2
http = httplib2.Http()
http = credentials.authorize(http)

from apiclient.discovery import build
service = build('calendar', 'v3', http=http)
print service.