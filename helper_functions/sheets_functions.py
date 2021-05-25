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
    except googleapiclient.errors.HttpError:
        print("Crash!   Could not find spreadsheet Do you have a spreadsheet ID of this? " + str(spreadsheet_id))

    values = result.get('values', [])

    if not values:
        raise ValueError("Tried to read from course {} on spreadsheet {}, but there were no values".
                         format(sheet, spreadsheet_id))
    return values
