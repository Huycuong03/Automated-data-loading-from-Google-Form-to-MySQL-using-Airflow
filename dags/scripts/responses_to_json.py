from datetime import datetime, timedelta, timezone
from scripts.google_service import create_forms_service

SCOPES = [
    "https://www.googleapis.com/auth/forms.body.readonly",
    "https://www.googleapis.com/auth/forms.responses.readonly"
]
FORMID = "1PknKhOTcxiA-Tm-aqpqGg-wALJcOtR-y8TRn9tuONjE"

def responses_to_json(ti):
    service = create_forms_service(SCOPES)
    today = datetime.now(timezone.utc)
    yesterday = today - timedelta(days=1)

    data = service.forms().responses().list(formId=FORMID, filter=f'timestamp >= {yesterday.strftime('%Y-%m-%dT%H:%M:%SZ')}').execute()
    ti.xcom_push(key='json_data', value=data)