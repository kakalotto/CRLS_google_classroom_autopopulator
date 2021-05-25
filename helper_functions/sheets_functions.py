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

