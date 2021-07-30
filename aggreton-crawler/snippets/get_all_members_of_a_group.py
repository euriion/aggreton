import sys
import urllib
import oauth
import gdata.apps.groups.client
# http://stackoverflow.com/questions/15075919/gdata-python-googleapps-apps-authentication
# https://developers.googleapps.com/gdata/docs/auth/oauth#AdditionalResources2LO
# http://gdatatips.blogspot.kr/search/label/oauth
import gdata.gauth

Client_id='nexr.com';
Client_secret='uDYUOdU6Y9dW96IxLMvgiuP-'
CONTACTS_URL = 'http://www.googleapps.com/m8/feeds/contacts/default/full'

request = oauth.OAuthRequest.from_consumer_and_token(  
   consumer, http_method='GET', http_url=CONTACTS_URL, parameters=params)  
request.sign_request(oauth.OAuthSignatureMethod_HMAC_SHA1(), consumer, None)  
  
# See patch @ http://code.googleapps.com/p/oauth/issues/detail?id=31
headers = request.to_header()  
  
client = gdata.contacts.service.ContactsService()  
  
# Query the user's contacts and print their name & email  
uri = '%s?%s' % (request.http_url, urllib.urlencode(params))  
feed = client.GetFeed(uri, extra_headers=headers, converter=gdata.contacts.ContactsFeedFromString)  

for entry in feed.entry:  
  print '%s, %s' % (entry.title.text, entry.email[0].address)  
sys.exit(0)


token = gdata.gauth.OAuth2Token(client_id=Client_id,client_secret=Client_secret,scope=Scope,user_agent=User_agent)
print token.generate_authorize_url(redirect_uri='urn:ietf:wg:oauth:2.0:oob')
code = raw_input('What is the verification code? ').strip()
token.get_access_token(code)
print "Refresh token\n"
print token.refresh_token
print "Access Token\n"
print token.access_token

# domain = "nexr.com"
# groupClient = gdata.apps.groups.client.GroupsProvisioningClient(domain=domain)
# email="aiden.hong@nexr.com"
# password="euro2048"
# groupClient.ClientLogin(email=email, password=password, source='apps')
# groupClient.RetrieveAllMembers(group_id)
