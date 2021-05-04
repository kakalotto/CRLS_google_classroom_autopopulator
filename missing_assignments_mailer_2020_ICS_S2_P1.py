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


course_id = 246968428370
service_classroom = generate_classroom_credential()


student_dict = {'21nlei@cpsd.us': '103026788979009218908',
                '21atekieteklemariam@cpsd.us': 102189211805773929897}

'''
{'id': '118095516207692353716', 'name': {'givenName': 'JACOB', 'familyName': 'IRIZARRY', 'fullName': 'JACOB IRIZARRY'}}
{'id': '110021248229995981442', 'name': {'givenName': 'JUAN-MARIO', 'familyName': 'VUKSAN', 'fullName': 'JUAN-MARIO VUKSAN'}}
{'id': '117349461051374077598', 'name': {'givenName': 'ABIR', 'familyName': 'RAFE', 'fullName': 'ABIR RAFE'}}
{'id': '112150919220813497779', 'name': {'givenName': 'EDWIN', 'familyName': 'SMILACK', 'fullName': 'EDWIN SMILACK'}}
{'id': '112659499704384123491', 'name': {'givenName': 'ANTINOE', 'familyName': 'KOTSOPOULOS', 'fullName': 'ANTINOE KOTSOPOULOS'}}
{'id': '112329362841763056202', 'name': {'givenName': 'Florencia', 'familyName': 'Tapia', 'fullName': 'Florencia Tapia'}}
{'id': '107712720518728788404', 'name': {'givenName': 'Sara', 'familyName': 'Sabry', 'fullName': 'Sara Sabry'}}
{'id': '108472701554519800199', 'name': {'givenName': 'RAIMI', 'familyName': 'RIPPEY', 'fullName': 'RAIMI RIPPEY'}}
{'id': '107216050800037472541', 'name': {'givenName': 'MADISON', 'familyName': 'BARTEE', 'fullName': 'MADISON BARTEE'}}
{'id': '117792824151683217447', 'name': {'givenName': 'JADEN', 'familyName': 'TRAN', 'fullName': 'JADEN TRAN'}}
{'id': '106074871954277180882', 'name': {'givenName': 'VIDA', 'familyName': 'VELASCO', 'fullName': 'VIDA VELASCO'}}
{'id': '111658614171811028380', 'name': {'givenName': 'ELIZA', 'familyName': 'DICKIE', 'fullName': 'ELIZA DICKIE'}}
{'id': '116301743374649954865', 'name': {'givenName': 'Amreenbanu', 'familyName': 'Gadatia', 'fullName': 'Amreenbanu Gadatia'}}
{'id': '104576564205135421850', 'name': {'givenName': 'BRUNO', 'familyName': 'MUNOZ-OROPEZA', 'fullName': 'BRUNO MUNOZ-OROPEZA'}}
{'id': '118112896775925424096', 'name': {'givenName': 'HUMAIRA', 'familyName': 'AFRICAWALA', 'fullName': 'HUMAIRA AFRICAWALA'}}
{'id': '105373365405854105717', 'name': {'givenName': 'YASH', 'familyName': 'BAGGA', 'fullName': 'YASH BAGGA'}}
{'id': '115453615822437566312', 'name': {'givenName': 'LWAM', 'familyName': 'MAHARI', 'fullName': 'LWAM MAHARI'}}
{'id': '118309547490022435201', 'name': {'givenName': 'Mohammad', 'familyName': 'Jihad', 'fullName': 'Mohammad Jihad'}}
{'id': '115742769114603916849', 'name': {'givenName': 'AMARI', 'familyName': 'CEAC', 'fullName': 'AMARI CEAC'}}
'''
email_dict = {
    '118095516207692353716': '23jirizarry@cpsd.us',
    '110021248229995981442': '24jvuksan@cpsd.us',
    '117349461051374077598': '23arafe@cpsd.us',
    '112150919220813497779': '23esmilack@cpsd.us',
    '112659499704384123491': '22akotsopoulos@cpsd.us',
    '112329362841763056202': '22ttapia@cpsd.us',
    '107712720518728788404': '24ssabry@cpsd.us',
    '108472701554519800199': '21rrippey@cpsd.us',
    '107216050800037472541': '23mbartee@cpsd.us',
    '117792824151683217447': '24jtran@cpsd.us',
    '106074871954277180882': '24vvelasco@cpsd.us',
    '111658614171811028380': '24edickie@cpsd.us',
    '116301743374649954865': '23agadatia@cpsd.us',
    '104576564205135421850': '21bmunoz-oropeza@cpsd.us',
    '118112896775925424096': '22hafricawala@cpsd.us',
    '105373365405854105717': '22ybagga@cpsd.us',
    '115453615822437566312': '22lmahari@cpsd.us',
    '118309547490022435201': '24mjihad@cpsd.us',
    '115742769114603916849': '22aceac@cpsd.us',
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
                    q2 = datetime.datetime(2021, 2, 4)
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
        email_message['cc'] = 'ewu@cpsd.us, mtmurphy@cpsd.us'
        email_message['subject'] = 'Intro to CS assignments report'
        email_message.attach(MIMEText(msg_text, 'plain'))
        raw_string = base64.urlsafe_b64encode(email_message.as_bytes()).decode()

        send_message = service_gmail.users().messages().send(userId='me', body={'raw': raw_string}).execute()
        print(send_message)