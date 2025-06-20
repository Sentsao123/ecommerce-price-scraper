from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

def upload_to_gdrive(file_path, folder_id):
    SCOPES = ['https://www.googleapis.com/auth/drive.file']

    service_account_path = os.path.join('credentials', 'service_account.json')
    creds = Credentials.from_service_account_file(service_account_path, scopes=SCOPES)

    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [folder_id],
    }

    media = MediaFileUpload(file_path, resumable=True)

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    print(f"File uploaded with ID: {file.get('id')}")