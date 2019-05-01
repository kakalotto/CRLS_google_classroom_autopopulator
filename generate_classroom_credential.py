def generate_classroom_credential():
    import pickle
    import os.path
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request

    SCOPES = ['https://www.googleapis.com/auth/classroom.courses',
              'https://www.googleapis.com/auth/classroom.coursework.students',
              'https://www.googleapis.com/auth/classroom.announcements',
              ]
    creds = None
    # The file token_classroom.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token_classroom.pickle'):
        with open('token_classroom.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token_classroom.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('classroom', 'v1', credentials=creds)
     # Call the Classroom API
    results = service.courses().list(pageSize=10).execute()
    courses = results.get('courses', [])

    if not courses:
        print('No courses found.')
    else:
        print('Courses:')
        for course in courses:
            print(course['name'])


    return service


generate_classroom_credential()

            # from apiclient.discovery import build
    # from httplib2 import Http
    # from oauth2client import file, client, tools
    #
    # # Setup the Classroom API
    # SCOPES = ['https://www.googleapis.com/auth/classroom.courses',
    #           'https://www.googleapis.com/auth/classroom.coursework.students',
    #           'https://www.googleapis.com/auth/classroom.announcements',
    #           ]
    # store = file.Storage('credentials_classroom.json')
    # creds = store.get()
    # if not creds or creds.invalid:
    #     flow = client.flow_from_clientsecrets('google_classroom_client_secret.json', SCOPES)
    #     creds = tools.run_flow(flow, store)
    # service = build('classroom', 'v1', http=creds.authorize(Http()))
    # return service
