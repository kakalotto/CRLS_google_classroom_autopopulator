# https://developers.google.com/sheets/api/quickstart/python
# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib


def generate_sheets_credential():
    import pickle
    import os.path
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    import httplib2
    
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    creds = None
    # The file token_sheets.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token_sheets.pickle'):
        with open('token_sheets.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials_sheets.json', scopes)
            creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token_sheets.pickle', 'wb') as token:
                pickle.dump(creds, token)
    try:
        service = build('sheets', 'v4', credentials=creds)
    except httplib2.ServerNotFoundError:
        raise Exception(
                "Could not reach Google's servers to create a Google SHEETS service object. Internet down?"
                "Google down?  Your DNS not working?")

    # Call the Sheets API
    print("Google sheets service object generated")
    return service
