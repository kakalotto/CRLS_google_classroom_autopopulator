# https://developers.google.com/sheets/api/quickstart/python
# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

# inputs: none
# output: service object for Google sheets
def generate_drive_credential():
    import os.path

    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError

    # If modifying these scopes, delete the file token_drive.json.
    scopes = ['https://www.googleapis.com/auth/documents.readonly',
             'https://www.googleapis.com/auth/drive']

    """Shows basic usage of the Drive v3 API.
    Prints the names an d ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token_drive.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token_drive.json"):
        creds = Credentials.from_authorized_user_file("token_drive.json", scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials_drive.json", scopes
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token_drive.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("drive", "v3", credentials=creds)
        return service
    except HttpError as error:
        print(f"An error occurred: {error}")  # and crash out

    # import pickle
    # import os.path
    # from googleapiclient.discovery import build
    # from google_auth_oauthlib.flow import InstalledAppFlow
    # from google.auth.transport.requests import Request
    # import httplib2
    #
    # scopes = ['https://www.googleapis.com/auth/documents.readonly',
    #           'https://www.googleapis.com/auth/drive']
    # creds = None
    # # The file token_sheets.pickle stores the user's access and refresh tokens, and is
    # # created automatically when the authorization flow completes for the first
    # # time.
    # if os.path.exists('token_drive.pickle'):
    #     with open('token_drive.pickle', 'rb') as token:
    #         creds = pickle.load(token)
    # # If there are no (valid) credentials available, let the user log in.
    # if not creds or not creds.valid:
    #     if creds and creds.expired and creds.refresh_token:
    #         creds.refresh(Request())
    #     else:
    #         # flow = InstalledAppFlow.from_client_secrets_file('credentials_drive_old.json', scopes)
    #         flow = InstalledAppFlow.from_client_secrets_file('credentials_drive.json', scopes)
    #         creds = flow.run_local_server()
    #         # Save the credentials for the next run
    #         with open('token_drive.pickle', 'wb') as token:
    #             pickle.dump(creds, token)
    # try:
    #     service = build('drive', 'v3', credentials=creds)
    # except httplib2.ServerNotFoundError:
    #     raise Exception(
    #             "Could not reach Google's servers to create a Google drive service object. Internet down?"
    #             "Google down?  Your DNS not working?")
    #
    # # Call the drive API
    # print("Google drive service object generated")
    # return service
