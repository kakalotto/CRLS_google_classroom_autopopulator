import googleapiclient

from generate_sheets_credential import generate_sheets_credential
from generate_classroom_credential import generate_classroom_credential

print("Running create_courses.py")
# Set up sheets service object
service_sheets = generate_sheets_credential()


#SPREADSHEET_ID = '1uEmlRJjqEpsCj6wew44meJv3af0WQ7VRQFE4x-QU9FQ' # AP CSP test
#SPREADSHEET_ID = '1RFSXj_IjfqVLv-njFmeI1e0LoVdglvFjQGxk1drxdqw'  # Game development
#SPREADSHEET_ID = '1o_YPtSYB75fk9-r79GhNVqTDdkWr0VZA497nrC4r1h0' # ICS 2021
#SPREADSHEET_ID = '1HqwVlxXu-l1KCatU8lnYb9xD97djeA3BkO448K5HADk' # testing
#SPREADSHEET_ID = '1x0buDsw6pBjK1GJkZXc5mMo86dX7FnWj4daMn_5CyLc' # 2021 IT2/IT3
#SPREADSHEET_ID = '1ZenTcQlCQhbYvBvPOVq8XIB2FQgseIGHH4gTBTcw-KY' # 2021 level 1
#SPREADSHEET_ID = '1xkcNN1OFmscODqz3zbDUqRbkHAxIuIyx-FtMfXgqczA' # AP CSP test
#SPREADSHEET_ID = '1RFSXj_IjfqVLv-njFmeI1e0LoVdglvFjQGxk1drxdqw'  # Game development
#SPREADSHEET_ID = '1NmV9WVSJsVrrJIVRKat4oWnkWMBWCEuO-07eCesh4ow' # 2020 level 1
SPREADSHEET_ID = '1HBh9DcDUaKiyH_X5w_-qCh-Aw_0JZD-Rtzg_PfiER3Y' # 2020 level 1

SHEET_NAME = 'Courses'


# Set up classroom service object
service_classroom = generate_classroom_credential()

# Sample courses start at column C + D.  Real courses start at column E with a max of 12 courses.
for column in ['E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']:
    RANGE_NAME = SHEET_NAME + '!' + column + '3:' + column + '10'

    # Read course info
    result = service_sheets.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                        range=RANGE_NAME,
                                                        majorDimension='COLUMNS').execute()
    value = result.get('values', [])
    if not value:
        continue   # no more courses
    elif len(value[0]) == 7:
        continue  # 7th row (courseID) is populated.  This means course already created.
    else:
        # Course hasn't been created yet.  Create it now.
        print("In create_courses.py, creating this course: " + str(value[0][0] + ' Section: ' + str(value[0][1])))
        course_name, course_section, course_description_heading, course_description, course_room, _ = value[0]

        # Write course to Google classroom
        course = {
            'name': course_name,
            'section': course_section,
            'descriptionHeading': course_description_heading,
            'description': course_description,
            'room': course_room,
            'ownerId': 'me',
            'courseState': 'ACTIVE'
        }
        course = service_classroom.courses().create(body=course).execute()
        print('Course created in Google Classroom: {} ({})'
              .format(course.get('name'), course.get('id')))

        # Course created, write course ID into sheet
        values = [[course.get('id')]]
        body = {
            'values': values
        }
        RANGE_NAME = SHEET_NAME + '!' + column + '9'
        try:
            result = service_sheets.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
                                                               valueInputOption='USER_ENTERED', body=body).execute()
            print('{} cells in Google sheet with spreadsheetID {} updated with courseID {}.'
                  .format(result.get('updatedCells'), SPREADSHEET_ID, course.get('id')))
        except googleapiclient.errors.HttpError:
            raise Exception("Possible errors.\n  Did you put in the correct spreadsheet?  Spreadsheet should be "
                            "something like '1xkcNN1OFmscODqz3zbDUqRbkHAxIuIyx-FtMfXgqczA'\n"
                            "Spreadsheet actually is {}.".format(SPREADSHEET_ID))
        # Topics
        topics = value[0][5].split(',')
        course_id = course.get('id')
        for topic in topics:
            body = {"name": topic}
            try:
                result = service_classroom.courses().topics().create(
                    courseId=course_id,
                    body=body).execute()
                print('In course id {}, with course name {}, created topic {}'.format(course_id, value[0][1], topic))
            except googleapiclient.errors.HttpError:
                raise Exception("Possible errors.\n  If 'requested entity already exists', maybe already have topic {}."
                                "\n If 'requested entity not found', then the course id {} may not exist.\n)."
                    .format(topic, values))


