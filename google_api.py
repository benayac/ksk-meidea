import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
import base64
import urllib

class GoogleApi():
    def __init__(self):
        creds = None
        SCOPES = ['https://mail.google.com/', 'https://www.googleapis.com/auth/drive']
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        self.sheet_service = build('sheets', 'v4', credentials=creds)
        self.email_service = build('gmail', 'v1', credentials=creds)

    def create_message(self, sender, to, subject, message_text):
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        b64_bytes = base64.urlsafe_b64encode(message.as_bytes())
        b64_string = b64_bytes.decode()
        return {'raw': b64_string}

    def send_message(self, user_id, message):
        try:
            message = (self.email_service.users().messages().send(userId=user_id, body=message)
                    .execute())
            print ('Message Id: %s' % message['id'])
            return message
        except urllib.error.HTTPError as e:
            print('An error occurred: %s' % e)

    def read_sheet(self, sheet_id, sheet_range):
        sheet = self.sheet_service.spreadsheets()
        result = sheet.values().get(spreadsheetId=sheet_id,
                                    range=sheet_range).execute()
        values = result.get('values', [])
        return values

    def update_cell(self, sheet_id, cell, message):
        values = [[message]]
        body = {
            'values': values
        }
        result = self.sheet_service.spreadsheets().values().update(
            spreadsheetId=sheet_id, range=cell,
            valueInputOption='USER_ENTERED', body=body).execute()
        print('{0} cells updated.'.format(result.get('updatedCells'))) 