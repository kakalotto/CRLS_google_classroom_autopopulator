import googleapiclient.errors
import configparser
from generate_sheets_credential import generate_sheets_credential
from generate_classroom_credential import generate_classroom_credential

SHEET_NAME = 'Courses'
print("Running create_courses.py")
config = configparser.ConfigParser()
config_filename = "google_classroom_tools.ini"
config.read(config_filename)
spreadsheet_id = config.get("CREATE_COURSES", "spreadsheet_id", fallback='')
print("Trying to read Google sheet with this spreadsheet ID: " + str(spreadsheet_id))

# Set up sheets service object
service_sheets = generate_sheets_credential()

# Set up classroom service object
service_classroom = generate_classroom_credential()

# Sample courses start at column C + D.  Real courses start at column E with a max of 12 courses.
for column in ['E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']:
    RANGE_NAME = SHEET_NAME + '!' + column + '3:' + column + '10'

    # Read course info
    result = service_sheets.spreadsheets().values().get(spreadsheetId=spreadsheet_id,
                                                        range=RANGE_NAME,
                                                        majorDimension='COLUMNS').execute()
    value = result.get('values', [])
    if not value:
        print("no value in this column " + str(column) + " no course here")
        continue   # no more courses
    elif len(value[0]) == 7:
        print(value[0])
        print("In column " + str(column) + " 9th row is populated - course already created")
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
        range_name = SHEET_NAME + '!' + column + '9'
        try:
            result = service_sheets.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=range_name,
                                                                   valueInputOption='USER_ENTERED', body=body).execute()
            print('{} cells in Google sheet with spreadsheetID {} updated with courseID {}.'
                  .format(result.get('updatedCells'), spreadsheet_id, course.get('id')))
        except googleapiclient.errors.HttpError:
            raise Exception("Possible errors.\n  Did you put in the correct spreadsheet?  Spreadsheet should be "
                            "something like '1xkcNN1OFmscODqz3zbDUqRbkHAxIuIyx-FtMfXgqczA'\n"
                            "Spreadsheet actually is {}.".format(spreadsheet_id))
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
