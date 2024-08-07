def get_all_sheets(spreadsheet_id, p_service):
    import googleapiclient.errors
    """
    Gets the names of all of the sheets in the spreadsheet
    Args:
        spreadsheet_id:  ID of the Google spreadsheet (str)
        p_service:  Google sheets API object

    Returns:

    """
    try:
        sheet_metadata = p_service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    except googleapiclient.errors.HttpError as error:
        raise Exception(f"Crashed. trying to read Google sheet.\n"
                        f"Error is this: {error}\n"
                        f"Requested entity was not found:\n"
                        f"   Check that you have the correct spreadsheet_id in ini file")

    sheets = sheet_metadata.get('sheets', '')
    sheet_list = []
    for sheet in sheets:
        sheet_list.append(sheet['properties']['title'])
    print('List of sheets in the {} Google sheet is: {}'.format(spreadsheet_id, sheet_list))
    return sheet_list


def read_course_daily_data_all(spreadsheet_id, sheet, service):
    """
    Reads in all the data about assignments, coursework, etc... from Google sheets
    :param spreadsheet_id: ID of the Google spreadsheet (str)
    :param sheet: Name of the Google spreadsheet (bottom tabs) (str)
    :param service: Google sheets API object
    Returns:
    Values of what is in Google sheets (list of lists)
    """
    import googleapiclient
    # Read entire sheet for this particular course
    range_name = sheet + '!A3:H190'

    try:
        result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name, ).execute()
    except googleapiclient.errors.HttpError as error:
        print(f"Error: {error}\n"
              f"Spreadsheet ID read in is this: {spreadsheet_id}\n")
    values = result.get('values', [])

    if not values:
        raise ValueError("Tried to read from course {} on spreadsheet {}, but there were no values".
                         format(sheet, spreadsheet_id))
    return values


def read_in_holidays(spreadsheet_id, service):
    """
    Reads in all t holidays from Google sheets
    :param spreadsheet_id: ID of the Google spreadsheet (str)
    :param service: Google sheets API object
    Returns:
    List of holiday dates (lists)
    """

    p_holidays = []
    range_name = 'Calendar' + '!G3:G99'  # Cells for holidays.  Max of 99, but it'll never get that high
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])
    if not values:
        raise ValueError('Expected to see holidays filled in in cell G3:G99 of spreadsheet ID {},'
                         ' but no nothing there.  Fill in the dates and try again.'.format(spreadsheet_id))
    else:
        for row in values:
            p_holidays.append(row[0])
    return p_holidays

