def missing_assignments_mailer(p_config_filename, p_gc_name, p_send_email=False,
                               p_teachercc='', p_message='', p_scholar_guardians='',
                               p_classes_students_dict={}, p_nicknames_dict={}, p_spreadsheet_id='',
                               p_sheet_id='', p_past_blurbs_dict={}, p_future_blurbs_dict={}):
    """
    Sends emails to students letting them know what assignments are missing
    :param p_config_filename: Name of the configuration filename (str)
    :param p_gc_name: Name of Google classroom to look  (string)
    :param p_send_email: Boolean whether to send email (Bool)
    :param p_teachercc: email address to cc on this class (string)
    :param p_message: Email message to append for this class (string)
    :param p_scholar_guardians: Dictionary of keys scholar emails, values guardian emails.
    :param p_classes_students_dict: dictionary from Maya's program giving student info emails, birthdays
    :param p_classes_students_dict: dictionary hard coded with nicknames
    :param p_spreadsheet_ids: list of spreadsheet ids
    :param p_sheet_ids: list of sheet ids
    :param p_past_blurbs_dict: dictionary of blurbs to fill in if we run into the past assignment
    :param p_future_blurbs_dict: dictionary of blurbs to fill in if we run into the future assignment

    :return: none
    """
    import datetime
    import re
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import base64
    from helper_functions.sheets_functions import read_course_daily_data_all, get_all_sheets
    from helper_functions.read_day_info import read_day_info

    from generate_missing_mailer_credential import generate_missing_mailer_credential
    # from generate_classroom_credential import generate_classroom_credential
    # from generate_gmail_credential import generate_gmail_credential
    from helper_functions.classroom_functions import class_name_2_id
    from helper_functions.quarters import which_quarter_today

    # Get the course ID
    service_list = generate_missing_mailer_credential()
    service_classroom = service_list[0]
    service_gmail = service_list[1]
    service_sheets = service_list[2]

    # print(f"service_gmail {service_gmail}")
    # print(f"service_classroom {service_classroom}")

    course_id = class_name_2_id(service_classroom, p_gc_name)

    # Find the right key from Maya's dict (and thus the students), given gc class name
    maya_this_class_students = []
    for aspen_class in p_classes_students_dict.keys():
        if p_classes_students_dict[aspen_class]['gc'] == p_gc_name:
            maya_this_class_students =  p_classes_students_dict[aspen_class]['students']

    print(f"iii this is the dictionary for this class from Maya's program! {maya_this_class_students}")

    # Get all of the emails from Maya's dictionary
    all_emails_in_aspen = []
    for student_dict in maya_this_class_students:
        all_emails_in_aspen.append(student_dict['email'])

    # Get students and student profiles from google classroom
    email_dict = {}
    print("Getting the names and student profiles from Google classroom")
    students = service_classroom.courses().students().list(courseId=course_id, ).execute()
    students = students['students']
    for student in students:
        student_id = student['userId']
        student_profiles = service_classroom.userProfiles().get(userId=student_id, ).execute()
        email_address = student_profiles['emailAddress']
        email_dict[student_id] = email_address
        print(f"Looping through students, got this email from classroom {email_address}")

    # get all assignments from Google classroom
    print("Getting all assignments from Google classroom")
    assignments_id_dict = {}
    all_assignments = service_classroom.courses().courseWork().list(courseId=course_id).execute()
    all_assignments = all_assignments['courseWork']
    for assignment in all_assignments:
        assignments_id_dict[assignment['id']] = assignment['title']

    # Create the messages to send to students.  Messages are lists of dictionaries
    today = datetime.datetime.now()
    quarter_start = which_quarter_today(p_filename=p_config_filename)
    messages = []
    maya_student_info_dict = {}
    for student in students:
        email_address = student['profile']['emailAddress']
        print(f"email {email_address} student from Google classroom {student}")

        for student_dict in maya_this_class_students:
            # print(f"inside {student_dict['email']} email {email_address}")
            if student_dict['email'] == email_address:
                print("Found!")
                caretaker_emails = student_dict['caretaker_emails']
                student_birthday = student_dict['birthday']
                student_name = student_dict['name']
                maya_student_info_dict[student_dict['email']] = {'caretaker_emails': caretaker_emails,
                                                    'student_birthday': student_birthday,
                                                    'student_name': student_name}
                break
        if email_address not in maya_student_info_dict.keys():
            print(f"Did not find this student {email_address} not in aspen? continue ")
            continue

        if student['profile']['emailAddress'] not in all_emails_in_aspen:
            print(f"this student {student['profile']['emailAddress']} was in google classroom but not in aspen, skipping {student['profile']['emailAddress']}")
            print(f"{all_emails_in_aspen}")
            continue
        student_id = student['userId']
        message_dict = {student_id: ''}
        if student_id in email_dict:
            print("Creating email message for this student ID: " + str(student_id) +
                  "   this student" + email_dict[student_id])
            student_work = service_classroom.courses(). \
                courseWork().studentSubmissions(). \
                list(courseId=course_id, courseWorkId='-', userId=student_id).execute()
            student_work = student_work['studentSubmissions']
            for work in student_work:
                if 'late' in work:
                    work_id = work['courseWorkId']
                    due_date = {}
                    for assignment in all_assignments:
                        if work_id == assignment['id']:
                            due_date = assignment['dueDate']
                    if work['state'] != 'TURNED_IN' and work['late'] is True and due_date:
                        due_date = datetime.datetime(due_date['year'], due_date['month'], due_date['day'])
                        if today >= due_date > quarter_start:
                            link = work['alternateLink']
                            coursework_id = work['courseWorkId']
                            message_dict[student_id] += "assignment:  {} \nlink to assignment {}\n\n".format(
                                assignments_id_dict[coursework_id], link)
                elif 'state' in work.keys():
                    # print(f"potentially returned {work}")
                    if work['state'] == 'RETURNED' and 'assignedGrade' not in work.keys():
                        work_id = work['courseWorkId']
                        due_date = {}
                        for assignment in all_assignments:
                            if work_id == assignment['id']:
                                due_date = assignment['dueDate']
                        if due_date:
                            due_date = datetime.datetime(due_date['year'], due_date['month'], due_date['day'])
                            if today >= due_date > quarter_start:
                                link = work['alternateLink']
                                coursework_id = work['courseWorkId']
                                message_dict[
                                    student_id] += "Returned assignment that needs attention:  {} \nlink to assignment {}\n\n".format(
                                    assignments_id_dict[coursework_id], link)
        messages.append(message_dict)
    print(f"Maya info dict {maya_student_info_dict}")

    # generate info about what is going on in class
    today_obj = datetime.date.today()
    six_days_obj = datetime.timedelta(days=6)
    seven_days_obj = datetime.timedelta(days=7)
    one_week_previous_obj = today_obj - six_days_obj
    one_week_future_obj = today_obj + seven_days_obj
    print(f"today {today_obj} and 1 week prev {one_week_previous_obj} and 1 week future {one_week_future_obj}")
    print(f"reading in this spreadsheet-id {p_spreadsheet_id} and this sheet {p_sheet_id}")
    values = read_course_daily_data_all(p_spreadsheet_id, p_sheet_id, service_sheets)

    # Find index of today
    for i, row in enumerate(values, 1):
        day_info = read_day_info(row)
        this_date_obj = datetime.datetime.strptime(day_info['date'], '%m/%d/%Y')
        this_date_obj = this_date_obj.date()
        print(f"this day obj {this_date_obj}")
        if this_date_obj == today_obj:
            today_index = i
            print(f"it is today!!!! {today_index}")
    # Find index of 6 days ago
    for i, row in enumerate(values, 1):
        day_info = read_day_info(row)
        this_date_obj = datetime.datetime.strptime(day_info['date'], '%m/%d/%Y')
        this_date_obj = this_date_obj.date()
        print(f"this day obj {this_date_obj}")
        if this_date_obj > one_week_previous_obj:
            one_week_previous_index = i
            print(f"index of 6 days ago is today!!!! {one_week_previous_index}")
            break
    # Find index of future
    for i, row in enumerate(values, 1):
        day_info = read_day_info(row)
        this_date_obj = datetime.datetime.strptime(day_info['date'], '%m/%d/%Y')
        this_date_obj = this_date_obj.date()
        print(f"this day obj {this_date_obj}")
        if this_date_obj == one_week_future_obj:
            one_week_future_index = i
            print(f"future is today!!!! {one_week_future_index}")

    # get info for each of the days
    counter = one_week_previous_index - 1
    print(f"values ")
    print(values)
    assignments = []
    while counter < today_index:
        row = values[counter]
        print(row)
        todays_assignments_string = row[3]
        todays_assignments_list = todays_assignments_string.split('and')
        assignments.extend(todays_assignments_list)
        print(f"assignments {assignments}, todays_assignments_list {todays_assignments_list}, todays_string {todays_assignments_string}")
        counter = counter + 1
    new_assignments = []
    for assignment in assignments:
        temp_assignment = re.sub(r'^\s+','', assignment)
        temp_assignment = re.sub(r'\s+$','', temp_assignment)
        new_assignments.append(temp_assignment)
    print(f"Here are the stripped spaces {new_assignments}")
    assignments = new_assignments


    # future assignments
    counter = today_index
    future_assignments = []
    while counter < one_week_future_index:
        row = values[counter]
        print(row)
        todays_assignments_string = row[3]
        todays_assignments_list = todays_assignments_string.split('and')
        future_assignments.extend(todays_assignments_list)
        # print(f"assignments {assignments}, todays_assignments_list {todays_assignments_list}, todays_string {todays_assignments_string}")
        counter = counter + 1
    new_future_assignments = []
    for future_assignment in future_assignments:
        temp_assignment = re.sub(r'^\s+','', future_assignment)
        temp_assignment = re.sub(r'\s+$','', temp_assignment)
        new_future_assignments.append(temp_assignment)
    print(f"Here are the stripped spaces {new_future_assignments}")
    future_assignments = new_future_assignments

    # Getting Birthday info now
    print('looking for birthdays')
    birthday_names = []

    for student_dict in maya_this_class_students:
        birthday = student_dict['birthday']
        birthday_obj = datetime.datetime.strptime(birthday, '%m/%d/%Y')
        birthday_obj = birthday_obj.date()
        current_year = datetime.datetime.now().year
        print(f'current year {current_year}')
        birthday_obj = birthday_obj.replace(year=current_year)
        print(f"birthday dates {one_week_previous_obj} {birthday_obj} {today_obj}")
        if one_week_previous_obj <= birthday_obj <= today_obj:
            name = student_dict['name']
            email = student_dict['email']
            print(f"birthday found! {name} student dict {student_dict}")
            if email in p_nicknames_dict.keys():
                birthday_names.append(p_nicknames_dict[email])
            else:
                name_list = name.split()
                first_name = name_list[0]
                birthday_names.append(first_name)
    print(f"birthday names {birthday_names}" )
    birthday_string = ''
    if len(birthday_names) > 0:
        birthday_string = 'This week, we wish Happy Birthday to ' + birthday_names[0]
        if len(birthday_names) > 1:
            for name in birthday_names[1:]:
                birthday_string = birthday_string + ' and ' + name
        birthday_string = birthday_string + '!'
    print(f"birthday string! {birthday_string}")

    print("starting blurb writing now")
    blurb = ''
    for assignment in assignments:
        print(f"assignment {assignment} p_past_blurbs {p_past_blurbs_dict}")
        if assignment in p_past_blurbs_dict.keys():
            blurb = blurb + p_past_blurbs_dict[assignment] + '\n'
            print(f"found something now! {blurb}")

    if blurb:
        blurb = "This past week,\n" + blurb
        blurb = blurb + '\n'
    for future_assignment in future_assignments:
        if future_assignment in p_future_blurbs_dict.keys():
            blurb = blurb + p_future_blurbs_dict[future_assignment] + '\n'


    print("SEND EMAIL IS THIS" + str(p_send_email))
    for message in messages:
        for key in message:
            email_address = email_dict[key]
            # print("This person " + str(email_address) + " is missing these (past due) assignments ")
            name = maya_student_info_dict[email_address]['student_name']
            name_list = name.split()
            # print(f'name is this {name} and name_list is this {name_list}' )
            if email_address in p_nicknames_dict.keys():
                print("NAME REPLACEMENT FROM THE DICTIONARY")
                first_name = p_nicknames_dict[email_address]
            else:
                first_name = name_list[0]
            if not message[key]:
                message[key] = 'You have everything turned in that is due.  Great work!'
            else:
                message[key] = "Here are assignments that are past due that are not turned in yet:\n\n" + \
                               message[key]


            # message[key] = email_address + '\n' + message[key]
            message[key] = 'Hello ' + first_name + ' and ' + first_name + "'s caretakers! \n\n" + \
                           blurb + "\n" + birthday_string + '\n' + p_message + '\n\n' + message[key]
            # message[key] += '\n\nThis is an automated email\n\n'

            # Debug info here
            # if email_address in p_scholar_guardians.keys():
            #     print("Email address to send to: " + email_address + ',' +
            #           p_scholar_guardians[email_address])
            # else:
            #     print("Email address to send to: " + email_address)
            if p_teachercc:
                print("teacher cc: " + str(p_teachercc))
            else:
                print("no teacher cc")
            print("This is the message that will be/would have been sent:")
            print(message[key])
            msg_text = message[key]

            if p_send_email:
                email_message = MIMEMultipart()
                if email_address in p_scholar_guardians.keys():
                    if len(maya_student_info_dict[email_address]['caretaker_emails']) == 2:
                        caretaker_string = maya_student_info_dict[email_address]['caretaker_emails'][0] + ',' + \
                                           maya_student_info_dict[email_address]['caretaker_emails'][1]
                    else:
                        caretaker_string = maya_student_info_dict[email_address]['caretaker_emails'][0]
                    email_message['to'] = email_address + ',' + caretaker_string
                # else:
                #     email_message['to'] = email_address
                if p_teachercc:
                    email_message['cc'] = p_teachercc
                email_message['subject'] = p_gc_name + '  assignments report'
                email_message.attach(MIMEText(msg_text, 'plain'))
                raw_string = base64.urlsafe_b64encode(email_message.as_bytes()).decode()
                send_message = service_gmail.users().messages().send(userId='me', body={'raw': raw_string}).execute()
                print(send_message)
            else:
                print("send_message was sent to 0.  Emails were not sent.\n"
                      "To send emails, switch send_email to 1 in this file: " + str(p_config_filename) + "\n\n")

