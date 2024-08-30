import googleapiclient.errors
from google.auth.exceptions import RefreshError

import configparser
import re
from generate_classroom_aspen_tools_credentials import generate_classroom_aspen_tools_credentials
SHEET_NAME = 'Courses'
print("Running create_courses.py")
config = configparser.ConfigParser()
config_filename = "crls_teacher_tools.ini"
config.read(config_filename)
spreadsheet_id = config.get("CREATE_COURSES", "spreadsheet_id", fallback='')
print("Trying to read Google sheet with this spreadsheet ID: " + str(spreadsheet_id))
provision_status = config.get("CREATE_COURSES", "provisioned", fallback='PROVISIONED')


# Set up sheets service object
try:
    [service_classroom, service_sheets, service_docs] = generate_classroom_aspen_tools_credentials()
# except:
except RefreshError as error:
    raise Exception(f"Refresh error: {error}\n"
                    f"    Most likely problem: token expired.  Try to delete token_classroom_aspen_tools.json and "
                    f"re-authenticate. ")

classes_created = 0
# Sample courses start at column C + D.  Real courses start at column E with a max of 12 courses.
for column in ['E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']:
    RANGE_NAME = SHEET_NAME + '!' + column + '3:' + column + '10'

    # Read course info
    try:
        result = service_sheets.spreadsheets().values().get(spreadsheetId=spreadsheet_id,
                                                            range=RANGE_NAME,
                                                            majorDimension='COLUMNS').execute()
    except googleapiclient.errors.HttpError as error:
        raise Exception(f"Crashed trying to read spreadsheet column {column}. Error.\n"
                        f"Here is the error: {error}\n"
                        f"'requested entity not found':\n"
                        f"   Did you put in the correct spreadsheet?  Spreadsheet should be "
                        f"   something like '1xkcNN1OFmscODqz3zbDUqRbkHAxIuIyx-FtMfXgqczA'\n"
                        f"   Spreadsheet we tried to read is this: {spreadsheet_id}.\n"
                        f"   If you read a nonexistent spreadsheet, it will say something like this"
                        f" .\n"
                        f"'The caller does not have permission'\n"
                        f"  Check that your spreadsheet is shared with same user as the token owner.\n"
                        f"  Check that it's not the wrong spreadshheet")

    value = result.get('values', [])
    if not value:
        # print("no value in this column " + str(column) + " no course here")
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
            'courseState': provision_status
        }
        try:
            course = service_classroom.courses().create(body=course).execute()
            print('Course created in Google Classroom: {} ({})'
                  .format(course.get('name'), course.get('id')))
            classes_created = classes_created + 1
        except googleapiclient.errors.HttpError as error:
            raise Exception(f"Crashed.  Error is this: {error}\n")

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
        except googleapiclient.errors.HttpError as error:
            raise Exception(f"Crashed.  Error is this: {error}\n"
                            f"Possible errors.\n  Did you put in the correct spreadsheet?  Spreadsheet should be "
                            f"something like '1xkcNN1OFmscODqz3zbDUqRbkHAxIuIyx-FtMfXgqczA'\n"
                            f"Spreadsheet actually is {spreadsheet_id}.")
        # Topics
        topics = value[0][5].split(',')
        course_id = course.get('id')

        for topic in topics:
            topic2 = re.sub(r'\s+', '', topic, re.X | re.M | re.S)
            if topic2 != topic:
                print("Removed leading spaces in topic (separate topics by comma, not by comma space)")
                topic = topic2
            body = {"name": topic}
            try:
                result = service_classroom.courses().topics().create(
                    courseId=course_id,
                    body=body).execute()
                print(f'In course id {course_id}, with course name {value[0][1]}, created topic {topic}')
            except googleapiclient.errors.HttpError as error:
                raise Exception(f"Crashed.  Error is this: {error}\n"
                                f"Possible errors.\n  If 'requested entity already exists', "
                                f"maybe already have topic {topic}, and you tried to make another topic with the same "
                                f"name."
                                f"\n If 'requested entity not found', then the course id {values} may not exist.\n).")

print(f"Created this many classes: {classes_created}")