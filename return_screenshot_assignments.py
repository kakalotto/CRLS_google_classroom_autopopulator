def return_screenshot_assignments(classname:str, classes_to_return:list):
    import time
    import re
    # from generate_classroom_credential import generate_classroom_credential
    from helper_functions.classroom_functions import class_name_2_id
    from generate_classroom_aspen_tools_credentials import generate_classroom_aspen_tools_credentials
    # Get the course ID

    services = generate_classroom_aspen_tools_credentials()
    service_classroom = services[0]

    # Get the course ID
    # service_classroom = generate_classroom_credential()
    course_id = class_name_2_id(service_classroom, classname)

    # get all assignments from Google classroom
    print(f"Getting all assignments from Google classroom for class {classname} id {course_id} ")
    assignments_id_dict = {}
    all_assignments = service_classroom.courses().courseWork().list(courseId=course_id).execute()
    all_assignments = all_assignments['courseWork']

    # loop over all assignments to get titles (assignment names) and perfect scores (maxPoints)
    for assignment in all_assignments:
        # print(f"This is assignment {assignment}")
        assignments_id_dict[assignment['id']] = assignment['title']
        assignments_id_dict[assignment['id']] = {'title': assignment['title']}
        if 'maxPoints' in assignment.keys():
            assignments_id_dict[assignment['id']]['maxPoints'] = assignment['maxPoints']
        else:
            print(f"This assignment does not have maxpoints!"
                  "{assignment}")
            assignments_id_dict[assignment['id']]['maxPoints'] = 500

    # loop over all assignments, skip if not in the classes_to_return list
    # Get all student works for that assignment.
    # if assignment is in the classes_to_return list, return everything perfect
    print("looping over assignments to find a match")
    print(f"Here is the dictionary to try {assignments_id_dict}")
    for key in assignments_id_dict.keys():
        # print(f"Trying this one now {key}, {assignments_id_dict[key]}")
        if assignments_id_dict[key]['title'] not in classes_to_return:
            # print(f" {assignments_id_dict[key]['title']} is not in {classes_to_returns not} ")
            continue
        #print(f"Trying this one now {key}, {assignments_id_dict[key]}")

        student_work = service_classroom.courses(). \
            courseWork().studentSubmissions(). \
            list(courseId=course_id, courseWorkId=key).execute()
        if 'studentSubmissions' in student_work.keys():
            student_works = student_work['studentSubmissions']
            for work in student_works:
                # print(work)
                if work.get('state') == 'TURNED_IN':
                    if 'assignmentSubmission' in work.keys():
                        attachments = work['assignmentSubmission']['attachments']
                        for attachment in attachments:
                            print(attachment)
                            drivefile_title = attachment['driveFile']['title']
                            if re.search('[Jj][Pp][Ee][Gg]$', drivefile_title, re.X | re.M | re.S) or \
                               re.search('[Jj][Pp][Gg]$', drivefile_title, re.X | re.M | re.S) or \
                               re.search('[Pp][Nn][Gg]$', drivefile_title, re.X | re.M | re.S) :
                                # print("READY!")
                                studentSubmission = {
                                    'assignedGrade': assignments_id_dict[key]['maxPoints'],
                                    'draftGrade': assignments_id_dict[key]['maxPoints'],
                                }
                                service_classroom.courses().courseWork().studentSubmissions().patch(
                                    courseId=course_id, courseWorkId=key,id=work.get('id'),
                                    updateMask='assignedGrade,draftGrade',
                                    body = studentSubmission).execute()
                                time.sleep(2)
                                service_classroom.courses().courseWork().studentSubmissions().return_(courseId=course_id,
                                                                                                      courseWorkId=key,
                                                                                                      id=work.get('id')).execute()
                                break


        #
        #             if work.get('draftGrade') and work.get('state') == 'TURNED_IN':
        #             if work.get('draftGrade') and work.get('id') == 'Cg0IjZSL6icQ8rb5zo4T':

                    # print(f"This is the draft grade! {work.get('draftGrade')} and the max {assignments_id_dict[key]['maxPoints']}"
                    #       f"and the assignment name  {assignments_id_dict[key]['title']} and"
                    #       f"id for thie work {work.get('id')}"
                    #       f"and the work {work}"
                    #       f"and the courseid {course_id}"
                    #       f"and the assignment id {key}")
                    # print(f"coureID {course_id} courseworkID {key} id {work.get('id')}" )
