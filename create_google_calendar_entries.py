def create_google_calendar_entries(*, classname='', document_id='1KLMCq-Nvq-fCNnkCQ7mayIVOSS-HGupSTG_lPT8EPOI',
                           classroom_id='MTY0OTY1NDEyNjg3',
                           spreadsheet_id='1ZenTcQlCQhbYvBvPOVq8XIB2FQgseIGHH4gTBTcw-KY', sheet_id='APCSP_S1_P1',
                           header_text='AP CSP\n', course_id=164978040288,
                           course_contract_link='https://docs.google.com/document/d/'
                                                '1eR5rxgTZ0PXy_fYIFK2SS_Ro770IXxT9sM90vZr_OcU/edit',
                           zoom_links=None,
                           assignments_dictionary={}):
    """
    This creates a calendar document with daily activities, items due and notes.  Named after Dr. Lam, who does
    the same thing
    :param document_id: Google ID of the doc ID to edit (string)
    :param classroom_id: Classroom ID of the classroom to get info from (string)
    :param spreadsheet_id: Google sheets ID of the google sheet daily planner doc (string)
    :param sheet_id: Sheet within the spreadsheet (string)
    :param header_text: String to put at the top of the doc (string)
    :param course_id: ID of the coursenumber to edit (string)
    :param course_contract_link: Link to the course contract (string)
    :param zoom_links: links to the zoom for the class (string)
    :param assignments_dictionary: Dictionary of assignments to shorten because of overlap or length (dict of strings)
    :param fy: Full year or not (Boolean)
    :return: none
    """
    import datetime

    from generate_calendar_credential import generate_calendar_credential

    from helper_functions.calendar_functions import get_calendars, get_calendar_id, add_event_starttime, \
        get_calendar_start_datetime
    from helper_functions.classroom_functions import class_name_2_id
    import re
    import calendar
    # from copy import deepcopy
    from generate_docs_credential import generate_docs_credential
    from generate_sheets_credential import generate_sheets_credential
    from generate_ro_classroom_credential import generate_ro_classroom_credential
    from helper_functions.dr_lam_functions import add_table, delete_entire_document, get_text, \
        add_regular_text, add_bold_normal, add_italic_normal, add_link, get_assignment_link, iter4obj_2_list, \
        insert_page_break
    from helper_functions.dr_lam_requests import requests_header, requests_links
    from helper_functions.sheets_functions import read_course_daily_data_all
    from helper_functions.quarters import quarter_dates
    from helper_functions.sheets_functions import read_in_holidays

    service_calendar = generate_calendar_credential()
    service_classroom_ro = generate_ro_classroom_credential()
    service_sheets = generate_sheets_credential()

    # batch does things in random order. So delete before add
    events_add = []

    # Get ID and name of calendar
    calendars = get_calendars(service_calendar)
    calendar_id = get_calendar_id(classname, calendars)
    calendar = service_calendar.calendars().get(calendarId=calendar_id).execute()
    calendar_name = calendar['summary']

    # Get all events from calendar
    calendar_events = service_calendar.events().list(calendarId=calendar_id).execute()
    calendar_events = calendar_events['items']
    print("Got calendar events")

    # Delete everything after today that isn't an assignment:
    counter = 0
    batch_delete = service_calendar.new_batch_http_request()
    today_datetime = datetime.datetime.today()
    today_datetime = datetime.datetime.combine(today_datetime, datetime.datetime.min.time())
    print(today_datetime)
    for event in calendar_events:
        if re.search('Assignment:', event['summary']):
            print("delete assignment! skip " + str(event['summary']))
            continue
        elif today_datetime > get_calendar_start_datetime(event):
            print("delete event was in he past.  Skipping " + str(event['summary']))
        elif counter < 49:
            print("delete Going to delete this one: " + str(event['summary']))
            counter += 1
            event_id = event['id']
            batch_delete.add(service_calendar.events().delete(calendarId=calendar_id, eventId=event_id))
        else:  # 50 items in list, away we go!
            counter = 0
            batch_delete.execute()
            batch_delete = service_calendar.new_batch_http_request()
    batch_delete.execute()

    # Get ID of Google classroom
    print("Getting Google classroom ID")
    course_id = class_name_2_id(service_classroom_ro, classname)

    # Get assignments and materials from Google classroom
    print("Getting assignments from Google Classroom")
    courseworks = service_classroom_ro.courses().courseWork().list(courseId=course_id).execute().get('courseWork', [])
    for coursework in courseworks:
        print(coursework)
    materials = service_classroom_ro.courses(). \
        courseWorkMaterials().list(courseId=course_id).execute().get('courseWorkMaterial', [])

    # Read in everything from Google sheet (to put in Today and Notes)
    sheet_values = read_course_daily_data_all(spreadsheet_id, sheet_id, service_sheets)

    # Loop over Google sheet, add to events_add and events_delete
    batch = service_calendar.new_batch_http_request()
    for i, value in enumerate(sheet_values):
        date = value[1]
        [month, dom, year] = date.split('/')
        date_obj = datetime.datetime(int(year), int(month), int(dom))
        print(date_obj)
        today_obj = datetime.datetime.now()
        if date_obj < today_obj:
            # print("skipping, this date is before today")
            continue

        # do "Today"
        print(date_obj)
        is_today = True
        is_note = True
        try:
            all_todays = value[3]
        except TypeError:
            is_today = False
        try:
            note = value[7]
        except TypeError:
            is_note = False
        if is_today is False and is_note is False:
            continue
        if is_today:
            todays = all_todays.split('and ')
            for today in todays:
                # clean the assignment up
                clean_today = re.sub(r'^\s+', r'', today)
                clean_today = re.sub(r'\s+$', r'', clean_today)

                summary = 'Today: ' + clean_today
                link = get_assignment_link(assignments_dictionary, clean_today, courseworks, materials)
                description = link

                print(f"Here is the clean assignment: {clean_today} \nhere are the event:s {calendar_events}")
                event = {'summary': summary, 'description': description}
                event = add_event_starttime(event)
                batch.add(service_calendar.events().insert(calendarId=calendar_id, body=event))

            # Do notes
            #             notes = ' '
            #             if len(value) >= 8:
            #                 notes = value[7]
            # same check here - check to see if it's in events.  If so, then deleteold and batch the new one.

    # event = {
    #     'summary': 'Google I/O 2015',
    #     'description': 'A chance to hear more about Google\'s developer products.',
    #     'start': {
    #         'dateTime': '2021-05-28T09:00:00-07:00',
    #         'timeZone': 'America/Los_Angeles',
    #     },
    #     'end': {
    #         'dateTime': '2021-05-28T17:00:00-07:00',
    #         'timeZone': 'America/Los_Angeles',
    #     },
    #
    # }
    #
    # event2 = {
    #     'summary': 'Rocky Balboa',
    #     'description': 'more products.',
    #     'start': {
    #         'dateTime': '2021-05-22T09:00:00-07:00',
    #         'timeZone': 'America/Los_Angeles',
    #     },
    #     'end': {
    #         'dateTime': '2021-05-22T17:00:00-07:00',
    #         'timeZone': 'America/Los_Angeles',
    #     },
    #
    # }
    #abcevent = service_calendar.events().insert(calendarId=calendar_id, body=event).execute()
    #print(abcevent)

    from googleapiclient.http import BatchHttpRequest
    import httplib2
    from googleapiclient import discovery


    batch = service_calendar.new_batch_http_request()

#    batch.add(service_calendar.events().insert(calendarId=calendar_id, body=event2))
    batch.add(service_calendar.events().insert(calendarId=calendar_id, body=event))
    batch.execute()
    print(batch)
    # batch.add(service.calendars().insert(body={'summary': 'Using batch'}, fields='id'), callback=.., request_id=..)
    # batch.execute(http=http)


