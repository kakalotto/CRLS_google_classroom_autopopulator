
from generate_sheets_credential import generate_sheets_credential
from generate_classroom_credential import generate_classroom_credential

course_id = 36642186002
service_classroom = generate_classroom_credential()
assignments = service_classroom.courses().courseWork().list(courseId=course_id,
                                                            courseWorkStates='DRAFT').execute()
assignments_list = assignments['courseWork']

print(assignments_list)
for assignment in assignments_list:
    print(assignment['id'])
    deletion = service_classroom.courses().courseWork().delete(courseId=course_id, id=assignment['id']).execute()

announcements = service_classroom.courses().announcements().list(courseId=course_id,
                                                                 announcementStates='DRAFT').execute()
print(announcements)
announcements_list = announcements['announcements']

print(announcements_list)
for announcements in announcements_list:
    print(announcements['id'])
    deletion = service_classroom.courses().announcements().delete(courseId=course_id, id=announcements['id']).execute()