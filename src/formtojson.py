import os
from datetime import datetime, timezone, timedelta
from json import dump
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

CLIENT_SECRET = 'client_secret.json'
SCOPES = [
    'https://www.googleapis.com/auth/forms.body.readonly',
    'https://www.googleapis.com/auth/forms.responses.readonly'
]
FORMID = '1PknKhOTcxiA-Tm-aqpqGg-wALJcOtR-y8TRn9tuONjE'
def formtocsv():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET, SCOPES)
            creds = flow.run_local_server()
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

    service_form = build('forms', 'v1', credentials=creds)

    now = datetime.now(timezone.utc)
    yesterday = now - timedelta(days=1)
    yesterday_midnight = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday_timestamp = yesterday_midnight.isoformat("T") + "Z"

    yesterday_response_list = (
        service_form.forms()
        .responses()
        .list(formId=FORMID, filter=f'timestamp >= {yesterday_timestamp}')
        .execute()
    )
    with open(f'data/{yesterday_timestamp[0:10].replace('-', '_')}.json', 'w') as file:
        dump(yesterday_response_list, file)