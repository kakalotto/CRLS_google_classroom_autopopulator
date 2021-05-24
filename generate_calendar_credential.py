from __future__ import print_function


def generate_calendar_credential():
    """
    Create a Google calendar API service credential
    Returns:Google calendar API service credential

    """
    import datetime
    import os.path
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials

    # If modifying these scopes, delete the file token_calendar.json.
    scopes = ['https://www.googleapis.com/auth/calendar',
              'https://www.googleapis.com/auth/calendar.events']

    creds = None
    # The file token_calendar.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token_calendar.json'):
        creds = Credentials.from_authorized_user_file('token_calendar.json', scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials_calendar.json', scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token_calendar.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service


