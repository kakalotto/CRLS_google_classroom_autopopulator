
from generate_sheets_credential import generate_sheets_credential
from generate_classroom_credential import generate_classroom_credential

course_id = 234071686740



service_classroom = generate_classroom_credential()
assignments = service_classroom.courses().courseWork().list(courseId=course_id,
                                                            courseWorkStates='DRAFT').execute()
assignments_list = assignments['courseWork']

print(assignments_list)
for assignment in assignments_list:

    if assignment['state'] == 'DRAFT':
        print(assignment['id'])
        assignment_id = assignment['id']
        print(assignment)
        update = {'state': 'PUBLISHED'
                  }
        assignment = service_classroom.courses().courseWork().patch(courseId=course_id,
                                                                      id=assignment_id,
                                                                      updateMask='state',
                                                                      body=update).execute()

       # post = service_classroom.courses().courseWork().patch(courseId=course_id, id=assignment['id']).execute()
#
# announcements = service_classroom.courses().announcements().list(courseId=course_id,
#                                                                  announcementStates='DRAFT').execute()
# print(announcements)
# announcements_list = announcements['announcements']
#
# print(announcements_list)
# for announcements in announcements_list:
#     print(announcements['id'])
#     deletion = service_classroom.courses().announcements().delete(courseId=course_id, id=announcements['id']).execute()