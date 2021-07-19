# Input: sheet name (string), Google sheet service object
# Output: course ID

def read_course_id(spreadsheet_id, sheet, service):
    range_name = sheet + '!B1'
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id,range=range_name,).execute()
    value = result.get('values', [])
    if not value:
        raise ValueError("Could not read Course ID")  # no more courses
    else:
        course_id = value[0][0]
        return course_id

#
# from generate_sheets_credential import generate_sheets_credential
# SPREADSHEET_ID = '1xkcNN1OFmscODqz3zbDUqRbkHAxIuIyx-FtMfXgqczA'  # Game development
# SHEET = 'APCSP_S1_P1'
# service_sheets = generate_sheets_credential()
# abc = read_course_id(SPREADSHEET_ID, SHEET, service_sheets)
# print(abc)