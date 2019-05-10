
from generate_sheets_credential import generate_sheets_credential
from generate_classroom_credential import generate_classroom_credential

course_id = 36577460997
service_classroom = generate_classroom_credential()
assignments = service_classroom.courses().courseWork().list(courseId=course_id,).execute()
assignments_list = assignments['courseWork']

print(assignments_list)
for assignment in assignments_list:
    print(assignment['id'])
    deletion = service_classroom.courses().courseWork().delete(courseId=course_id, id=assignment['id']).execute()