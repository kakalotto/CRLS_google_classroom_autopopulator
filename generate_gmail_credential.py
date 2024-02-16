def generate_gmail_credential():
    import os.path

    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError

    # If modifying these scopes, delete the file token_gmail.json.
    scopes = ['https://www.googleapis.com/auth/gmail.send',
              'https://www.googleapis.com/auth/gmail.compose',]

    def main():
        """Shows basic usage of the Gmail API.
        Lists the user's Gmail labels.
        """
        creds = None
        # The file token_gmail.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token_gmail.json"):
            creds = Credentials.from_authorized_user_file("token_gmail.json", scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials_gmail.json", scopes
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token_gmail.json", "w") as token:
                token.write(creds.to_json())

        try:
            # Call the Gmail API
            service = build("gmail", "v1", credentials=creds)
            return service
        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f"An error occurred: {error}")

    # import pickle
    # import os.path
    # from googleapiclient.discovery import build
    # from google_auth_oauthlib.flow import InstalledAppFlow
    # from google.auth.transport.requests import Request
    # import httplib2
    #
    # print("Generating gmail token")
    # scopes = ['https://www.googleapis.com/auth/gmail.send',
    #           'https://www.googleapis.com/auth/gmail.compose',]
    #
    # creds = None
    # # The file token_gmail.pickle stores the user's access and refresh tokens, and is
    # # created automatically when the authorization flow completes for the first
    # # time.
    # if os.path.exists('token_gmail.pickle'):
    #     with open('token_gmail.pickle', 'rb') as token:
    #         creds = pickle.load(token)
    # # If there are no (valid) credentials available, let the user log in.
    # if not creds or not creds.valid:
    #     if creds and creds.expired and creds.refresh_token:
    #         creds.refresh(Request())
    #     else:
    #         flow = InstalledAppFlow.from_client_secrets_file('credentials_gmail_2023_09_12.json', scopes)
    #         creds = flow.run_local_server()
    #         # Save the credentials for the next run
    #         with open('token_gmail.pickle', 'wb') as token:
    #             pickle.dump(creds, token)
    # try:
    #     service = build('gmail', 'v1', credentials=creds)
    # except httplib2.ServerNotFoundError:
    #     raise Exception(
    #         "Could not reach Google's servers to create a Google gmail service object. Internet down?"
    #         "Google down?  Your DNS not working?")
    #
    # # Call the gmail API
    # print("Google gmail service object generated")
    # return service
