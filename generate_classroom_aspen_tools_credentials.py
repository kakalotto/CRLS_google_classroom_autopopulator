# https://developers.google.com/classroom/quickstart/python
# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib


# inputs: none
# output: service object for Google classroom
# def generate_classroom_credential():
#     import pickle
#     import os.path
#     from googleapiclient.discovery import build
#     from google_auth_oauthlib.flow import InstalledAppFlow
#     from google.auth.transport.requests import Request
#     import httplib2
#
#     scopes = ['https://www.googleapis.com/auth/classroom.announcements',
#               'https://www.googleapis.com/auth/classroom.courses',
#               'https://www.googleapis.com/auth/classroom.coursework.students',
#               'https://www.googleapis.com/auth/classroom.rosters',
#               'https://www.googleapis.com/auth/classroom.topics',
#               'https://www.googleapis.com/auth/classroom.courseworkmaterials',
#               'https://www.googleapis.com/auth/classroom.profile.emails',
#               'https://www.googleapis.com/auth/classroom.guardianlinks.students.readonly',
#               ]
#
#
#     creds = None
#     # The file token_classroom.pickle stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     if os.path.exists('token_classroom.pickle'):
#         with open('token_classroom.pickle', 'rb') as token:
#             creds = pickle.load(token)
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file('credentials_classroom_aspen_tools.json', scopes)
#             creds = flow.run_local_server()
#             # Save the credentials for the next run
#             with open('token_classroom.pickle', 'wb') as token:
#                 pickle.dump(creds, token)
#     try:
#         service = build('classroom', 'v1', credentials=creds)
#     except httplib2.ServerNotFoundError:
#         raise Exception("Could not reach Google's servers to create a Google CLASSROOM service object. Internet down?"
#                         "Google down?  Your DNS not working?")
#     print("Google classroom service object generated")
#     return service
#

def generate_classroom_aspen_tools_credentials():
    import os.path

    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError

    scopes = ['https://www.googleapis.com/auth/classroom.announcements',
              'https://www.googleapis.com/auth/classroom.courses',
              'https://www.googleapis.com/auth/classroom.coursework.students',
              'https://www.googleapis.com/auth/classroom.topics',
              'https://www.googleapis.com/auth/classroom.courseworkmaterials',
              'https://www.googleapis.com/auth/spreadsheets',
              'https://www.googleapis.com/auth/documents',
              'https://www.googleapis.com/auth/classroom.profile.emails',
              'https://www.googleapis.com/auth/classroom.rosters.readonly',
              ]


    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token_classroom_aspen_tools.json"):
        creds = Credentials.from_authorized_user_file("token_classroom_aspen_tools.json", scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials_classroom_aspen_tools.json", scopes
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token_classroom_aspen_tools.json", "w") as token:
            token.write(creds.to_json())

    try:
        service_classroom = build("classroom", "v1", credentials=creds)
        service_sheets = build("sheets", "v4", credentials=creds)
        service_docs = build("docs", "v1", credentials=creds)

        return [service_classroom, service_sheets, service_docs]

    except HttpError as error:
        print(f"ERROR: Unable to generate credential for classroom aspen tools.   Error is this: {error}")
