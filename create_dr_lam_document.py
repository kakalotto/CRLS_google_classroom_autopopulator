def create_dr_lam_document(*, document_id='1KLMCq-Nvq-fCNnkCQ7mayIVOSS-HGupSTG_lPT8EPOI',
                           classroom_id='MTY0OTY1NDEyNjg3',
                           spreadsheet_id='1ZenTcQlCQhbYvBvPOVq8XIB2FQgseIGHH4gTBTcw-KY', sheet_id='APCSP_S1_P1',
                           header_text='AP CSP\n', course_id=164978040288,
                           course_contract_link='https://docs.google.com/document/d/'
                                                '1eR5rxgTZ0PXy_fYIFK2SS_Ro770IXxT9sM90vZr_OcU/edit',
                           zoom_links=None,
                           assignments_dictionary=None, fy=False):
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
    import re
    import calendar
    import datetime
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

    if zoom_links is None:
        zoom_links = ['https://zoom.us/j/9332367963?pwd=WElmWmc0dHBqSjY2MDFpaWJsbEFsdz09']
    if assignments_dictionary is None:
        assignments_dictionary = {}

    service_doc = generate_docs_credential()
    service_sheets = generate_sheets_credential()
    service_classroom = generate_ro_classroom_credential()

    calendar_obj = calendar.Calendar()

    # Start over
    print("Deleting old document")
    doc_contents = get_text(service_doc, document_id)
    delete_entire_document(service_doc, document_id, doc_contents)

    # Write header to doc
    print("starting header printout")
    [last_index, batch_requests] = requests_header(header_text, course_contract_link)

    # Make a table to put the links.  This table is 14 long
    batch_requests = add_table(1, 5, last_index, batch_requests)
    last_index += 14  # This table is always size 14

    # Write links to header table
    print("starting links printout")
    [last_index, batch_requests] = requests_links(last_index, classroom_id, zoom_links, batch_requests)
    last_index += 2

    # Read Google classroom for all of the course info
    print("Getting assignments from Google Classroom")
    courseworks = service_classroom.courses().courseWork().list(courseId=course_id).execute().get('courseWork', [])
    print("Getting materials from Google classroom")
    materials = service_classroom.courses(). \
        courseWorkMaterials().list(courseId=course_id).execute().get('courseWorkMaterial', [])

    # Read Google sheets automator file for info about file names, etc...
    print("Reading info from Google sheets")
    sheet_values = read_course_daily_data_all(spreadsheet_id, sheet_id, service_sheets)

    # read in holidays
    holidays = read_in_holidays(spreadsheet_id, service_sheets)
    # print(f"These are the holidays {holidays}")

    # Find the start of the quarter
    [q_start, q_end] = quarter_dates(fy=fy)
    print(f"Start quarter for course is this: {q_start} End quarter for course is this: {q_end}")
    iter4_obj = calendar_obj.itermonthdays4(q_start.year, q_start.month)
    cal_list = iter4obj_2_list(iter4_obj)
    cal_month = q_start.month
    cal_list_counter = 0
    # print(cal_list)

    # Add header for month and create the table
    [last_index, batch_requests] = insert_page_break(last_index, batch_requests)
    [previous_last, last_index, batch_requests] = add_regular_text('\n\n ' + calendar.month_name[cal_month] +
                                                                   '\n\n', last_index, batch_requests)
    batch_requests = add_bold_normal(previous_last, last_index, batch_requests)
    batch_requests = add_table(6, 5, last_index, batch_requests)
    last_index += 4  # 5x5 table is always this size

    # print("last index before starting to fill the month " + str(last_index))
    # Takes the list of lesson plans and intercalates holidays
    skip = False
    holiday_counter = 0
    new_sheet_values = []
    for i, value in enumerate(sheet_values):
        date = value[1]
        date_list = date.split('/')
        month = date_list[0]
        dom = date_list[1]
        year = date_list[2]
        sheet_value_date_obj = datetime.datetime(int(year), int(month), int(dom))
        check_holiday = True
        while holiday_counter < len(holidays) and check_holiday:
            holiday = holidays[holiday_counter]
            holiday_list = holiday.split('/')
            holiday_month = holiday_list[0]
            holiday_dom = holiday_list[1]
            holiday_year = holiday_list[2]
            holiday_obj = datetime.datetime(int(holiday_year), int(holiday_month), int(holiday_dom))
            if holiday_obj < sheet_value_date_obj:
                new_sheet_values.append(['0', holiday, 'dummy', 'dummy', 'dummy', 'dummy', 'dummy', 'dummy',
                                         'dummy', 'dummy'])
                holiday_counter += 1
            else:
                check_holiday = False
                new_sheet_values.append(value)
        if holiday_counter >= len(holidays):
            new_sheet_values.append(value)

    # Go through full list of lesson plans and holidays
    for i, value in enumerate(new_sheet_values):
        if skip:
            continue
        is_holiday = False
        # print("value" + str(value))
        if len(value) == 3:
            continue
        if len(value) == 10:
            is_holiday = True
        # if i > 17:
        #     continue;
        # if i < 88:
        #     continue
        # if i < 93:
        #     continue
        # if i > 96:
        #     break
        #     break
        # Add day and date header

        day = value[0]
        date = value[1]
        date_list = date.split('/')
        month = date_list[0]
        dom = date_list[1]
        year = date_list[2]
        today_datetime = datetime.datetime(int(year), int(month), int(dom))
        # print(f" {today_datetime} {q_start} {q_end}")
        if today_datetime < q_start:
            # print("skipping it's before")
            continue
        elif today_datetime > q_end:
            # print("skipping it's after")
            continue

        if int(month) > cal_month or (int(month) == 1 and cal_month == 12):
            # Make a new calendar here
            # print("Making new calendar here!")
            cal_month = int(month)
            # old_cal_list = deepcopy(cal_list)  # save the old cal list

            # Skip to the end of the month
            for j in range(cal_list_counter, 42):
                # print(f"generating new calendar and flushing.  "
                #       f"j is this {j} + last index {last_index}")
                # try:
                #     print(f"old_cal_list {old_cal_list[i]}")
                # except IndexError:
                #     print("past the list")
                if j % 7 == 6:
                    last_index += 3
                elif j % 7 != 4 and j % 7 != 5:
                    last_index += 2

            # print("index before new month " + str(last_index))
            # Add header for month and create the table

            [last_index, batch_requests] = insert_page_break(last_index, batch_requests)
            [previous_last, last_index, batch_requests] = add_regular_text('\n\n ' + calendar.month_name[cal_month] +
                                                                           '\n\n', last_index, batch_requests)
            batch_requests = add_bold_normal(previous_last, last_index, batch_requests)
            batch_requests = add_table(6, 5, last_index, batch_requests)
            last_index += 4  # Jump ahead to the next calendar

            # create the new cal list
            iter4_obj = calendar_obj.itermonthdays4(int(year), int(month))
            cal_list = iter4obj_2_list(iter4_obj)
            cal_month = int(month)
            # print("new calendar list")
            # for k, j in enumerate(cal_list):
            #     print(str(k) + " " + str(j))
            # print(cal_list)

            # Reset the calendar list counter
            cal_list_counter = 0
            # print(f"last index after adding new talbe {last_index}")

        today_cal = cal_list[cal_list_counter]
        not_found = True
        # print(f"THIS IS THE DATE LOOKING FOR {year} {month} {dom}")
        while not_found:
            # print(f"Looking for!{today_cal[0]} month {today_cal[1]}  day {today_cal[2]}")
            if today_cal[0] == int(year) and today_cal[1] == int(month) and today_cal[2] == int(dom):
                not_found = False
            else:
                if cal_list_counter == len(cal_list) - 1:
                    # print("DONE!")
                    not_found = False
                    continue

                if cal_list_counter % 7 == 6:
                    last_index += 3
                elif cal_list_counter % 7 != 4 and cal_list_counter % 7 != 5:
                    last_index += 2
                cal_list_counter += 1
                # print(cal_list_counter)
                today_cal = cal_list[cal_list_counter]

        #
        # month_info = calendar_obj.itermonthdays4(year, month)
        # last_index=696
        # calendar_obj.itermonthdays2(year, month):
        # print("starting this one here " + str(last_index))
        # 704  is at the last one 707 for next line
        day_of_week = value[2]
        # print(f"wooo {month} {dom} {year}")
        # for day in calendar_obj.itermonthdays2(2018, 9):
        #     print(day)
        if is_holiday:
            text = "\n" + ' ' + date + ' \nSchool holiday \n'
            [previous_last, last_index, batch_requests] = add_regular_text(text, last_index, batch_requests)
            batch_requests = add_bold_normal(previous_last, last_index, batch_requests)
        else:
            text = "\n" + ' ' + date + " " + day_of_week + ' Day ' + str(day) + "\n"
            [previous_last, last_index, batch_requests] = add_regular_text(text, last_index, batch_requests)
            batch_requests = add_bold_normal(previous_last, last_index, batch_requests)

            # Add "Due today:" header
            text = 'Due today:\n'
            [previous_last, last_index, batch_requests] = add_regular_text(text, last_index, batch_requests)
            batch_requests = add_italic_normal(previous_last, last_index, batch_requests)

            # Look for what is actually due
            nothing_due = True
            for coursework in courseworks:
                if 'dueDate' in coursework:
                    year = coursework['dueDate']['year']
                    month = coursework['dueDate']['month']
                    day = coursework['dueDate']['day']
                    mdy = str(month) + '/' + str(day) + '/' + str(year)
                    if mdy == date:
                        nothing_due = False
                        title = coursework['title']
                        title_text = title + '\n'
                        [previous_last, last_index, batch_requests] = \
                            add_regular_text(title_text, last_index, batch_requests)
                        link = get_assignment_link(assignments_dictionary, coursework['title'], courseworks, materials)
                        batch_requests = add_link(link, previous_last, last_index, batch_requests)
            if nothing_due:
                [_, last_index, batch_requests] = add_regular_text('Nothing due yet! '
                                                                   '\n', last_index, batch_requests)

            # Print out Today header:
            [previous_last, last_index, batch_requests] = add_regular_text('\nToday:\n', last_index, batch_requests)
            batch_requests = add_italic_normal(previous_last, last_index, batch_requests)

            # Add Today's assignments
            all_assignments = value[3]
            assignments = all_assignments.split('and ')

            for assignment in assignments:
                # Get the assignment name
                # print("assignment " + str(assignment))
                clean_assignment = re.sub(r'^\s+', r'', assignment)
                clean_assignment = re.sub(r'\s+$', r'', clean_assignment)

                # Get ready to write the name of the assignment
                index_assignment_start = last_index
                # print(f"last index  at beginning of write {last_index}")
                assignment_text = clean_assignment + '\n'
                assignment_dict = {
                    'insertText': {
                        'location': {
                            'index': last_index,
                        },
                        'text': assignment_text
                    }
                }
                last_index += len(clean_assignment) + 1
                batch_requests.append(assignment_dict)

                # get the link to the assignment or material
                link = get_assignment_link(assignments_dictionary, clean_assignment, courseworks, materials)
                batch_requests = add_link(link, index_assignment_start, last_index, batch_requests)

            # Add "Class notes:" header
            text = '\nClass Notes:\n'
            [previous_last, last_index, batch_requests] = add_regular_text(text, last_index, batch_requests)
            batch_requests = add_italic_normal(previous_last, last_index, batch_requests)
            #        notes = '\n'
            #   notes = ''
            notes = ' '
            if len(value) >= 8:
                notes = value[7]
            [_, last_index, batch_requests] = add_regular_text(notes + '', last_index, batch_requests)

            #        [_, last_index, batch_requests] = add_regular_text(notes, last_index, batch_requests)

            # Go to the next cell after printing out today's stuff
            # last_index += 2
            # print("This is last index at end of day" + str(last_index))

    # print("Printing out the schedule now...\n")
    print(batch_requests)

    service_doc.documents().batchUpdate(documentId=document_id, body={'requests': batch_requests}).execute()
