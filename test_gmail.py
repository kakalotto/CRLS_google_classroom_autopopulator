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


course_id = 164965412687
service_classroom = generate_classroom_credential()


student_dict = {'21nlei@cpsd.us': '103026788979009218908',
                '21atekieteklemariam@cpsd.us': 102189211805773929897}

'''
{'id': '118019748065546509612', 'name': {'givenName': 'ELIAS', 'familyName': 'POOR', 'fullName': 'ELIAS POOR'}}
{'id': '100871169894951601685', 'name': {'givenName': 'Antonio', 'familyName': 'Barandao', 'fullName': 'Antonio Barandao'}}
{'id': '110876164562340111873', 'name': {'givenName': 'ELI', 'familyName': 'KANNER', 'fullName': 'ELI KANNER'}}
{'id': '105017346725485429401', 'name': {'givenName': 'JIN HO', 'familyName': 'LEE', 'fullName': 'JIN HO LEE'}}
{'id': '104113433050725927606', 'name': {'givenName': 'ZACCARIA', 'familyName': 'MIR', 'fullName': 'ZACCARIA MIR'}}
{'id': '117986384455193347817', 'name': {'givenName': 'MARGARET', 'familyName': 'UNGER', 'fullName': 'MARGARET UNGER'}}
{'id': '102898302120491642633', 'name': {'givenName': 'MATTHEW', 'familyName': 'LIU', 'fullName': 'MATTHEW LIU'}}
{'id': '100698129038669714895', 'name': {'givenName': 'Sergey', 'familyName': 'Koenig', 'fullName': 'Sergey Koenig'}}
{'id': '110324586370991168343', 'name': {'givenName': 'MAHEK', 'familyName': 'KAPADIA', 'fullName': 'MAHEK KAPADIA'}}
{'id': '107115973202555038760', 'name': {'givenName': 'TAVIEN', 'familyName': 'POLLARD', 'fullName': 'TAVIEN POLLARD'}}
{'id': '117913055311995206070', 'name': {'givenName': 'Claire', 'familyName': 'Wang', 'fullName': 'Claire Wang'}}
{'id': '108243673046075981382', 'name': {'givenName': 'Cedar', 'familyName': 'Larson', 'fullName': 'Cedar Larson'}}
{'id': '105690526668455496344', 'name': {'givenName': 'Nebiyu', 'familyName': 'Demie', 'fullName': 'Nebiyu Demie'}}
{'id': '101091239715242333236', 'name': {'givenName': 'LUCY', 'familyName': 'ENGELS', 'fullName': 'LUCY ENGELS'}}

'''
email_dict = {
    '100871169894951601685': '22abarandao@cpsd.us',
    '118019748065546509612': '23epoor@cpsd.us',
    '110876164562340111873': '23ekanner@cpsd.us',
    '105017346725485429401': '22jlee@cpsd.us',
    '104113433050725927606': '23zmir@cpsd.us',
    '117986384455193347817': '23munger@cpsd.us',
    '102898302120491642633': '22mliu@cpsd.us',
    '100698129038669714895': '24skoenig@cpsd.us',
    '110324586370991168343': '24mkapadia@cpsd.us',
    '107115973202555038760': '23tpollard@cpsd.us',
    '117913055311995206070': '22cwang@cpsd.us',
    '108243673046075981382': '24clarson@cpsd.us',
    '105690526668455496344': '24ndemie@cpsd.us',
    '101091239715242333236': '23lengels@cpsd.us'
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
            message[key] = "Hello! Here are assignments that are due that are not turned in yet:\n\n" + message[key]
        message[key] = email_address + '\n' + message[key]
        message[key] += '\n\nThis is an automated email\n\n'
        print(message[key])


        msg_text = message[key]
        email_message = MIMEMultipart()
        email_message['to'] = email_address
        email_message['cc'] = 'ewu@cpsd.us'

        email_message['subject'] = 'AP CSP assignments report'
        email_message.attach(MIMEText(msg_text, 'plain'))
        raw_string = base64.urlsafe_b64encode(email_message.as_bytes()).decode()

        send_message = service_gmail.users().messages().send(userId='me', body={'raw': raw_string}).execute()
        print(send_message)