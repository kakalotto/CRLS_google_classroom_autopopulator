# input: spreadhseet ID (string), service object
# output:  list of dictionaries which contain info about the assignment.
#     example dictionary: 


def read_lesson_plan(p_spreadsheet_id, p_service):
    range_name = 'Sheet1!B2:BZ41'
    result = p_service.spreadsheets().values().get(majorDimension='COLUMNS',
                                                        spreadsheetId=p_spreadsheet_id,
                                                        range=range_name, ).execute()
    columns = result.get('values', [])
    return columns