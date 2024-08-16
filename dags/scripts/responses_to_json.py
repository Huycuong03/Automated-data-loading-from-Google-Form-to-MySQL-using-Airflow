import json
from datetime import datetime, timedelta, timezone
from google_service import create_forms_service

SCOPES = [
    "https://www.googleapis.com/auth/forms.body.readonly",
    "https://www.googleapis.com/auth/forms.responses.readonly"
]
FORMID = "1PknKhOTcxiA-Tm-aqpqGg-wALJcOtR-y8TRn9tuONjE"

def responses_to_json(ti):
    service = create_forms_service(SCOPES)
    today = datetime.now(timezone.utc)
    yesterday = today - timedelta(days=1)

    data = service.forms().responses().list(formId=FORMID, filter=f'timestamp >= {yesterday.isoformat('T')}Z').execute()
    file_name = f'data/json/{yesterday.strftime("%Y_%m_%d")}.json'
    
    with open(file_name, 'w') as file:
        json.dump(data, file)
        ti.xcom_push(key='json_file', value=file_name)