def thirty_days_fifty(classname:str):
    import time
    from generate_classroom_credential import generate_classroom_credential
    from helper_functions.classroom_functions import class_name_2_id
    import re
    import time
    import datetime
    import math
    from googleapiclient.errors import HttpError
    # Get the course ID
    service_classroom = generate_classroom_credential()
    course_id = class_name_2_id(service_classroom, classname)

    # get all assignments from Google classroom
    print(f"Getting all assignments from Google classroom for class {classname} id {course_id} ")
    assignments_id_dict = {}
    all_assignments = service_classroom.courses().courseWork().list(courseId=course_id).execute()
    all_assignments = all_assignments['courseWork']

    # loop over all assignments to get titles (assignment names) and perfect scores (maxPoints)
    for assignment in all_assignments:
        # print(f"This is assignment {assignment} and due_date {assignment['dueDate']}")
        if 'dueDate' not in assignment.keys():
            print(f"ERROR: This is assignment has not due date, skipping: bf{assignment} ")
            continue
        python_due_date = datetime.datetime(int(assignment['dueDate']['year']), int(assignment['dueDate']['month']),
                                            int(assignment['dueDate']['day']))
        thirtyfive_days = datetime.timedelta(days=35)
        if python_due_date + thirtyfive_days < datetime.datetime.now():
        # gt the due duate
            assignments_id_dict[assignment['id']] = assignment['title']
            if re.search(r':-\)', assignments_id_dict[assignment['id']] , re.X | re.M | re.S):
                continue

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
        if 'title' not in assignments_id_dict[key]:
            continue
        # assignment = assignments_id_dict[key]['title']

        print(f"Trying this one now {key}, {assignments_id_dict[key]} in this class: {classname}")
        # time.sleep(60)
        student_work = service_classroom.courses(). \
            courseWork().studentSubmissions(). \
            list(courseId=course_id, courseWorkId=key).execute()
        # # print(student_work)
        if 'studentSubmissions' in student_work.keys():
            student_works = student_work['studentSubmissions']
            for work in student_works:
                if work['state'] != 'CREATED':
                    continue
                if 'draftGrade' in work.keys():
                    continue
                print(f"Giving this one a 50% f{work}")
                grade = math.ceil(assignments_id_dict[key]['maxPoints']/2.0)
                studentSubmission = {
                    'assignedGrade': grade,
                    'draftGrade': grade,
                }
                # print(grade)

                try:
                    service_classroom.courses().courseWork().studentSubmissions().patch(
                        courseId=course_id, courseWorkId=key, id=work.get('id'),
                        updateMask='assignedGrade,draftGrade',
                        body=studentSubmission).execute()
                except HttpError as e:
                    error_reason = e.reason
                    error_details = e.error_details
                    print(f"Error! Reason is this: {error_reason} and details are these: {error_details}")

                # service_classroom.courses().courseWork().studentSubmissions().return_(courseId=course_id,
                #                                                                       courseWorkId=key,
                #                                                                       id=work.get('id')).execute()
                # time.sleep(60)

        #         if work.get('draftGrade') == assignments_id_dict[key]['maxPoints'] and\
        #                 work.get('state') == 'TURNED_IN':
        #             print(f"The work to return  {assignments_id_dict[key]} {work}")
        #             studentSubmission = {
        #                 'assignedGrade': work.get('draftGrade'),
        #                 'draftGrade': work.get('draftGrade'),
        #             }
        #             service_classroom.courses().courseWork().studentSubmissions().patch(
        #                 courseId=course_id, courseWorkId=key,id=work.get('id'),
        #                 updateMask='assignedGrade,draftGrade',
        #                 body = studentSubmission).execute()
        #             time.sleep(2)
        #             service_classroom.courses().courseWork().studentSubmissions().return_(courseId=course_id,
        #                                                                                   courseWorkId=key,
        #                                                                                    id=work.get('id')).execute()
        #
        #             if work.get('draftGrade') and work.get('state') == 'TURNED_IN':
        #             if work.get('draftGrade') and work.get('id') == 'Cg0IjZSL6icQ8rb5zo4T':

