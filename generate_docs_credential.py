# https://developers.google.com/sheets/api/quickstart/python
# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

# # inputs: none
# # output: service object for Google sheets
# def generate_docs_credential():
#     import pickle
#     import os.path
#     from googleapiclient.discovery import build
#     from google_auth_oauthlib.flow import InstalledAppFlow
#     from google.auth.transport.requests import Request
#     import httplib2
# 
#     scopes = ['https://www.googleapis.com/auth/documents.readonly',
#               'https://www.googleapis.com/auth/drive']
#     creds = None
#     # The file token_sheets.pickle stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     if os.path.exists('token_docs.pickle'):
#         with open('token_docs.pickle', 'rb') as token:
#             creds = pickle.load(token)
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file('credentials_docs.json', scopes)
#             creds = flow.run_local_server()
#             # Save the credentials for the next run
#             with open('token_docs.pickle', 'wb') as token:
#                 pickle.dump(creds, token)
#     try:
#         service = build('docs', 'v1', credentials=creds)
#     except httplib2.ServerNotFoundError:
#         raise Exception(
#                 "Could not reach Google's servers to create a Google Docs service object. Internet down?"
#                 "Google down?  Your DNS not working?")
# 
#     # Call the Docs API
#     print("Google Docs service object generated")
#     return service

def generate_docs_credential():
    import os.path
    
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    
    # If modifying these scopes, delete the file token_docs.json.
    scopes = ['https://www.googleapis.com/auth/documents.readonly',
              'https://www.googleapis.com/auth/drive']
    creds = None

    if os.path.exists("token_docs.json"):
        creds = Credentials.from_authorized_user_file("token_docs.json", scopes)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials_docs.json", scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
    with open("token_docs.json", "w") as token:
        token.write(creds.to_json())
    try:
        service = build("docs", "v1", credentials=creds)
        return service
    except HttpError as err:
        print(err)   # and then crashes
