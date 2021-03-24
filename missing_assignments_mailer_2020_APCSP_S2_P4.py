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


course_id = 253721407705
service_classroom = generate_classroom_credential()


student_dict = {'21nlei@cpsd.us': '103026788979009218908',
                '21atekieteklemariam@cpsd.us': 102189211805773929897}

'''
{'id': '117452578857277872875', 'name': {'givenName': 'KIDUSZ', 'familyName': 'DESALEGN', 'fullName': 'KIDUSZ DESALEGN'}}
{'id': '103272859374799712470', 'name': {'givenName': 'DANTE', 'familyName': 'PEREIRA', 'fullName': 'DANTE PEREIRA'}}
{'id': '115740157332489436144', 'name': {'givenName': 'DANIEL', 'familyName': 'HAILEMICHAEL', 'fullName': 'DANIEL HAILEMICHAEL'}}
{'id': '114909928568690002693', 'name': {'givenName': 'CHRISTOPHER', 'familyName': 'GOULD', 'fullName': 'CHRISTOPHER GOULD'}}
{'id': '100005598522736662577', 'name': {'givenName': 'Amel', 'familyName': 'Hirwa', 'fullName': 'Amel Hirwa'}}
{'id': '102848789089810514900', 'name': {'givenName': 'Adel', 'familyName': 'Baimatova', 'fullName': 'Adel Baimatova'}}
{'id': '117683953214224961729', 'name': {'givenName': 'NILA', 'familyName': 'KRISHNAMURTHY', 'fullName': 'NILA KRISHNAMURTHY'}}
{'id': '116599132288268488441', 'name': {'givenName': 'WILLIAM', 'familyName': 'KAUFMANN', 'fullName': 'WILLIAM KAUFMANN'}}
{'id': '100437299855115523930', 'name': {'givenName': 'MOHAMMED', 'familyName': 'MUSAWWIR', 'fullName': 'MOHAMMED MUSAWWIR'}}
{'id': '115201586460491413577', 'name': {'givenName': 'Mohamed-Nabil', 'familyName': 'Bentayeb', 'fullName': 'Mohamed-Nabil Bentayeb'}}
{'id': '112564350864349666347', 'name': {'givenName': 'MIRANDA', 'familyName': 'SANTIAGO', 'fullName': 'MIRANDA SANTIAGO'}}
{'id': '114206349887093438144', 'name': {'givenName': 'Basem', 'familyName': 'Moustafa', 'fullName': 'Basem Moustafa'}}
{'id': '110666845259670072790', 'name': {'givenName': 'Paul', 'familyName': 'Colombo', 'fullName': 'Paul Colombo'}}
{'id': '106465749274984627003', 'name': {'givenName': 'Andrew', 'familyName': 'Mccarroll', 'fullName': 'Andrew Mccarroll'}}
{'id': '111106579952134632116', 'name': {'givenName': 'Fairooz', 'familyName': 'Chowdhury', 'fullName': 'Fairooz Chowdhury'}}
{'id': '102149991699609361106', 'name': {'givenName': 'MAIA', 'familyName': 'FEIK REINHART', 'fullName': 'MAIA FEIK REINHART'}}
{'id': '105919406273768327593', 'name': {'givenName': 'SELINA', 'familyName': 'HAILEMARIAM', 'fullName': 'SELINA HAILEMARIAM'}}

'''
email_dict = {
'117452578857277872875': '23kdesalegn@cpsd.us',
'115740157332489436144': '22dhailemichael@cpsd.us',
'114909928568690002693': '22cgould@cpsd.us',
'100005598522736662577': '23ahirwa@cpsd.us',
'102848789089810514900': '21abaimatova@cpsd.us',
'117683953214224961729': '23nkrishnamurthy@cpsd.us',
'116599132288268488441': '22wkaufmann@cpsd.us',
'100437299855115523930': '23mmusawwir@cpsd.us',
'115201586460491413577': '23mbentayeb@cpsd.us',
'112564350864349666347': '22msantiago@cpsd.us',
'114206349887093438144': '23bmoustafa@cpsd.us',
'110666845259670072790': '24pcolombo@cpsd.us',
'106465749274984627003': '24amccarroll@cpsd.us',
'111106579952134632116': '23fchowdhury@cpsd.us',
'102149991699609361106': '23mfeikreinhart@cpsd.us',
'105919406273768327593': '22shailemariam@cpsd.us',
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
        email_message['cc'] = 'ewu@cpsd.us'
        email_message['subject'] = 'AP CSP assignments report'
        email_message.attach(MIMEText(msg_text, 'plain'))
        raw_string = base64.urlsafe_b64encode(email_message.as_bytes()).decode()

        send_message = service_gmail.users().messages().send(userId='me', body={'raw': raw_string}).execute()
        print(send_message)