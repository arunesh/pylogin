import datetime as dt
from O365 import Account, MSGraphProtocol, FileSystemTokenBackend

AZURE_CLIENT_ID='75d1c35d-7ab6-4668-ab3a-0dfe4a1f3ead'
AZURE_CLIENT_SECRET='6T_8Q~AfaYwKIK9BGb98apVT1x-rjN2LQ-jnTb2N'
CALLBACK_URL='http://localhost:5000/outlook_redirect'
CALLBACK_URL_HTTPS='https://localhost:5000/outlook_redirect'
COACH_SCOPES=['basic', 'message_all', 'calendar_all']

#credentials = ('my_client_id', 'my_client_secret')
credentials = (AZURE_CLIENT_ID, AZURE_CLIENT_SECRET)

# the default protocol will be Microsoft Graph
# the default authentication method will be "on behalf of a user"


class BackendAccount(Account):
    def __init__(self, credentials, *, protocol=None, main_resource=None, **kwargs):
        super().__init__(credentials, protocol=protocol, main_resource=main_resource, **kwargs)

    def authenticate_geturl(self, *, scopes=None, **kwargs):
        if self.con.auth_flow_type in ('authorization', 'public'):
            if scopes is not None:
                if self.con.scopes is not None:
                    raise RuntimeError('The scopes must be set either at the Account instantiation or on the account.authenticate method.')
                self.con.scopes = self.protocol.get_scopes_for(scopes)
            else:
                if self.con.scopes is None:
                    raise ValueError('The scopes are not set. Define the scopes requested.')

        consent_url, _ = self.con.get_authorization_url(**kwargs)
        return consent_url

    def authenticate_complete(self, *, scopes=None, token_url=None, **kwargs):
        if token_url:
            result = self.con.request_token(token_url, **kwargs)  # no need to pass state as the session is the same
            if result:
                print('Authentication Flow Completed. Oauth Access Token Stored. You can now use the API.')
            else:
                print('Something go wrong. Please try again.')
                return bool(result)
        else:
            print('Authentication Flow aborted.')
            return False
        return True
    
def get_auth(user_email):
    protocol = MSGraphProtocol()
    token_filename = f'{user_email}_outlook_token.txt'
    print("using token file name " + token_filename)
    token_backend = FileSystemTokenBackend(token_path='live_tokens', token_filename=token_filename)
    outlook_account = BackendAccount(credentials, protocol=protocol, token_backend=token_backend)
    return outlook_account

def get_auth_url(user_email, callback=None):
    user_email = user_email or "default"
    callback = callback or CALLBACK_URL
    acc = get_auth("default")
    url = acc.authenticate_geturl(scopes=COACH_SCOPES, redirect_uri=callback)
    return url

def auth_complete(user_email, url, callback=None):
    acc = get_auth(user_email)
    callback = callback or CALLBACK_URL
    url_https = url
    if url.__contains__('https'):
        print('already https')
    else:
        url_https = url.replace('http', 'https')
    print("URL HTTPS =" + url_https)
    acc.authenticate_complete(scopes=COACH_SCOPES, token_url = url_https, redirect_uri=callback)
    return acc

def schedule_event(user_email, startTime, endTime, subject):

    try:
        subject = subject or "Coach AI Work !"
        acc = get_auth(user_email)
        schedule = acc.schedule()

        calendar = schedule.get_default_calendar()
        new_event = calendar.new_event()  # creates a new unsaved event 
        new_event.subject = subject
        new_event.location = 'California'

        # naive datetimes will automatically be converted to timezone aware datetime
        #  objects using the local timezone detected or the protocol provided timezone

        new_event.start = dt.datetime.fromisoformat(startTime)
        # new_event.start = dt.datetime(year=2022, month=5, day=14, hour=10, minute=0) 
        # so new_event.start becomes: datetime.datetime(2018, 9, 5, 19, 45, tzinfo=<DstTzInfo 'Europe/Paris' CEST+2:00:00 DST>)

        #new_event.recurrence.set_daily(1, end=dt.datetime(2022, month=5, day=17))
        new_event.recurrence.set_daily(1, end=dt.datetime.fromisoformat(endTime))
        new_event.remind_before_minutes = 45

        new_event.save()
        return True
    except: 
        return False

if __name__ == "__main__":
    acc = get_auth("arun@coach.ai")
    url = acc.authenticate_geturl(scopes=COACH_SCOPES)
    print("URL = " + url)
    auth_url = input('Paste the authenticated url here:\n')
    acc.authenticate_complete(scopes=COACH_SCOPES, token_url = auth_url)
