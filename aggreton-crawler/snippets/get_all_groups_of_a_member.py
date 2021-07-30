
import gdata.apps.groups.client

email="aiden.hong@nexr.com"
password="euro2048"
domain="nexr.com"

groupClient = gdata.apps.groups.client.GroupsProvisioningClient(domain)
print(groupClient)
groupClient.ClientLogin(email=email, password=password, source='apps')
for group in groupClient.RetrieveAllGroups():
  print group

jT3xrvtdb 