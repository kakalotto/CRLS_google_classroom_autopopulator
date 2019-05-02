# Inputs: spreadsheet ID (string), id of announcement or assignment (int), day of year (int) ,
#         Googlesheet service object, sheet ID (int)
# Output: none.
# NOTE may need to change to update with 4, 5, 6 IDs instead of just one at a time


def update_sheet_with_id(p_spreadsheet_id, p_id, day, p_service, p_sheet):
    p_cell = 'F' + str(day + 2)
    p_range_name = p_sheet + '!' + p_cell
    p_body = {
        'values': [[p_id]]
    }
    p_result = p_service.spreadsheets().values().update(spreadsheetId=p_spreadsheet_id, range=p_range_name,
                                                        valueInputOption='USER_ENTERED', body=p_body).execute()
    print("Updating Google sheet {}, cell F{} with announce/assignment ID {}.  Total cells updated: {} "
          .format(p_spreadsheet_id, day + 2, p_id, p_result.get('updatedCells')))

# from generate_sheets_credential import generate_sheets_credential
# SPREADSHEET_ID = '1xkcNN1OFmscODqz3zbDUqRbkHAxIuIyx-FtMfXgqczA'  # Game development
# SHEET = 'APCSP_S1_P1'
# service_sheets = generate_sheets_credential()
# day = 1
# update_sheet_with_id(SPREADSHEET_ID, 300, day, service_sheets, SHEET)
