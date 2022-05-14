from O365 import Account

# MS Graph business account credentials
#AZURE_CLIENT_ID='22d78996-f2d0-47ca-9e1e-0049997c6090'
#AZURE_CLIENT_SECRET='Sr~8Q~ID3d3JZw_hYbrDTY3EhfzSzhu9bPGPYcPK'

# MS Graph personal + business account credentials
AZURE_CLIENT_ID='75d1c35d-7ab6-4668-ab3a-0dfe4a1f3ead'
AZURE_CLIENT_SECRET='6T_8Q~AfaYwKIK9BGb98apVT1x-rjN2LQ-jnTb2N'

#credentials = ('my_client_id', 'my_client_secret')
credentials = (AZURE_CLIENT_ID, AZURE_CLIENT_SECRET)

# the default protocol will be Microsoft Graph
# the default authentication method will be "on behalf of a user"

account = Account(credentials)
if account.authenticate(scopes=['basic', 'message_all', 'calendar_all']):
   print('Authenticated!')

user = account.get_current_user()

print("User full name: " + user.full_name)
print("\n")
##print("User profile photo: " + user.get_profile_photo())
#print("\n")
print("User display name: " + user.display_name )
print("\n")
print("User given name: " +  user.given_name)
print("\n")
print("User surname: " + user.surname)
print("\n")
print("User principal name: " + user.user_principal_name)
# 'basic' adds: 'offline_access' and 'https://graph.microsoft.com/User.Read'
# 'message_all' adds: 'https://graph.microsoft.com/Mail.ReadWrite' and 'https://graph.microsoft.com/Mail.Send'
