def create_hyperlink(x, y, link, link_name, sheet_id):
    hyperlink = 'HYPERLINK("' + link + '", "' + link_name + '")'
    return_dict = {
        "updateCells": {
            "rows": [
                {
                    "values": [{
                        "userEnteredValue": {
                            "formulaValue": '=' + hyperlink,

                        }
                    }]
                }
            ],
            "fields": "userEnteredValue",
            "start": {
                "sheetId": sheet_id,
                "rowIndex": y,
                "columnIndex": x
            }
        }}

    return return_dict

    #     # DATA = {'requests': [
    #     #     {'repeatCell': {
    #     #         'range': {'sheetId': '0',  "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 2, "endColumnIndex": 3},
    #     #         'cell':  {'userEnteredFormat': {'textFormat': {'bold': True}, 'wrapStrategy': 'wrap' }},
    #     #         'fields': 'userEnteredFormat.textFormat.bold,userEnteredFormat.wrapStrategy',
    #     #     }}
    #     # ]}

def create_oss_sheet(*, name='', advisory_link='',cm_link='', course_ids=''):
    from generate_sheets_credential import generate_sheets_credential
    from generate_classroom_credential import generate_classroom_credential
    from generate_drive_credential import generate_drive_credential

    from helper_functions.dr_lam_functions import get_assignment_link
    import re
    import datetime

    if course_ids is None:
        course_ids = []


    TEMPLATE_SHEET_ID = '1RQ-as6qcsOSC93dmDvdLhu85AocoY8ybt2g4Ujo8DDQ'
    sheet_name = 'Test version'

    # Generate all the service  objects
    service_sheets = generate_sheets_credential()
    service_classroom = generate_classroom_credential()
    service_drive = generate_drive_credential()

    #Copy the file and get the ID
    copied_file = {'title': 'Erics test'}
    copied_file = service_drive.files().copy(fileId=TEMPLATE_SHEET_ID,body=copied_file).execute()
    new_sheet_id = copied_file['id']
    print("Here is link to the new doc: https://docs.google.com/spreadsheets/d/" + new_sheet_id)

    datapoints = []
    requests_value = []

    class_link_cells = [[[1, 6], [2, 6], [4, 6], [5, 6]], [[1, 9], [2, 9], [4, 9], [5, 9]],
                        [[1, 12], [2, 12], [4, 12], [5, 12]], [[1, 15], [2, 15], [4, 15], [5, 15], ]]


    # Fill in all the zoom links
    for i, course_id in enumerate(course_ids):
        if not course_id:
            continue

        # Getting zoom link for each class
        print("Getting Zoom link for period " + str(i + 1))
        materials = service_classroom.courses().courseWorkMaterials().list(courseId=course_id).execute().\
            get('courseWorkMaterial', [])
        description = ''
        for material in materials:
            if 'title' in material:
                title = material['title'].lower()
                if re.search('zoom link', str(title)) or re.search('zoom_link', str(title)):
                    description = material['description']
        link = re.search('https:\/\/zoom.us(.+?)\n', description)
        full_link = ''
        if not link:
            print("Could not find a zoom link for period " + str(i + 1))
        else:
            full_link = 'https://zoom.us' + link.group(1)
        print("FULL LINK!" + str(full_link))

        row = class_link_cells[i]
        period = 'Period ' + str(i + 1) + ' Zoom link'
        for point in row:
            x = point[0]
            y = point[1]
            request = create_hyperlink(x, y, full_link, period, 0)
            requests_value.append(request)



    DATA = {'requests': requests_value}

    sheets_result = service_sheets.spreadsheets().batchUpdate(spreadsheetId=new_sheet_id, body=DATA).execute()


    # Get the correct week
    today = datetime.datetime.now()
#     #today_day = today.strptime()
#     #print(today_day)
#     print(today)
    day_of_week = today.weekday()
    if day_of_week  > 4:
        monday = today + datetime.timedelta(days=(7 - int(day_of_week)))
    else:
        monday = today - datetime.timedelta(days=day_of_week)
    current_day = monday
    original_monday = monday
    one_day = datetime.timedelta(days=1)


    # Print out from/to dates
    datapoint = {'range': 'Test version!D1', 'values': [[str(current_day.strftime('%B %d'))]]}
    datapoints.append((datapoint))
    datapoint = {'range': 'Test version!F1', 'values': [[str((current_day + 5 * one_day).strftime('%B %d'))]]}
    datapoints.append((datapoint))

    body = {'valueInputOption': 'USER_ENTERED', 'data': datapoints}
    sheets_result = service_sheets.spreadsheets().values().batchUpdate(spreadsheetId=new_sheet_id, body=body).execute()
    print(sheets_result)

    # Print out assignments
    print("Getting assignments")
    courseworks = service_classroom.courses().courseWork().list(courseId=course_id).execute().get('courseWork', [])

    requests_value = []
    cells = [[1, 26], [2, 26], [3, 26], [4, 26], [5, 26]]
    cell_counter = 0
    for i in range(0, 5):
        x = cells[i][0]
        y = cells[i][1]
        max_y = 1
        nothing_due = True
        if i == 5 or i == 6:
            current_day += one_day
            continue
        # Loop over everything, see what is due.
        for coursework in courseworks:
             date = str(current_day.strftime('%Y/%m/%d'))
             if 'dueDate' in coursework:
                 # get the due date of the assignment as mdy
                 year = coursework['dueDate']['year']
                 month = coursework['dueDate']['month']
                 day = coursework['dueDate']['day']
                 # adjust for assignments with no due date
                 if coursework['dueTime']['hours'] == 4 and coursework['dueTime']['minutes'] == 59:
                     new_date = datetime.datetime(year, month, day)
                     new_date -= one_day
                     year = new_date.year
                     month = new_date.month
                     day = new_date.day
                 if day < 10:
                     day = '0' + str(day)
                 if month < 10:
                     month = '0' + str(month)
                 mdy = str(year) + '/' + str(month) + '/' + str(day)
                 if mdy == date:

                     nothing_due = False
                     title = coursework['title']
                     link = get_assignment_link({}, coursework['title'], courseworks, {})
                     request = create_hyperlink(x, y, link, title, 0)
                     y += 1
                     requests_value.append(request)
        current_day += one_day

    DATA = {'requests': requests_value}

    if requests_value:
        sheets_result = service_sheets.spreadsheets().batchUpdate(spreadsheetId=new_sheet_id, body=DATA).execute()
        print(sheets_result)


#
#         print(total_text)
#         range_name = sheet_name + '!' + cells[cell_counter]
#         datapoint = {'range': range_name, 'values': [[total_text]]}
#         datapoints.append(datapoint)
#
#         cell_counter += 1
#         current_day += one_day
#
#
#     body = {'valueInputOption': 'USER_ENTERED', 'data': datapoints}
#     sheets_result = service_sheets.spreadsheets().values().batchUpdate(spreadsheetId=sheets_id, body=body).execute()
#
#     DATA = {'requests': [
#         {'repeatCell': {
#             'range': 'Sheet1!C1',
#             'cell':  {'userEnteredFormat': {'textFormat': {'bold': True}, 'wrapStrategy': 'wrap'}},
#             'fields': 'userEnteredFormat.textFormat.bold, userEnteredFormat.wrapStrategy,',
#         }}
#     ]}
#
#     spreadsheet = service_sheets.spreadsheets().get(spreadsheetId=sheets_id).execute()
#     print(spreadsheet)
#
#     # DATA = {'requests': [
#     #     {'repeatCell': {
#     #         'range': {'sheetId': '0',  "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 2, "endColumnIndex": 3},
#     #         'cell':  {'userEnteredFormat': {'textFormat': {'bold': True}, 'wrapStrategy': 'wrap' }},
#     #         'fields': 'userEnteredFormat.textFormat.bold,userEnteredFormat.wrapStrategy',
#     #     }}
#     # ]}
#     #
#     #
#     # sheets_result = service_sheets.spreadsheets().batchUpdate(spreadsheetId=sheets_id, body=DATA).execute()
#
#
#     DATA = {
#         'requests': [
#             {'repeatCell':
#                 {
#                     'range': {'sheetId': '0',  "startRowIndex": 0, "endRowIndex": 1000, "startColumnIndex": 0, "endColumnIndex": 50},
#                     'cell':  {'userEnteredFormat': {'wrapStrategy': 'wrap' }},
#                     'fields': 'userEnteredFormat.wrapStrategy',
#                 }
#             }
#         ]
#     }
#
#     requests_value = []
#