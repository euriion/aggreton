import pprint
import gflags
import httplib2

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

FLAGS = gflags.FLAGS

# Set up a Flow object to be used if we need to authenticate. This
# sample uses OAuth 2.0, and we set up the OAuth2WebServerFlow with
# the information it needs to authenticate. Note that it is called
# the Web Server Flow, but it can also handle the flow for native
# applications
# The client_id and client_secret are copied from the API Access tab on
# the Google APIs Console

# https://developers.googleapps.com/admin-sdk/directory/v1/guides/authorizing

FLOW = OAuth2WebServerFlow(
    client_id='182451245744.apps.googleusercontent.com',
    client_secret='bTcBbw2hz_JNKJFzL3_bBcQ_',
    scope='https://www.googleapis.com/auth/admin.directory.group',
    user_agent='nexr-infra/1.0',
    access_type="offline")

# To disable the local server feature, uncomment the following line:
# FLAGS.auth_local_webserver = False
print "making FLOW is done"
# If the Credentials don't exist or are invalid, run through the native client
# flow. The Storage object will ensure that if successful the good
# Credentials will get written back to a file.
storage = Storage('groups-settings.dat')
credentials = storage.get()
if credentials is None or credentials.invalid == True:
  print "Can not find credentials from storage. you need to get the data"
  credentials = run(FLOW, storage)

# Create an httplib2.Http object to handle our HTTP requests and authorize it
# with our good Credentials.
http = httplib2.Http()
http = credentials.authorize(http)

# Build a service object for interacting with the API. Visit
# the Google APIs Console
# to get a developerKey for your own application.
service = build(serviceName='groupssettings', version='v1', http=http)


