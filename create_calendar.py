# pip install dateutil-parser


def create_calendar(spreadsheet_id):
    import googleapiclient

    from generate_classroom_aspen_tools_credentials import generate_classroom_aspen_tools_credentials
    #from generate_sheets_credential import generate_sheets_credential
    from helper_functions.generate_school_dates import generate_school_dates

    #spreadsheet_id = '1Bows1MWZ8sQAbLZW9t7QTRD-NwNh8bYwua1n1eRvcAE'
    # spreadsheet_id = '1xkcNN1OFmscODqz3zbDUqRbkHAxIuIyx-FtMfXgqczA' # Test_APCSP_Computer_principles
    # spreadsheet_id ='1o_YPtSYB75fk9-r79GhNVqTDdkWr0VZA497nrC4r1h0'
    #spreadsheet_id = '1veaJaPo--jFET5b5LGi71RujwKtIq4IAmuWu3YX8tUo'
    SHEET_NAME = 'Calendar'

    # Generate sheets service object
    services = generate_classroom_aspen_tools_credentials()
    service_sheets = services[1]

    # Read in first day of school, assign to variable first_day
    print("In create_calendar, reading in first day of school")
    range_name = SHEET_NAME + '!F3:F3'  # Cell for first day of school, format 9/4/2018
    try:
        result = service_sheets.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    except googleapiclient.errors.HttpError as error :
        raise Exception(f"Http error.  Is the spreadsheet ID correct?  Tried this spreadsheet ID: {spreadsheet_id}\n"
                        f"The error is this: \n{error}")

    value = result.get('values', [])
    if not value:
        raise ValueError('Expected to see first day of school filled in in cell F3 of spreadsheet ID {}, '
                         'but no nothing there.  Fill in the date and try again.'.format(spreadsheet_id))
    else:
        first_day = value[0][0]

    # Read in holidays (not snow days), assign to variable holidays (which is a list)
    print("In create_calendar, reading in holidays.")
    holidays = list()
    range_name = SHEET_NAME + '!G3:G99'  # Cells for holidays.  Max of 97, but it'll never get that high
    result = service_sheets.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])
    if not values:
        raise ValueError('Expected to see holidays/snow days filled in in cell G3:G99 of spreadsheet ID {},'
                         ' but no nothing there.  Fill in the dates and try again.'.format(spreadsheet_id))
    else:
        for row in values:
            holidays.append(row[0])

    # Read in snow days, assign to list variable snow_days
    print("In create_calendar, reading in snow days")
    snow_days = list()
    range_name = SHEET_NAME + '!H3:H12'  # max of 10 snow days
    result = service_sheets.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])
    for row in values:
        snow_days.append(row[0])
    print(snow_days)
    # All days off is the sum of holidays + snow days
    all_vacation_days = holidays + snow_days

    # Get days we are in school, datetime format i.e. datetime.datetime(2018, 9, 4, 0, 0)
    school_dates_datetime = generate_school_dates(first_day, all_vacation_days)

    number_to_day_of_week = {
        1: "M",
        2: "T",
        3: "W",
        4: "Th",
        5: "F",
    }

    # Clear spreadsheet first
    range_name = SHEET_NAME + '!A3:C200'
    result = service_sheets.spreadsheets().values().clear(spreadsheetId=spreadsheet_id, range=range_name).execute()

    # Generate values list, which is what to insert into Google sheet
    # values = [ school day, date in 9-4-2018 format, day of week in M, T, W format ]
    values = []
    for i, day in enumerate(school_dates_datetime, 1):
        values.append([i, str(day.month) + '-' + str(day.day) + '-'
                       + str(day.year), number_to_day_of_week[day.isoweekday()]])


    # Edit Google sheet to add day of school year, date, and day of week
    body = {
        'values': values
    }
    result = service_sheets.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=range_name,
                                                           valueInputOption='USER_ENTERED', body=body).execute()
    print('Updated {} sheet in Google sheet with ID {}.  {} cells updated '.format(SHEET_NAME, spreadsheet_id,
                                                                                   result.get('updatedCells')))
