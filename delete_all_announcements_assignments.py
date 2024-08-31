from google.auth.exceptions import RefreshError

# from generate_sheets_credential import generate_sheets_credential
from generate_classroom_aspen_tools_credentials import generate_classroom_aspen_tools_credentials

# Get sheet service credential and service_classroom credential
try:
    [service_classroom, service_sheets, _] = generate_classroom_aspen_tools_credentials()
except RefreshError as error:
    raise Exception(f"Refresh error: {error}\n"
                    f"    Most likely problem: token expired.  Try to delete token_classroom_aspen_tools.json and "
                    f"re-authenticate. ")

course_id = 681197999730

course_id = 710120936540

assignments = service_classroom.courses().courseWork().list(courseId=course_id,
                                                            courseWorkStates='DRAFT').execute()
if 'courseWork' in assignments:
    assignments_list = assignments['courseWork']

    for assignment in assignments_list:
        print(assignment['id'])
        deletion = service_classroom.courses().courseWork().delete(courseId=course_id, id=assignment['id']).execute()

assignments = service_classroom.courses().courseWork().list(courseId=course_id,
                                                            courseWorkStates='PUBLISHED').execute()
if 'courseWork' in assignments:
    assignments_list = assignments['courseWork']

    # print(assignments_list)
    for assignment in assignments_list:
        print(assignment['id'])
        deletion = service_classroom.courses().courseWork().delete(courseId=course_id, id=assignment['id']).execute()


announcements = service_classroom.courses().announcements().list(courseId=course_id,
                                                                 announcementStates='DRAFT').execute()
print(announcements)
if 'announcements' in announcements:
    announcements_list = announcements['announcements']

    print(announcements_list)
    for announcements in announcements_list:
        print(announcements['id'])
        deletion = service_classroom.courses().announcements().\
            delete(courseId=course_id, id=announcements['id']).execute()


materials = service_classroom.courses().courseWorkMaterials().list(courseId=course_id,
                                                                   courseWorkMaterialStates='DRAFT').execute()
print("try for materials ")
print(materials)
if 'courseWorkMaterial' in materials:
    materials_list = materials['courseWorkMaterial']
    for material in materials_list:
        print(material['id'])
        deletion = service_classroom.courses().courseWorkMaterials().\
            delete(courseId=course_id, id=material['id']).execute()
else:
    print("no mateirals draft")


materials = service_classroom.courses().courseWorkMaterials().list(courseId=course_id,
                                                                   courseWorkMaterialStates='PUBLISHED').execute()
print("try for materials published ")
print(materials)
if 'courseWorkMaterial' in materials:
    materials_list = materials['courseWorkMaterial']

    for material in materials_list:
        print(material['id'])
        deletion = service_classroom.courses().courseWorkMaterials().\
            delete(courseId=course_id, id=material['id']).execute()
else:
    print("no mateirals published")
