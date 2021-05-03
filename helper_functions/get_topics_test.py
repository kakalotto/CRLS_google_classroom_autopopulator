from generate_classroom_credential import generate_classroom_credential


service_classroom = generate_classroom_credential()
course_id = 234359485686



assignment = service_classroom.courses().topics().list(courseId=course_id).execute()
print(assignment)