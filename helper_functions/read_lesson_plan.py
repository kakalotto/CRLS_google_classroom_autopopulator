# input: spreadhseet ID (string), service object
# output:  list of dictionaries which contain info about the assignment.
#     example dictionary:


def read_lesson_plan(p_spreadsheet_id, p_service):

    import googleapiclient

    from helper_functions.unicode_text import unicode_text
    from helper_functions.get_attachments import get_attachments

    range_name = 'Sheet1!B2:BZ41'
    try:
        result = p_service.spreadsheets().values().get(majorDimension='COLUMNS',
                                                       spreadsheetId=p_spreadsheet_id,
                                                       range=range_name, ).execute()
        columns = result.get('values', [])
    except googleapiclient.errors.HttpError as error:
        raise Exception(f"Error: {error}"
                        f"Trying to read this spreadsheet id {p_spreadsheet_id}.\n"
                        f"The caller does not have permission:\n"
                        f"   Be sure the spreadsheet {p_spreadsheet_id} is shared to user of the token\n"
                        f"Requested entity was not found:\n"
                        f"   Check the link (probably wrong)\n  ")
    column_dicts = []
    for column in columns:
        column_dict = {}
        # print("blah {}".format(column))
        # print("COLUMN " + str(column) + " id " + p_spreadsheet_id)
        if column[0] == 'announcement':
            if column[1] != '' or column[2] != '' or column[3] != '':
                raise Exception("In lesson with spreadsheet ID {}, rows 3 - 5 must be empty"
                                "for every announcement. \n"
                                " Please check.\n"
                                "Possibly, your lesson file is in the old format with no topic.  New format is this:\n"
                                "row 3: topic , row 4: Title text, row 5: Days to complete. \n"
                                "Also, possible you selected 'announcement' when you meant 'assignment'."
                                "Or else you put a topic with an announcement."
                                .format(p_spreadsheet_id))
            column_dict['assignment_or_announcement'] = 'announcement'
        elif column[0] == 'assignment':
            if not str.isdigit(column[3]):
                raise Exception("row 3 is not an integer in lesson with spreadsheet ID {}.\n"
                                "This probably means you forgot to add days to finish.   {}"
                                .format(p_spreadsheet_id, column[3]))
            if column[1] == '' or column[2] == '' or column[3] == '':
                raise Exception("In lesson with spreadsheet ID {}, rows 3 - 5 must be filled out "
                                "for every assignment. \n"
                                " Please check and add topic, title text, and days to complete.\n"
                                "Or else possibly, you selected 'assignment' when you meant 'announcement'. \n"
                                "Or else you put a topic with an announcement."
                                .format(p_spreadsheet_id))
            else:
                column_dict['assignment_or_announcement'] = 'assignment'
                try:
                    if column[5].isdigit():
                        column_dict['points'] = column[5]
                except IndexError:
                    raise Exception(f"List index out of range.  Did you forget to put points?  Here is column {column}")

                if column[5].isdigit() or column[5].replace(".", "", 1).isdigit():
                    column_dict['points'] = column[5]
                else:
                    column_dict['points'] = 0
                column_dict['topic'] = column[1]
                column_dict['title'] = column[2]
                column_dict['days_to_complete'] = column[3]
                column_dict['attachments'] = get_attachments(column, column_dict['points'])

        elif column[0] == 'materials':
            # print("MATERIALS! " + str(column))
            if column[3] != '':
                raise Exception("In lesson with spreadsheet ID {}, row 3 (days to complete) sould be empty if it's"
                                "a materials.\n"
                                "Please check.\n"
                                "Possibly, your lesson file is in the old format with no topic."
                                .format(p_spreadsheet_id))

            if len(column) != 5 and column[5] != '':
                raise Exception("In lesson with spreadsheet ID {}, row 5 (points) should be empty if it's"
                                "a materials.\n"
                                "Please check.\n"
                                "Possibly, your lesson file is in the old format with no topic."
                                .format(p_spreadsheet_id))

            if len(column) >= 7:  # attachments
                if column[5] != '':
                    raise Exception("In lesson with spreadsheet ID {}, row 5 (points) should be empty if it's"
                                    "a materials.\n"
                                    "Please check.\n"
                                    "Possibly, your lesson file is in the old format with no topic."
                                    .format(p_spreadsheet_id))
                column_dict['attachments'] = get_attachments(column, 999)
            elif len(column) == 5:
                column_dict['attachments'] = []
            column_dict['topic'] = column[1]
            column_dict['title'] = column[2]
            column_dict['topic'] = column[1]
            column_dict['assignment_or_announcement'] = 'materials'
        else:
            raise Exception(f"In lesson with spreadsheet ID {p_spreadsheet_id}, something in row 2 has something other than "
                            f"'announcement' or 'assignment' or 'materials'.\n"
                            f"Type is this {column[0]} (should be announcement, assignment, or materials)"
                            f"and entire column is this: {column}"
                            f"If entire column is empty, then try to delete the contents of those columns")
        column_dict['text'] = column[4]
        column_dict['text'] = unicode_text(column[4])
        # print('fff final column ' + str(column_dict))
        column_dicts.append(column_dict)
    return column_dicts


# from generate_sheets_credential import generate_sheets_credential
# SPREADSHEET_ID = '1zR9dCyNOAikEFXJblvkkTqOUXQkNEm6CG4kIOBZApE4'  # Last day of school (D180)
# service_sheets = generate_sheets_credential()
# abc = read_lesson_plan(SPREADSHEET_ID, service_sheets)
# print(abc)

# from generate_sheets_credential import generate_sheets_credential
# SPREADSHEET_ID = '1Onx-EMOHveOXSO3bR4K6rMB4ovKYzeVdvYh04EnoS58' # AP CSP create task 1
# service_sheets = generate_sheets_credential()
# abc = read_lesson_plan(SPREADSHEET_ID, service_sheets)
# print(abc)
