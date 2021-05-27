def create_google_calendar_entries(*, classname='',
                                   spreadsheet_id='1ZenTcQlCQhbYvBvPOVq8XIB2FQgseIGHH4gTBTcw-KY',
                                   sheet_id='APCSP_S1_P1',
                                   assignments_dictionary=None):
    """
    Create Google calendar entries
    Args:
        classname: Name of the class
        spreadsheet_id: Spreadsheet ID of the class we are reading today's work and notes from (string)
        sheet_id: ID of the sheet we want (at the bottom) (string)
        assignments_dictionary: To convert abbreviations in Google classroom to full assignment names (dict)

    Returns:
        none
    """
    import datetime

    from generate_calendar_credential import generate_calendar_credential

    from helper_functions.calendar_functions import get_calendars, get_calendar_id, add_event_starttime, \
        get_calendar_start_datetime
    from helper_functions.classroom_functions import class_name_2_id
    import re
    from generate_sheets_credential import generate_sheets_credential
    from generate_ro_classroom_credential import generate_ro_classroom_credential
    from helper_functions.dr_lam_functions import get_assignment_link
    from helper_functions.sheets_functions import read_course_daily_data_all

    if assignments_dictionary is None:
        assignments_dictionary = {}

    service_calendar = generate_calendar_credential()
    service_classroom_ro = generate_ro_classroom_credential()
    service_sheets = generate_sheets_credential()

    # Get ID and name of calendar
    calendars = get_calendars(service_calendar)
    calendar_id = get_calendar_id(classname, calendars)
    calendar = service_calendar.calendars().get(calendarId=calendar_id).execute()
    calendar_name = calendar['summary']
    print("This is calendar_name " + str(calendar_name))
    # Get all events from calendar
    calendar_events = service_calendar.events().list(calendarId=calendar_id, maxResults=2500).execute()
    calendar_events = calendar_events['items']
    print("Got calendar events")
    # for event in calendar_events:
    #     print(event)
    # Delete everything after today that isn't an assignment:
#    counter = 0
    batch_delete = service_calendar.new_batch_http_request()
    today_datetime = datetime.datetime.today()
    today_datetime = datetime.datetime.combine(today_datetime, datetime.datetime.min.time())
    print("length " + str(len(calendar_events)))
    for event in calendar_events:
        if event['status'] == 'cancelled':
            continue
#        print(event)
        if re.search('Assignment:', event['summary']):
            print("delete assignment! skip " + str(event['summary']))
            continue
        elif today_datetime > get_calendar_start_datetime(event):
            print("delete event was in he past.  Skipping " + str(event['summary']))
        else:
            event_id = event['id']
            batch_delete.add(service_calendar.events().delete(calendarId=calendar_id, eventId=event_id))
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
        today_obj = datetime.datetime.now()
        if date_obj < today_obj:
            continue

        # do "Today"
        print(date_obj)
        is_today = True
        is_note = True
        all_todays = ''
        try:
            all_todays = value[3]
        except TypeError:
            is_today = False
        except IndexError:
            is_today = False
        all_notes = ''
        try:
            all_notes = value[7]
        except TypeError:
            is_note = False
        except IndexError:
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
                zero_month = date_obj.month
                if zero_month < 10:
                    zero_month = '0' + str(zero_month)
                zero_day = date_obj.day
                if zero_day < 10:
                    zero_day = '0' + str(zero_day)
                datestring = str(date_obj.year) + '-' + str(zero_month) + '-' + str(zero_day)
                event = add_event_starttime(event, calendar_name, datestring)
                print("adding this!" + str(event))
                batch.add(service_calendar.events().insert(calendarId=calendar_id, body=event))

        if is_note:
            notes = all_notes.split('and ')
            for note in notes:
                # clean the assignment up
                clean_note = re.sub(r'^\s+', r'', note)
                clean_note = re.sub(r'\s+$', r'', clean_note)

                summary = 'Notes: ' + clean_note
                link = get_assignment_link(assignments_dictionary, clean_note, courseworks, materials)
                description = link

                print(f"Here is the clean Note for the day: {clean_note} \nhere are the event:s {calendar_events}")
                event = {'summary': summary, 'description': description}
                zero_month = date_obj.month
                if zero_month < 10:
                    zero_month = '0' + str(zero_month)
                zero_day = date_obj.day
                if zero_day < 10:
                    zero_day = '0' + str(zero_day)
                datestring = str(date_obj.year) + '-' + str(zero_month) + '-' + str(zero_day)
                event = add_event_starttime(event, calendar_name, datestring, p_offset=25)
                print("adding this!" + str(event))
                batch.add(service_calendar.events().insert(calendarId=calendar_id, body=event))
    batch.execute()
