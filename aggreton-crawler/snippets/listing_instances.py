#!/usr/bin/env python

import pprint
import httplib2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run

from apiclient.discovery import build

CLIENT_SECRETS = 'client_secrets.json'
OAUTH2_STORAGE = 'oauth2.dat'
GCE_SCOPE = 'https://www.googleapis.com/auth/admin.directory.group'
PROJECT_ID = 'nexr.com:nexr-infra'
API_VERSION = 'v1'
GCE_URL = 'https://www.googleapis.com/admin/directory/%s/groups/' % (API_VERSION)
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

  # List instances
  request = gce_service.instances().list(project=PROJECT_ID, filter=None, zone=DEFAULT_ZONE)
  request = gce_service.instances().list(project=PROJECT_ID, filter=None)
  response = request.execute(auth_http)
  if response and 'items' in response:
    instances = response['items']
    for instance in instances:
      print instance['name']
  else:
    print 'No instances to list.'

if __name__ == '__main__':
  main()

