import base64
import os
import pickle
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

class GmailService:
    def __init__(self):
        self.creds = None
        self.service = None
        self._authenticate()

    def _authenticate(self):
        token_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'token.pickle')
        
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                self.creds = pickle.load(token)
        
        if self.creds and self.creds.expired and self.creds.refresh_token:
            self.creds.refresh(Request())
            # Save refreshed token
            with open(token_path, 'wb') as token:
                pickle.dump(self.creds, token)
        
        if self.creds and self.creds.valid:
            self.service = build('gmail', 'v1', credentials=self.creds)

    def send_verification_email(self, to_email: str, token: str):
        if not self.service:
            print("Gmail service not authenticated. Cannot send email.")
            return False

        verification_link = f"http://localhost:3000/verify?token={token}"
        
        message_text = f"""
        <h1>Welcome to Seyyul!</h1>
        <p>Please verify your email address by clicking the link below:</p>
        <p><a href="{verification_link}">Verify Email</a></p>
        <p>Or copy this link: {verification_link}</p>
        """

        message = MIMEText(message_text, 'html')
        message['to'] = to_email
        message['from'] = 'me'
        message['subject'] = 'Verify your Seyyul account'

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        
        try:
            self.service.users().messages().send(
                userId='me', body={'raw': raw_message}
            ).execute()
            print(f"Verification email sent to {to_email}")
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
