# input: spreadhseet ID (string), service object
# output:  list of dictionaries which contain info about the assignment.
#     example dictionary:


def read_lesson_plan(p_spreadsheet_id, p_service):
    range_name = 'Sheet1!B2:BZ41'
    result = p_service.spreadsheets().values().get(majorDimension='COLUMNS',
                                                        spreadsheetId=p_spreadsheet_id,
                                                        range=range_name, ).execute()
    columns = result.get('values', [])

    column_dicts = []
    for column in columns:
        column_dict = {}
        if column[0] == 'announcement':
            if column[1] != '' or column[2] != '' or column[3] != '':
                raise Exception("In lesson with spreadsheet ID {}, rows 3 - 5 must be empty"
                                "for every announcement. \n"
                                " Please check.\n"
                                "Possibly, your file is in the old format.  New format is this:\n"
                                "row 3: topic , row 4: Title text, row 5: Days to complete. "
                                .format(p_spreadsheet_id))
            column_dict['assignment_or_announcement'] = 'announcement'
        elif column[0] == 'assignment':
            print("assignment")
        else:
            raise Exception("In lesson with spreadsheet ID {}, one of the row 2's had something other than"
                            "'announcement' or 'assignment'.".format(p_spreadsheet_id))
        column_dict['text'] = column[4]
        column_dicts.append(column_dict)
    return column_dicts


# from generate_sheets_credential import generate_sheets_credential
# SPREADSHEET_ID = '1zR9dCyNOAikEFXJblvkkTqOUXQkNEm6CG4kIOBZApE4'  # Last day of school (D180)
# service_sheets = generate_sheets_credential()
# abc = read_lesson_plan(SPREADSHEET_ID, service_sheets)
# print(abc)