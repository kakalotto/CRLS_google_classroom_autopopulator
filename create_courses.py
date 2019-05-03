from generate_sheets_credential import generate_sheets_credential
from generate_classroom_credential import generate_classroom_credential

print("Running create_courses.py")
# Set up sheets service object
service_sheets = generate_sheets_credential()

SPREADSHEET_ID = '1xkcNN1OFmscODqz3zbDUqRbkHAxIuIyx-FtMfXgqczA' # AP CSP test
#SPREADSHEET_ID = '1RFSXj_IjfqVLv-njFmeI1e0LoVdglvFjQGxk1drxdqw'  # Game development

SHEET_NAME = 'Courses'

# Set up classroom service object
service_classroom = generate_classroom_credential()

# Sample courses start at column C + D.  Real courses start at column E with a max of 12 courses.
for column in ['E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']:
    RANGE_NAME = SHEET_NAME + '!' + column + '3:' + column + '9'

    # Read course info
    result = service_sheets.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                        range=RANGE_NAME,
                                                        majorDimension='COLUMNS').execute()
    value = result.get('values', [])
    if not value:
        continue   # no more courses
    elif len(value[0]) == 6:
        continue  # 6th row (courseID) is populated.  This means course already created.
    else:
        # Course hasn't been created yet.  Create it now.
        print("In create_courses.py, creating this course: " + str(value[0][0] + ' Section: ' + str(value[0][1])))
        course_name, course_section, course_description_heading, course_description, course_room = value[0]

        # Write course to Google classroom
        course = {
            'name': course_name,
            'section': course_section,
            'descriptionHeading': course_description_heading,
            'description': course_description,
            'room': course_room,
            'ownerId': 'me',
            'courseState': 'PROVISIONED'
        }
        course = service_classroom.courses().create(body=course).execute()
        print('Course created in Google Classroom, you will need to open Google classroom and click "Accept": {0} ({1})'
              .format(course.get('name'), course.get('id')))

        # Course created, write course ID into sheet
        values = [[course.get('id')]]
        body = {
            'values': values
        }
        RANGE_NAME = SHEET_NAME + '!' + column + '8'
        result = service_sheets.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
                                                               valueInputOption='USER_ENTERED', body=body).execute()
        print('{} cells in Google sheet with spreadsheetID {} updated with courseID {}.'
              .format(result.get('updatedCells'), SPREADSHEET_ID, course.get('id')))
