def generate_missing_mailer_credential():
    import os.path

    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError

    # If modifying these scopes, delete the file token_gmail.json.
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets.readonly',
        "https://www.googleapis.com/auth/gmail.send",
        'https://www.googleapis.com/auth/classroom.courses.readonly',
        'https://www.googleapis.com/auth/classroom.rosters.readonly',
        'https://www.googleapis.com/auth/classroom.student-submissions.students.readonly',
        'https://www.googleapis.com/auth/classroom.profile.emails',
        'https://www.googleapis.com/auth/classroom.coursework.students',

    ]

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token_google_classroom_send_emails_1.json"):
        creds = Credentials.from_authorized_user_file("token_google_classroom_send_emails_1.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials_google_classroom_send_emails_1.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token_google_classroom_send_emails_1.json", "w") as token:
            token.write(creds.to_json())

    try:
        service_google_classroom_send_emails_1_gmail = build("gmail", "v1", credentials=creds)
        service_google_classroom_send_emails_1_classroom = build("classroom", "v1", credentials=creds)
        service_sheets_classroom_send_emails_1_classroom = build("sheets", "v4", credentials=creds)

        return [service_google_classroom_send_emails_1_classroom, service_google_classroom_send_emails_1_gmail,
                service_sheets_classroom_send_emails_1_classroom]
    except HttpError as error:
        print(f"ERROR: Unable to generate credential for missing_mailer_credential.   Error is this: {error}")
