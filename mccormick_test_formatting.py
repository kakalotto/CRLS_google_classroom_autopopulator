def create_oss_sheet(cm_id, p1_id, p2_id, p3_id, p4_id):
    from generate_sheets_credential import generate_sheets_credential
    from generate_classroom_credential import generate_classroom_credential
    from helper_functions.dr_lam_functions import get_assignment_link
    import re
    import datetime

    course_id = 153399353373
    datapoints = []
    sheet_name = 'Sheet1'


    service_sheets = generate_sheets_credential()
    service_classroom = generate_classroom_credential()


    # create a spreadsheet here
    spreadsheet = {
        'properties': {
            'title': 'esting'
        }
     }
    #spreadsheet = service_sheets.spreadsheets().create(body=spreadsheet,
    #                                     fields='spreadsheetId').execute()

    #print("Here is the link to the doc: https://docs.google.com/spreadsheets/d/" + spreadsheet.get('spreadsheetId'))
    #sheets_id = spreadsheet.get('spreadsheetId')
    sheets_id = '1OLdx6Nk10cXt-Azzo1WYVXuNzjdcqfzupwAVZtYsZNg'

    print("Getting materials")
    materials = service_classroom.courses(). \
        courseWorkMaterials().list(courseId=course_id).execute().get('courseWorkMaterial', [])

    description = ''
    for material in materials:
        if 'title' in material:
            title = material['title'].lower()
            if re.search('zoom link', str(title)):
                description = material['description']

    link = re.search('https:\/\/zoom.us(.+?)\n', description)
    full_link = 'https://zoom.us' + link.group(1)

    datapoint = {'range': sheet_name + '!' + 'A1', 'values': [[full_link]]}
    datapoints.append(datapoint)

    print("FULL LINK!" + str(full_link))

    today = datetime.datetime.now()
    #print(today)
    #print(today.year)
    #today_day = today.strptime()
    #print(today_day)
    print(today)
    day_of_week = today.weekday()
    monday = today - datetime.timedelta(days=day_of_week)
    current_day = monday
    original_monday = monday
    one_day = datetime.timedelta(days=1)

    datapoint = {'range': 'Sheet1!C1', 'values': [['From']]}
    datapoints.append((datapoint))
    datapoint = {'range': 'Sheet1!D1', 'values': [[str(current_day.strftime('%B %d'))]]}
    datapoints.append((datapoint))
    datapoint = {'range': 'Sheet1!E1', 'values': [['To']]}
    datapoints.append((datapoint))
    datapoint = {'range': 'Sheet1!F1', 'values': [[str((current_day + 5 * one_day).strftime('%B %d'))]]}
    datapoints.append((datapoint))


    print("Getting assignments")
    courseworks = service_classroom.courses().courseWork().list(courseId=course_id).execute().get('courseWork', [])

    cells = [ 'B22', 'C22', 'D22', 'E22', 'F22', 'B24', 'C24', 'D24', 'E24', 'F24',]
    cell_counter = 0
    for i in range(12):
        nothing_due = True
        if i == 5 or i == 6:
            current_day += one_day
            continue
        date = str(current_day.strftime('%Y/%m/%d'))
        total_text = str(current_day) + '\n'
        for coursework in courseworks:
            date = str(current_day.strftime('%Y/%m/%d'))

            if 'dueDate' in coursework:
                year = coursework['dueDate']['year']
                month = coursework['dueDate']['month']
                day = coursework['dueDate']['day']
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
                # print("date and mdy" + str(date) + ' ' + str(mdy))
                if mdy == date:
                    print(coursework)
                    nothing_due = False
                    title = coursework['title']
                    total_text += title + '\n'
                    link = get_assignment_link({}, coursework['title'], courseworks, {})
                    total_text += link + '\n\n'

        print(total_text)
        range_name = sheet_name + '!' + cells[cell_counter]
        datapoint = {'range': range_name, 'values': [[total_text]]}
        datapoints.append(datapoint)

        cell_counter += 1
        current_day += one_day


    body = {'valueInputOption': 'USER_ENTERED', 'data': datapoints}
    sheets_result = service_sheets.spreadsheets().values().batchUpdate(spreadsheetId=sheets_id, body=body).execute()

    DATA = {'requests': [
        {'repeatCell': {
            'range': 'Sheet1!C1',
            'cell':  {'userEnteredFormat': {'textFormat': {'bold': True}, 'wrapStrategy': 'wrap'}},
            'fields': 'userEnteredFormat.textFormat.bold, userEnteredFormat.wrapStrategy,',
        }}
    ]}

    spreadsheet = service_sheets.spreadsheets().get(spreadsheetId=sheets_id).execute()
    print(spreadsheet)

    # DATA = {'requests': [
    #     {'repeatCell': {
    #         'range': {'sheetId': '0',  "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 2, "endColumnIndex": 3},
    #         'cell':  {'userEnteredFormat': {'textFormat': {'bold': True}, 'wrapStrategy': 'wrap' }},
    #         'fields': 'userEnteredFormat.textFormat.bold,userEnteredFormat.wrapStrategy',
    #     }}
    # ]}
    #
    #
    # sheets_result = service_sheets.spreadsheets().batchUpdate(spreadsheetId=sheets_id, body=DATA).execute()


    DATA = {
        'requests': [
            {'repeatCell':
                {
                    'range': {'sheetId': '0',  "startRowIndex": 0, "endRowIndex": 1000, "startColumnIndex": 0, "endColumnIndex": 50},
                    'cell':  {'userEnteredFormat': {'wrapStrategy': 'wrap' }},
                    'fields': 'userEnteredFormat.wrapStrategy',
                }
            }
        ]
    }

    requests_value = []

    # make whole thing wrap
    request = {'repeatCell':
                {
                    'range': {'sheetId': '0',  "startRowIndex": 0, "endRowIndex": 1000, "startColumnIndex": 0, "endColumnIndex": 50},
                    'cell':  {'userEnteredFormat': {'wrapStrategy': 'wrap' }},
                    'fields': 'userEnteredFormat.wrapStrategy',
                }
            }
    requests_value.append(request)

    # center cell
    request =   {'repeatCell':
                {
                    'range': {'sheetId': '0',  "startRowIndex": 0, "endRowIndex":1, "startColumnIndex": 4, "endColumnIndex":5 },
                    'cell':  {'userEnteredFormat': {"horizontalAlignment": 'center' }},
                    'fields': 'userEnteredFormat.horizontalAlignment',
                }
            }

    # vertically center for times
    request =   {'repeatCell':
                {
                    'range': {'sheetId': '0',  "startRowIndex": 4, "endRowIndex": 5, "startColumnIndex": 1, "endColumnIndex":2 },
                    'cell':  {'userEnteredFormat': {"verticalAlignment": 'middle' }},
                    'fields': 'userEnteredFormat.verticalAlignment',
                }
            }
    requests_value.append(request)
    request = {'repeatCell':
        {
            'range': {'sheetId': '0', "startRowIndex": 8, "endRowIndex": 9, "startColumnIndex": 1, "endColumnIndex": 2},
            'cell': {'userEnteredFormat': {"verticalAlignment": 'middle'}},
            'fields': 'userEnteredFormat.verticalAlignment',
        }
    }
    requests_value.append(request)
    request = {'repeatCell':
        {
            'range': {'sheetId': '0', "startRowIndex": 13, "endRowIndex": 14, "startColumnIndex": 1, "endColumnIndex": 2},
            'cell': {'userEnteredFormat': {"verticalAlignment": 'middle'}},
            'fields': 'userEnteredFormat.verticalAlignment',
        }
    }
    requests_value.append(request)
    # Background color of headers
    request =   {'repeatCell':
                {
                    'range':
                        {'sheetId': '0',  "startRowIndex": 2, "endRowIndex": 3,
                         "startColumnIndex": 1, "endColumnIndex":6 },
                    'cell':
                        {'userEnteredFormat': {"backgroundColor": {'red': 0.635, 'green': 0.752, 'blue': 0.788}, }},
                    'fields': 'userEnteredFormat.backgroundColor',
                }
            }
    requests_value.append(request)

    # Background color left most column
    request = {'repeatCell':
        {
            'range':
                {'sheetId': '0', "startRowIndex": 3, "endRowIndex": 20,
                 "startColumnIndex": 1, "endColumnIndex": 2},
            'cell':
                {'userEnteredFormat': {"backgroundColor": {'red': 0.815, 'green': 0.878, 'blue': 0.890}, }},
            'fields': 'userEnteredFormat.backgroundColor',
        }
    }
    requests_value.append(request)

    # merge cells for times
    request = {'mergeCells': {
        'mergeType': 'MERGE_ALL',
        'range': {
            'startRowIndex': 4,
            'endRowIndex': 6,
            'sheetId': '0',
            'startColumnIndex': 1,
            'endColumnIndex': 2,

        }
    }}
    requests_value.append(request)
    request = {'mergeCells': {
        'mergeType': 'MERGE_ALL',
        'range': {
            'startRowIndex': 6,
            'endRowIndex': 8,
            'sheetId': '0',
            'startColumnIndex': 1,
            'endColumnIndex': 2,

        }
    }}
    requests_value.append(request)
    request = {'mergeCells': {
        'mergeType': 'MERGE_ALL',
        'range': {
            'startRowIndex': 13,
            'endRowIndex': 15,
            'sheetId': '0',
            'startColumnIndex': 1,
            'endColumnIndex': 2,

        }
    }}
    requests_value.append(request)

    DATA = {'requests': requests_value}
    sheets_result = service_sheets.spreadsheets().batchUpdate(spreadsheetId=sheets_id, body=DATA).execute()

    # left column times
#    datapoints = {}

    datapoint = {'range': 'Sheet1!B4', 'values': [['8:35 - 9:00']]}
    datapoints.append(datapoint)
    datapoint = {'range': 'Sheet1!B5', 'values': [['9:10 - 10:00']]}
    datapoints.append(datapoint)
    datapoint = {'range': 'Sheet1!B7', 'values': [['10:00 - 10:10']]}
    datapoints.append(datapoint)
    datapoint = {'range': 'Sheet1!B8', 'values': [['10:10 - 11:00']]}
    datapoints.append(datapoint)
    datapoint = {'range': 'Sheet1!B9', 'values': [['11:10 - 11:10']]}
    datapoints.append(datapoint)
    datapoint = {'range': 'Sheet1!B10', 'values': [['11:10 - 12:00']]}
    datapoints.append(datapoint)
    datapoint = {'range': 'Sheet1!B12', 'values': [['12:00 - 12:30']]}
    datapoints.append(datapoint)
    datapoint = {'range': 'Sheet1!B13', 'values': [['12:30 - 1:00']]}
    datapoints.append(datapoint)
    datapoint = {'range': 'Sheet1!B14', 'values': [['1:00 - 1:50']]}
    datapoints.append(datapoint)
    datapoint = {'range': 'Sheet1!B16', 'values': [['1:50 - 2:00']]}
    datapoints.append(datapoint)
    datapoint = {'range': 'Sheet1!B17', 'values': [['2:00 - 2:30']]}
    datapoints.append(datapoint)
    datapoint = {'range': 'Sheet1!B18', 'values': [['2:30 - 3:00']]}
    datapoints.append(datapoint)
    datapoint = {'range': 'Sheet1!B19', 'values': [['60 minutes daily']]}
    datapoints.append(datapoint)


    # M, T, W, Th, and black silver
    cells = ['B3', 'C3', 'D3', 'E3', 'F3', 'B5', 'C5', 'D5', 'E5', 'F5', ]
    current_day = original_monday
    cell_counter = 0
    trailer = ''
    for i in range(5):
        if i == 5 or i == 6:
            current_day += one_day
            continue
        day_of_week = current_day.weekday()
        if day_of_week == 0 or day_of_week == 3:
            trailer = '(Silver)'
        elif day_of_week == 1 or day_of_week == 4:
            trailer = '(Black)'
        date_header = current_day.strftime('%A %m/%d\n' + trailer)
        datapoint = {'range': 'Sheet1!' + cells[cell_counter], 'values': [[date_header]]}
        datapoints.append((datapoint))
        cell_counter += 1
        current_day += one_day

    body = {'valueInputOption': 'USER_ENTERED', 'data': datapoints}
    sheets_result = service_sheets.spreadsheets().values().batchUpdate(spreadsheetId=sheets_id, body=body).execute()



