def missing_assignments_mailer(p_config_filename, p_gc_name, p_send_email=False,
                               p_teachercc='', p_message='', p_scholar_guardians=''):
    """
    Sends emails to students letting them know what assignments are missing
    :param p_config_filename: Name of the configuration filename (str)
    :param p_gc_name: Name of Google classroom to look through (string)
    :param p_send_email: Boolean whether to send email (Bool)
    :param p_teachercc: email address to cc on this class (string)
    :param p_message: Email message to append for this class (string)
    :param p_scholar_guardians: Dictionary of keys scholar emails, values guardian emails.
    :return: none
    """
    import datetime
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import base64

    from generate_ro_classroom_credential import generate_ro_classroom_credential
    from generate_gmail_credential import generate_gmail_credential
    from helper_functions.classroom_functions import class_name_2_id
    from helper_functions.quarters import which_quarter_today

    # Get the course ID
    service_classroom = generate_ro_classroom_credential()
    course_id = class_name_2_id(service_classroom, p_gc_name)

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
        print(email_address)
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
    for student in students:
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
        messages.append(message_dict)

    if p_send_email:
        service_gmail = generate_gmail_credential()

    print("SEND EMAIL IS THIS" + str(p_send_email))
    for message in messages:
        for key in message:
            email_address = email_dict[key]
            print("This person " + str(email_address) + " is missing these (past due) assignments ")
            if not message[key]:
                message[key] = 'Nothing! You have everything turned in that is due.  Great work!'
            else:
                message[key] = "Hello! Here are assignments that are past due that are not turned in yet:\n\n" + \
                               message[key]
            message[key] = email_address + '\n' + message[key]

            message[key] += "\n\n" + p_message

            message[key] += '\n\nThis is an automated email\n\n'
            print("This is the message that will be/would have been sent:")
            print(message[key])
            msg_text = message[key]

            if p_send_email:
                email_message = MIMEMultipart()
                if email_address in p_scholar_guardians.keys():
                    email_message['to'] = email_address + ',' + p_scholar_guardians[email_address]
                else:
                    email_message['to'] = email_address
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
