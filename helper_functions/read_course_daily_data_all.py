# Input: sheet name (string), Google sheet service object
# Output: 2d list of all of the data in a google sheet with assignments.  Will have link to individual assignments
# IDs of posted assignments, and so on.

def read_course_daily_data_all(spreadsheet_id, sheet, service):
    # Read entire sheet for this particular course
    range_name = sheet + '!A3:F190'
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name, ).execute()
    values = result.get('values', [])
    if not values:
        raise ValueError("Tried to read from course {} on spreadsheet {}, but there were no values".
                         format(sheet, spreadsheet_id))
    return values


# from generate_sheets_credential import generate_sheets_credential
# SPREADSHEET_ID = '1xkcNN1OFmscODqz3zbDUqRbkHAxIuIyx-FtMfXgqczA'  # Game development
# SHEET = 'APCSP_S1_P1'
# service_sheets = generate_sheets_credential()
# abc = read_course_daily_data_all(SPREADSHEET_ID, SHEET, service_sheets)
# print(abc)