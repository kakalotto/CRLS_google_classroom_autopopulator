def return_perfect_scores(classname:str, classes_to_return:list):
    import time
    # from generate_classroom_credential import generate_classroom_credential
    from helper_functions.classroom_functions import class_name_2_id
    from generate_classroom_aspen_tools_credentials import generate_classroom_aspen_tools_credentials
    # Get the course ID

    services = generate_classroom_aspen_tools_credentials()
    service_classroom = services[0]

    course_id = class_name_2_id(service_classroom, classname)

    # get all assignments from Google classroom
    print(f"Getting all assignments from Google classroom for class {classname} id {course_id} ")
    assignments_id_dict = {}
    all_assignments = service_classroom.courses().courseWork().list(courseId=course_id).execute()
    if 'courseWork' in all_assignments:
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
                  f"{assignment}")
            assignments_id_dict[assignment['id']]['maxPoints'] = 500


    # loop over all assignments, skip if not in the classes_to_return list
    # Get all student works for that assignment.
    # if assignment is in the classes_to_return list, return everything perfect
    for key in assignments_id_dict.keys():
        # print(f"Trying this one now {key}, {assignments_id_dict[key]}")
        if assignments_id_dict[key]['title'] not in classes_to_return:
            continue

        student_work = service_classroom.courses(). \
            courseWork().studentSubmissions(). \
            list(courseId=course_id, courseWorkId=key).execute()
        if 'studentSubmissions' in student_work.keys():
            student_works = student_work['studentSubmissions']
            for work in student_works:
                if work.get('draftGrade') == assignments_id_dict[key]['maxPoints'] and\
                        work.get('state') == 'TURNED_IN':
                    print(f"The work to return  {assignments_id_dict[key]} {work}")
                    studentSubmission = {
                        'assignedGrade': work.get('draftGrade'),
                        'draftGrade': work.get('draftGrade'),
                    }
                    service_classroom.courses().courseWork().studentSubmissions().patch(
                        courseId=course_id, courseWorkId=key,id=work.get('id'),
                        updateMask='assignedGrade,draftGrade',
                        body = studentSubmission).execute()
                    time.sleep(2)
                    service_classroom.courses().courseWork().studentSubmissions().return_(courseId=course_id,
                                                                                          courseWorkId=key,
                                                                                           id=work.get('id')).execute()
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
