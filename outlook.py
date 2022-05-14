import datetime as dt
from O365 import Account, MSGraphProtocol

AZURE_CLIENT_ID='75d1c35d-7ab6-4668-ab3a-0dfe4a1f3ead'
AZURE_CLIENT_SECRET='6T_8Q~AfaYwKIK9BGb98apVT1x-rjN2LQ-jnTb2N'

#credentials = ('my_client_id', 'my_client_secret')
credentials = (AZURE_CLIENT_ID, AZURE_CLIENT_SECRET)

# the default protocol will be Microsoft Graph
# the default authentication method will be "on behalf of a user"
protocol = MSGraphProtocol()

outlook_account = Account(credentials, protocol=protocol)
#if outlook_account.authenticate(scopes=['basic', 'message_all', 'calendar_all']):
#   print('Authenticated!')

def get_auth():
    

def schedule_event():
    schedule = outlook_account.schedule()

    calendar = schedule.get_default_calendar()
    new_event = calendar.new_event()  # creates a new unsaved event 
    new_event.subject = 'Coach AI work!'
    new_event.location = 'California'

    # naive datetimes will automatically be converted to timezone aware datetime
    #  objects using the local timezone detected or the protocol provided timezone

    new_event.start = dt.datetime(year=2022, month=5, day=14, hour=10, minute=0) 
    # so new_event.start becomes: datetime.datetime(2018, 9, 5, 19, 45, tzinfo=<DstTzInfo 'Europe/Paris' CEST+2:00:00 DST>)

    new_event.recurrence.set_daily(1, end=dt.datetime(2022, month=5, day=17))
    new_event.remind_before_minutes = 45

    new_event.save()
