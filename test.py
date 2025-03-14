import os
import google.auth
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Define the scope (permission level)
SCOPES = ['https://www.googleapis.com/auth/drive.file']


def authenticate():
    """Handles OAuth 2.0 authentication."""

    # Use the OAuth2.0 credentials (downloaded JSON file from Google Cloud Console)
    creds = None
    if os.path.exists('token.json'):
        creds = google.auth.load_credentials_from_file('token.json')[0]

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Launch OAuth 2.0 flow to get credentials
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)  # Specify your credentials file
            creds = flow.run_local_server(port=0)  # Start the local server for authentication

        # Save credentials for future use
        with open('token.json', 'w') as token:
            print(creds.to_json())
            token.write(creds.to_json())

    return creds


def upload_file(file_path):
    """Uploads a file to Google Drive."""

    creds = authenticate()  # Authenticate using OAuth credentials

    # Build the service
    service = build('drive', 'v3', credentials=creds)

    # Create the file metadata
    file_metadata = {'name': os.path.basename(file_path)}

    # Prepare the file for upload
    media = MediaFileUpload(file_path, resumable=True)

    # Upload the file
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f'File uploaded. File ID: {file["id"]}')


# Example usage: upload a file to Google Drive
upload_file('schema.py')  # Replace with the actual file path
