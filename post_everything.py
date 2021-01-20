import re
import datetime
from generate_sheets_credential import generate_sheets_credential
from generate_classroom_credential import generate_classroom_credential

course_id = 234297641199
service_classroom = generate_classroom_credential()

assignments = service_classroom.courses().courseWork().list(courseId=course_id,
                                                            courseWorkStates='DRAFT').execute()
assignments_list = assignments['courseWork']

print(assignments_list)
for assignment in assignments_list:

    if assignment['state'] == 'DRAFT':
        assignment_id = assignment['id']
        print("THIS IS THE INFO!")
        print(assignment['id'])
        print(assignment)

        #now_plus_1 = datetime.datetime.utcnow().isoformat() + 'Z'
        now = datetime.datetime.utcnow()
        now_plus_1 = now + datetime.timedelta(minutes=1)
        now_plus_1 = now_plus_1.isoformat()
        now_plus_1 = str(now_plus_1)
        now_plus_1 = re.sub(r'\.[0-9]+$', '', now_plus_1)
        now_plus_1 = now_plus_1 + 'Z'
        print(now_plus_1)
        #
        update = {'scheduledTime': now_plus_1
                  }
        updater = service_classroom.courses().courseWork().patch(courseId=course_id,
                                                                 id=assignment_id,
                                                                 updateMask='scheduledTime',
                                                                 body=update).execute()


materials= service_classroom.courses().\
    courseWorkMaterials().list(courseId=course_id,courseWorkMaterialStates='DRAFT').execute()
materials_list = materials['courseWorkMaterial']

print(materials_list)
for material in materials_list:

    if material['state'] == 'DRAFT':
        material_id = material['id']
        print("THIS IS THE INFO!")
        print(material['id'])
        print(material)

        #now_plus_1 = datetime.datetime.utcnow().isoformat() + 'Z'
        now = datetime.datetime.utcnow()
        now_plus_1 = now + datetime.timedelta(minutes=1)
        now_plus_1 = now_plus_1.isoformat()
        now_plus_1 = str(now_plus_1)
        now_plus_1 = re.sub(r'\.[0-9]+$', '', now_plus_1)
        now_plus_1 = now_plus_1 + 'Z'
        print(now_plus_1)
        #
        update = {'scheduledTime': now_plus_1
                  }
        updater = service_classroom.courses().courseWorkMaterials().patch(courseId=course_id,
                                                                          id=material_id,
                                                                          updateMask='scheduledTime',
                                                                          body=update).execute()
