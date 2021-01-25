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


course_id = 164978040288
service_classroom = generate_classroom_credential()


student_dict = {'21nlei@cpsd.us': '103026788979009218908',
                '21atekieteklemariam@cpsd.us': 102189211805773929897}

'''
{'id': '106302684326838575074', 'name': {'givenName': 'Ibta', 'familyName': 'Chowdhury', 'fullName': 'Ibta Chowdhury'}}
{'id': '103026788979009218908', 'name': {'givenName': 'NING-ER', 'familyName': 'LEI', 'fullName': 'NING-ER LEI'}}
{'id': '107705225444308491895', 'name': {'givenName': 'ISAAC', 'familyName': 'WEDAMAN', 'fullName': 'ISAAC WEDAMAN'}}
{'id': '103561355144787719910', 'name': {'givenName': 'RIVKA', 'familyName': 'ZICKLER', 'fullName': 'RIVKA ZICKLER'}}
{'id': '102189211805773929897', 'name': {'givenName': 'Abel', 'familyName': 'Tekie Teklemariam', 'fullName': 'Abel Tekie Teklemariam'}}
{'id': '111937520438917276179', 'name': {'givenName': 'Alexander', 'familyName': 'Thearling', 'fullName': 'Alexander Thearling'}}
{'id': '110177580948269407840', 'name': {'givenName': 'SOPHIA', 'familyName': 'PRICE', 'fullName': 'SOPHIA PRICE'}}
{'id': '116508309214412781248', 'name': {'givenName': 'STEPHEN', 'familyName': 'GWON', 'fullName': 'STEPHEN GWON'}}
{'id': '117781278118817502289', 'name': {'givenName': 'SKYLER', 'familyName': 'MARKS', 'fullName': 'SKYLER MARKS'}}
{'id': '116803666292650634300', 'name': {'givenName': 'WILLIAM', 'familyName': 'SPEIGHT', 'fullName': 'WILLIAM SPEIGHT'}}
{'id': '109935763611444835059', 'name': {'givenName': 'SAMUEL', 'familyName': 'KIM', 'fullName': 'SAMUEL KIM'}}
{'id': '111459602464629250094', 'name': {'givenName': 'Milo', 'familyName': 'Song-Weiss', 'fullName': 'Milo Song-Weiss'}}
{'id': '109280795417965105924', 'name': {'givenName': 'ALISTER', 'familyName': 'CUTLER', 'fullName': 'ALISTER CUTLER'}}
{'id': '101150326899581288337', 'name': {'givenName': 'JARROD', 'familyName': 'JONES', 'fullName': 'JARROD JONES'}}
{'id': '101735270111427702213', 'name': {'givenName': 'ROBERT', 'familyName': 'CLEMENS', 'fullName': 'ROBERT CLEMENS'}}
{'id': '102382921205084160882', 'name': {'givenName': 'LARA', 'familyName': 'ARTIGAS', 'fullName': 'LARA ARTIGAS'}}
{'id': '102971606372646759587', 'name': {'givenName': 'JOSEPH', 'familyName': 'BETANCOURT', 'fullName': 'JOSEPH BETANCOURT'}}

'''
email_dict = {
'107705225444308491895': '23iwedaman@cpsd.us',
'103561355144787719910': '24rzickler@cpsd.us',
'102189211805773929897': '21atekieteklemariam@cpsd.us',
'111937520438917276179': '21athearling@cpsd.us',
'110177580948269407840': '21sprice@cpsd.us',
'116508309214412781248': '24sgwon@cpsd.us',
'117781278118817502289': '22smarks@cpsd.us',
'116803666292650634300': '24wspeight@cpsd.us',
'109935763611444835059': '23skim@cpsd.us',
'111459602464629250094': '21msong-weiss@cpsd.us',
'109280795417965105924': '21acutler@cpsd.us',
'101150326899581288337': '22jajones@cpsd.us',
'101735270111427702213': '22rclemens@cpsd.us',
'102382921205084160882': '23lartigas@cpsd.us',
'102971606372646759587': '23jbetancourt@cpsd.us',
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


        message[key] += '\n\nLast day to turn in assignments or extra credit is Friday 01/29/21\n\n'
        message[key] += 'Create task must be "finalized" by 1/29 and turned in the digital portfolio, even if ' \
                        'you are not taking the AP exam.  \n' \
                        'link: https://digitalportfolio.collegeboard.org/\n\n' \
                        'If you need to edit your AP create task after 1/29, we can "unfinalize" it for you.\n'


        message[key] += '\n\nThis is an automated email\n\n'
        print(message[key])


        msg_text = message[key]
        email_message = MIMEMultipart()
        email_message['to'] = email_address
        email_message['cc'] = 'ewu@cpsd.us,mkann@cpsd.us'
        email_message['subject'] = 'AP CSP assignments report'
        email_message.attach(MIMEText(msg_text, 'plain'))
        raw_string = base64.urlsafe_b64encode(email_message.as_bytes()).decode()

        send_message = service_gmail.users().messages().send(userId='me', body={'raw': raw_string}).execute()
        print(send_message)