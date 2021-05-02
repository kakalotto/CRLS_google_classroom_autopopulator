from generate_classroom_credential import generate_classroom_credential


service_classroom = generate_classroom_credential()
course_id = 234359485686
assignment_id = 234375208396

assignments = service_classroom.courses().courseWork().list(courseId=course_id,courseWorkStates='DRAFT').execute()
assignments = assignments['courseWork']
print(assignments)
for assignment in assignments:
    print(assignment['title'])
#
# courseworks = service_classroom.courses().courseWork().list(courseId=course_id).execute()
#
#     #.get('courseWork', [])
# print(courseworks)
#
#
# assignment = service_classroom.courses().courseWork().get(courseId=course_id, id=assignment_id).execute()
# print(assignment)
#
#
#
# assignment = service_classroom.courses().courseWork().list(courseId=course_id).execute()
# print(assignment)