import base64
import datetime

from generate_gmail_credential import generate_gmail_credential
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from generate_classroom_credential import generate_classroom_credential

def create_message(sender, to, subject, message_text):
    """Create a message for an email.

      Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.

      Returns:
        An object containing a base64url encoded email object.
      """
    import base64
    from email.mime.text import MIMEText

    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string())}


course_id = 247697843639
service_classroom = generate_classroom_credential()


student_dict = {'21nlei@cpsd.us': '103026788979009218908',
                '21atekieteklemariam@cpsd.us': 102189211805773929897}

'''

{'id': '108001275956982622720', 'name': {'givenName': 'AMEIR', 'familyName': 'DAWSON', 'fullName': 'AMEIR DAWSON'}}
{'id': '108001275956982622720', 'name': {'givenName': 'ZOE', 'familyName': 'SIEGELNICKEL', 'fullName': 'ZOE SIEGELNICKEL'}}
{'id': '103072792655643970842', 'name': {'givenName': 'THEODORE', 'familyName': 'WOODWARD', 'fullName': 'THEODORE WOODWARD'}}
{'id': '108395054813353959432', 'name': {'givenName': 'LONSO', 'familyName': 'IRR', 'fullName': 'LONSO IRR'}}
{'id': '116969031591258211573', 'name': {'givenName': 'EMAN', 'familyName': 'ABDUREZAK', 'fullName': 'EMAN ABDUREZAK'}}
{'id': '104076916696146047444', 'name': {'givenName': 'DEREK', 'familyName': 'PRICE', 'fullName': 'DEREK PRICE'}}
{'id': '117853584363396485494', 'name': {'givenName': 'ANWESHA', 'familyName': 'MAITY', 'fullName': 'ANWESHA MAITY'}}
{'id': '112008539441208883957', 'name': {'givenName': 'FAROOZ', 'familyName': 'KHAN-TRUNNELL', 'fullName': 'FAROOZ KHAN-TRUNNELL'}}
{'id': '117699940410151230499', 'name': {'givenName': 'JIAMING', 'familyName': 'WANG', 'fullName': 'JIAMING WANG'}}
{'id': '103833412767890898981', 'name': {'givenName': 'Elias', 'familyName': 'Regina', 'fullName': 'Elias Regina'}}
{'id': '102475404831589545837', 'name': {'givenName': 'Sauvik', 'familyName': 'Roy', 'fullName': 'Sauvik Roy'}}
{'id': '113300105166289299368', 'name': {'givenName': 'MEKEYAS', 'familyName': 'MEKURIA', 'fullName': 'MEKEYAS MEKURIA'}}
{'id': '112700773999980928897', 'name': {'givenName': 'CHLOE', 'familyName': 'YANG', 'fullName': 'CHLOE YANG'}}
{'id': '114034608136063461848', 'name': {'givenName': 'ANTHONY', 'familyName': 'ARIAS-ESTRADA', 'fullName': 'ANTHONY ARIAS-ESTRADA'}}
{'id': '111434302568014093638', 'name': {'givenName': 'GRACE', 'familyName': 'VALASKOVIC', 'fullName': 'GRACE VALASKOVIC'}}
{'id': '110461501134972561443', 'name': {'givenName': 'Jeiran', 'familyName': 'Kvaitchadze', 'fullName': 'Jeiran Kvaitchadze'}}
'''
email_dict = {
'108001275956982622720': '24adawson@cpsd.us',
'108001275956982622720': '23zsiegelnickel@cpsd.us',
'103072792655643970842': '21twoodward@cpsd.us',
'108395054813353959432': '23lirr@cpsd.us',
'116969031591258211573': '23eabdurezak@cpsd.us',
'104076916696146047444': '23dprice@cpsd.us',
'117853584363396485494': '22amaity@cpsd.us',
'112008539441208883957': '24fkhan-trunnell@cpsd.us',
'117699940410151230499': '23jwang@cpsd.us',
'103833412767890898981': '24eregina@cpsd.us',
'102475404831589545837': '22sroy@cpsd.us',
'113300105166289299368': '23mmekuria@cpsd.us',
'112700773999980928897': '23cyang@cpsd.us',
'114034608136063461848': '24aarias-estrada@cpsd.us',
'111434302568014093638': '21gvalaskovic@cpsd.us',
'110461501134972561443': '24jkvaitchadze@cpsd.us',
}

students = service_classroom.courses().students().list(courseId=course_id,).execute()
students = students['students']


for student in students:
    student_id = student['userId']
    student_profiles = service_classroom.userProfiles().get(userId=student_id,).execute()
    print(student_profiles)
    # print(student_profiles['emailAddress'])


assignments_id_dict = {}
all_assignments = service_classroom.courses().courseWork().list(courseId=course_id,).execute()
all_assignments = all_assignments['courseWork']
# print(all_assignments)
for assignment in all_assignments:
    assignments_id_dict[assignment['id']] = assignment['title']

#print("HERE ARE THE ASSIGNMENTS AND THEIR IDs")
#print(assignments_id_dict)

messages = []
for student in students:
    student_id = student['userId']
    message_dict = {}
    message_dict[student_id] = ''
    if student_id in email_dict:
        print("Trying this student ID : " + str(student_id))
        print("this student" + email_dict[student_id])
        student_email = email_dict[student_id]
        student_work = service_classroom.courses().courseWork().studentSubmissions().list(courseId=course_id, courseWorkId='-',userId=student_id).execute()
        student_work = student_work['studentSubmissions']
        for work in student_work:

            if 'late' in work:
                work_id = work['courseWorkId']
                for assignment in all_assignments:
                    if work_id == assignment['id']:
                        due_date = assignment['dueDate']

                if work['state'] != 'TURNED_IN' and work['late'] is True:
                    d1 = datetime.datetime(due_date['year'], due_date['month'], due_date['day'])
                    d2 = datetime.datetime.now()
                    q2 = datetime.datetime(2020, 11, 14)
                    if d2 >= d1 and d1 > q2:
                        link = work['alternateLink']
                        coursework_id = work['courseWorkId']
                        message_dict[student_id] += "assignment:  {} \nlink to assignment {}\n\n".format(assignments_id_dict[coursework_id], link)
        messages.append(message_dict)
#message_dict = create_message('ewu@cpsd.us', 'ejw50@hotmail.com', 'hello there', 'smell my   feet')
#print(message_dict)
service_gmail = generate_gmail_credential()

print("these are messages")
for message in messages:
    for key in message:
        email_address = email_dict[key]
        print("This person " + str(email_address) + " is missing these (past due) assignments ")
        if not message[key]:
            message[key] = 'Nothing! You have everything turned in that is due.  Great work!'
        else:
            message[key] = "Hello! Here are assignments that are past due that are not turned in yet:\n\n" + message[key]
        message[key] = email_address + '\n' + message[key]

        message[key] += '\n\nLast day to turn in assignments for quarter 3 is Friday 04/9/21!!!!\n\n'

        # message[key] += '\n\nLast day to turn in assignments or extra credit is Friday 01/29/21\n\n'
        # message[key] += 'Create task must be "finalized" by 1/29 and turned in the digital portfolio, even if ' \
        #                 'you are not taking the AP exam.  \n' \
        #                 'link: https://digitalportfolio.collegeboard.org/\n\n' \
        #                 'If you need to edit your AP create task after 1/29, we can "unfinalize" it for you.\n'


        message[key] += '\n\nThis is an automated email\n\n'
        print(message[key])


        msg_text = message[key]
        email_message = MIMEMultipart()
        email_message['to'] = email_address
        email_message['cc'] = 'ewu@cpsd.us,mkann@cpsd.us'
        email_message['subject'] = 'AP CSP assignments report'
        email_message.attach(MIMEText(msg_text, 'plain'))
        raw_string = base64.urlsafe_b64encode(email_message.as_bytes()).decode()

       # send_message = service_gmail.users().messages().send(userId='me', body={'raw': raw_string}).execute()
      #  print(send_message)