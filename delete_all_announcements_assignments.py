
from generate_sheets_credential import generate_sheets_credential
from generate_classroom_credential import generate_classroom_credential

course_id = 36512536321
service_classroom = generate_classroom_credential()
assignments = service_classroom.courses().courseWork().list(courseId=course_id,).execute()

print(assignments)