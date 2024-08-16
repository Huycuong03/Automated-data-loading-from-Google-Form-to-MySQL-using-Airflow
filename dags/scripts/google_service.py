from google.oauth2 import service_account
from googleapiclient import discovery

def create_forms_service(scopes=None):
    credentials = service_account.Credentials.from_service_account_file(
        'dags/scripts/service_account_key.json',
        scopes=scopes
    )
    
    return discovery.build(
        serviceName='forms',
        version='v1',
        credentials=credentials
    )