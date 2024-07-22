import os
import sys
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

SCOPES = [
    'https://www.googleapis.com/auth/docs',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive.metadata.readonly'
]

def get_creds():
    """Получить учетные данные для доступа к Google API."""
    token_path = 'token.json'
    creds_path = 'creds.json'

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        return creds

    if os.path.exists(creds_path):
        return request_creds(creds_path, token_path)

    print('Credentials not present')
    sys.exit(1)

def request_creds(creds_path, token_path):
    """Запрос новых учетных данных и сохранение их в файл."""
    flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
    creds = flow.run_local_server(port=0)
    with open(token_path, 'w') as token:
        token.write(creds.to_json())
    return creds

