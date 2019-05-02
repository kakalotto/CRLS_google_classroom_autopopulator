# Inputs: spreadsheet ID (integer), service object
# Output: sheet_list, list of sheets in document.


def get_all_sheets(spreadsheet_id, service):
    sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheets = sheet_metadata.get('sheets', '')
    sheet_list = []
    for sheet in sheets:
        sheet_list.append(sheet['properties']['title'])
    print('List of sheets in the {} Google sheet is: {}'.format(spreadsheet_id, sheet_list))
    return sheet_list

# from generate_sheets_credential import generate_sheets_credential
# SPREADSHEET_ID = '1xkcNN1OFmscODqz3zbDUqRbkHAxIuIyx-FtMfXgqczA'  # Game development
# service_sheets = generate_sheets_credential()
# abc = get_all_sheets(SPREADSHEET_ID, service_sheets)
# print(abc)