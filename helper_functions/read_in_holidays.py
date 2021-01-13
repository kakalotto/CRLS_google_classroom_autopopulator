# Input: service object for Google sheets
# Output: list of holidays, format [ '9-4-2018', '3-22-2019' ]

def read_in_holidays(spreadsheet_id, service):
    
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

# from generate_sheets_credential import generate_sheets_credential
# service_sheets = generate_sheets_credential()
# abc = read_in_holidays('1xkcNN1OFmscODqz3zbDUqRbkHAxIuIyx-FtMfXgqczA', service_sheets)
# print(abc)