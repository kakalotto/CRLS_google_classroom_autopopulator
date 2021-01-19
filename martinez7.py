
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from datetime import datetime

# for ASPEN
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

#for colors
from termcolor import colored

#For explicit waiting times
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#The following location should be basically the same place where the main project is stored
path_were_the_Google_webdriver_is_stored = r'C:\Users\dimmyfinster\Dropbox\dimmyfinster18\Downloads\chromedriver.exe'


flag = " :-)"

# Check into ASPEN and GC, fill this dictionary:
ASPEN_vs_Gclassroom_dictionary = {'IT1/CS1':'T604-001',
                                 #'AP Computer Science Principles P4':'T608-003',
                                 #   'Murphy S1 P1 Intro to CS' : 'M415-001',
                                 # 'IT3 2020-2021':'T986-001',
                                 # 'IT2 2020-2021': 'T746-001',
                                 # 'T527A-001: SY2020-21 TC Web Design & Development':'T527A-001',
                                  }

# In aspen you need the following categories
# content_knowledge
# completion
# CheckIn_Studentship

#-------------------------------    Gclassroom Code     -------------------------------

def create_Gclassroom_service():
    # if you want to switch between the google classroom of CRLS and your personal account
    # just delete the "token.pickle" file on the work directory of this file and re-run the program

    # If modifying these scopes, delete the file token.pickle.
    Gclassroom_SCOPES = [    'https://www.googleapis.com/auth/classroom.announcements',
                             'https://www.googleapis.com/auth/classroom.courses',
                             'https://www.googleapis.com/auth/classroom.coursework.students',
                             'https://www.googleapis.com/auth/classroom.rosters',
                             'https://www.googleapis.com/auth/classroom.topics',
                             # 'https://www.googleapis.com/auth/classroom.courses',
                             # 'https://www.googleapis.com/auth/classroom.rosters',
                        # 'https://www.googleapis.com/auth/classroom.coursework.students',
                        # 'https://www.googleapis.com/auth/classroom.topics',
                        ]


    """Shows basic usage of the Classroom API.
    Prints the names of the first 10 courses the user has access to.
    """
    # The following takes care of the credentials....  just don't touch....
    Gclassroom_creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token_classroom_martinez.pickle'):
        with open('token_classroom_martinez.pickle', 'rb') as token:
            Gclassroom_creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not Gclassroom_creds or not Gclassroom_creds.valid:
        if Gclassroom_creds and Gclassroom_creds.expired and Gclassroom_creds.refresh_token:
            Gclassroom_creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials_classroom.json', Gclassroom_SCOPES)
            Gclassroom_creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token_classroom_martinez.pickle', 'wb') as token:
            pickle.dump(Gclassroom_creds, token)

    # Once the credentials have been established we start accessing the google classroom
    service = build('classroom', 'v1', credentials=Gclassroom_creds)
    return service
Gclassroom_service = create_Gclassroom_service()

def obtain_Gclassrooms_dictionary_only_for_ASPEN_classes(service): # Names is the key
    import re
    # Call the Classroom API to get all the google classrooms within the account with the login credentials created above above
    results = service.courses().list().execute()  # <----- This is a dictionary with two pairs,
    # the first one is the only one that matters, its called courses
    # the following gives a list of dictionaries, one element for each Gclassroom
    courses_list = results.get('courses', [])  #<---- This is a list with dictionaries as the elements... each element

    # we will turn the list into a dictionary where the keys are the Gclassroom names
    courses_dictionary = {}

    if not courses_list: # This catches if there are no courses in the account... troubleshoots if you are in the right account
        print('No courses found.')
    else:
        # The following turns the list into a dictionary
        for course in courses_list:
            if course['name'] in ASPEN_vs_Gclassroom_dictionary.keys():
                print("Found a course that I want to edit! {}".format(course['name']))

                print("Getting categories now")
                course['courseWork categories'] = service.courses().topics().list(courseId=course['id']).execute().get('topic', [])
                Categories_dictionary = {}
                for category in course['courseWork categories']:
                    Categories_dictionary[category['topicId']] = category
                course['courseWork categories'] = Categories_dictionary

                print("Getting assignments now")
                CourseWork_dictionary = {}
                for state in ['PUBLISHED', 'DRAFT']:
                    print("trying this status " + str(state))
                    course['CourseWork'] = service.courses().courseWork().list(courseId=course['id'], courseWorkStates=state).execute().get('courseWork', [])
                    for courseWork in course['CourseWork']:
                        # print("assignment is {}".format(courseWork))
                        ASPEN_coursework_categories = ['grade term','category','GB column name','Assignment name','Date assigned','Date due','Total points','Sequence number','extra credit points']
                        new_title = courseWork['title']
                        new_title = re.sub('Python ', 'py', new_title)
                        new_title = re.sub('Scratch ', 'Sc', new_title)
                        new_title = re.sub('Autograder', 'AG', new_title)
                        new_title = re.sub('Encryption', 'Encrp', new_title)
                        print("TITLE IS " + str(new_title))

                        if len(new_title) >= 7:
                            GB_column_name = new_title[:7] + '-K'
                        else:
                            GB_column_name = new_title + '-K'

                        if len(new_title) >= 50:
                            Assignment_name = new_title[:50]
                        else:
                            Assignment_name = new_title

                        if 'dueDate' in courseWork:
                            python_assigned_date = datetime(int(courseWork['dueDate']['year']), int(courseWork['dueDate']['month']), int(courseWork['dueDate']['day']))
                        else:
                            print("SKIPPING THIS ONE, NO DUE DATE: " + str(new_title))
                            continue
                        End_of_quarter_dates = {'Q1':datetime(2020, 11, 13), 'Q2': datetime(2021, 1, 29), 'Q3': datetime(2021, 4, 9)}

                        if state == 'PUBLISHED':
                            year_assigned = courseWork['creationTime'].split("T")[0].split('-')[0]
                            month_assigned = courseWork['creationTime'].split("T")[0].split('-')[1]
                            day_assigned = courseWork['creationTime'].split("T")[0].split('-')[2]
                        else:
                            year_assigned = courseWork['scheduledTime'].split("T")[0].split('-')[0]
                            month_assigned = courseWork['scheduledTime'].split("T")[0].split('-')[1]
                            day_assigned = courseWork['scheduledTime'].split("T")[0].split('-')[2]
                        date_assigned = month_assigned + "/" + day_assigned + "/" + year_assigned
                        if python_assigned_date <= End_of_quarter_dates['Q1']:
                            grade_term = 'Q1'
                        elif python_assigned_date <= End_of_quarter_dates['Q2']:
                            grade_term = 'Q2'
                        elif python_assigned_date <= End_of_quarter_dates['Q3']:
                            grade_term = 'Q3'
                        else:
                            grade_term = 'Q4'
                        print("PYTHON ASSIGNED DATE {}    TERM {}".format(python_assigned_date, grade_term))
                        print("\n\n")

                        try:
                            ASPEN_points = courseWork['maxPoints']
                        except:
                            ASPEN_points = 1

                        try:
                            ASPEN_due_date = str(courseWork['dueDate']['month']) + "/" + str(
                                courseWork['dueDate']['day']) + "/" + str(courseWork['dueDate']['year'])
                        except:
                            ASPEN_due_date = date_assigned


                        ASPEN_courseWork_values = {
                            'grade term': {'ASPEN_value': grade_term, 'num_of_tabs': 23},
                            'category': {'ASPEN_value': 'content_knowledge', 'num_of_tabs': 2},
                            # fix for short names
                            'GB column name': {'ASPEN_value': GB_column_name, 'num_of_tabs': 1},
                            'Assignment name': {'ASPEN_value': Assignment_name, 'num_of_tabs': 1},
                            'Date assigned': {'ASPEN_value': date_assigned, 'num_of_tabs': 2},
                            'Date due': {'ASPEN_value': ASPEN_due_date, 'num_of_tabs': 3},
                            'Total points': {'ASPEN_value': ASPEN_points, 'num_of_tabs': 8},
                            'Sequence number': {'ASPEN_value': "", 'num_of_tabs': 10},
                            'extra credit points': {'ASPEN_value': str(round(int(courseWork['maxPoints']) * .05)),
                                                    'num_of_tabs': 0},
                        }

                        courseWork['ASPEN_coursework_categories'] = ASPEN_coursework_categories
                        courseWork['ASPEN_courseWork_values'] = ASPEN_courseWork_values
                        courseWork['Gclassroom_topic'] = course['courseWork categories'][courseWork['topicId']]['name']
                        CourseWork_dictionary[new_title] = courseWork
                        print("THIS IS COURSEWORK!!! \n{}".format(courseWork))
                course['CourseWork'] = CourseWork_dictionary
                courses_dictionary[course['name']] = course
    return courses_dictionary
Gclassrooms_dictionary = obtain_Gclassrooms_dictionary_only_for_ASPEN_classes(Gclassroom_service)
print("Printing google classrooms dictionary now")
for key in Gclassrooms_dictionary:
    print(Gclassrooms_dictionary[key])
    print()
def print_Gclassrooms(Gclassrooms):
    for Gclassroom in Gclassrooms.keys():
        print(Gclassroom + " ---- " + str(Gclassrooms[Gclassroom]))
        for Gclassroom_attribute in Gclassrooms[Gclassroom].keys():
            if Gclassroom_attribute != 'CourseWork' and Gclassroom_attribute != 'courseWork categories':
                print('\t' + Gclassroom_attribute + ' ---- ' + str(Gclassrooms[Gclassroom][Gclassroom_attribute]))
            elif Gclassroom_attribute == 'courseWork categories':
                print('\t' + 'courseWork categories')
                for category in Gclassrooms[Gclassroom]['courseWork categories'].keys():
                    print('\t\t' + category + ' ---- ' + str(Gclassrooms[Gclassroom][Gclassroom_attribute][category]))
            elif Gclassroom_attribute == 'CourseWork':
                print('\t' + 'CourseWork')
                for task in Gclassrooms[Gclassroom]['CourseWork'].keys():
                    print('\t\t' + task + ' ---- ' + str(Gclassrooms[Gclassroom][Gclassroom_attribute][task]))
                    print('\t\t\t' + str(Gclassrooms[Gclassroom][Gclassroom_attribute][task]['Gclassroom_topic']))
                    for task_ASPEN_attribute in Gclassrooms[Gclassroom][Gclassroom_attribute][task]['ASPEN_courseWork_values'].keys():
                        print('\t\t\t' + task_ASPEN_attribute + ' ---- ' + str(Gclassrooms[Gclassroom][Gclassroom_attribute][task]['ASPEN_courseWork_values'][task_ASPEN_attribute]))

        print('\n\n')
print("PRINTING GOOGLE CLASSROOMS HERE")
#print_Gclassrooms(Gclassrooms_dictionary)


#-------------------------------    ASPEN Code     -------------------------------

def open_and_log_into_ASPEN(ASPEN_webdriver_path):
    # Control Variables
    time_to_wait_for_user_input = 20

    # import the chromedriver as we will code a robot that uses aspen to manage google classroom
    chrome_webdriver_robot = webdriver.Chrome(executable_path=ASPEN_webdriver_path)

    # navigate to aspen
    chrome_webdriver_robot.get("https://aspen.cpsd.us/aspen/home.do")
    # chrome_webdriver_robot.get("https://www.youtube.com")

    # # see the title of the website and decide if we are in the right website indeed
    # print(chrome_webdriver_robot.title)  ## <---- this is for developing purposes, just to see what the title would ideally say
    assert "Aspen" in chrome_webdriver_robot.title

    # we click in the opening aspen screen to enter our credentials
    aspen_login_button = chrome_webdriver_robot.find_element_by_class_name('button').click()

    # we wait for the user to login
    WebDriverWait(chrome_webdriver_robot, time_to_wait_for_user_input).until(EC.presence_of_element_located((By.ID, "contextMenu")))

    # # We login for the user
    # # type the username in the logon textbox
    # aspen_login_username_textfield = chrome_webdriver_robot.find_element_by_id('username')
    # aspen_login_username_textfield.send_keys("ewu")
    # # type the password in the logon textbox
    # aspen_login_password_textfield = chrome_webdriver_robot.find_element_by_id('password')
    # aspen_login_password_textfield.send_keys("#$#$#")
    # # # click enter to enter the matrix
    # aspen_login_password_textfield.send_keys(Keys.RETURN)

    return chrome_webdriver_robot

def add_assignments_to_ASPEN(Gclassrooms, robot_path, service):
    robot = open_and_log_into_ASPEN(robot_path)
    print("LOGGED IN")

    print("These is the current google classrooms {}".format(Gclassrooms))
    print()
    for course in Gclassrooms.keys():
        print("we are at this course {}".format(course))
        print(colored("\t" + Gclassrooms[course]['name'], 'green'))

        robot.find_element_by_link_text("Gradebook").click()
        robot.find_element_by_link_text(ASPEN_vs_Gclassroom_dictionary[Gclassrooms[course]['name']]).click()
        robot.find_element_by_link_text("Scores").click()
        time.sleep(3)

        for task in Gclassrooms[course]['CourseWork'].keys():
            print("Here is the current task: {}".format(task))
#            if flag not in Gclassrooms[course]['CourseWork'][task]['title'] and Gclassrooms[course]['CourseWork'][task]['state'] == "PUBLISHED":

            if flag not in Gclassrooms[course]['CourseWork'][task]['title']:
                print(colored("\t\t" + task + " --------- " + "Content Knowledge",'red'))

                robot.find_element_by_css_selector("body").send_keys(Keys.CONTROL, "a")
                while len(robot.window_handles) == 1:
                    time.sleep(1) # <---for the add assignment tab to load
                robot.switch_to_window(robot.window_handles[1])

                robot_actions = ActionChains(robot)
                # The following goes to the "Visibility Type" In aspen and makes it public
                for repetition in range(19):
                    robot_actions.send_keys(Keys.TAB)
                for repetition in range(2):
                    robot_actions.send_keys(Keys.ARROW_LEFT)
                for repetition in range(4):
                    robot_actions.send_keys(Keys.TAB)
                robot_actions.perform()
                for ASPEN_input_value in Gclassrooms[course]['CourseWork'][task]['ASPEN_coursework_categories']:
                    robot_actions = ActionChains(robot)
                    robot_actions.send_keys(Gclassrooms[course]['CourseWork'][task]['ASPEN_courseWork_values'][ASPEN_input_value]['ASPEN_value'])
                    print("aspen input value {}      {}".format(ASPEN_input_value, Gclassrooms[course]['CourseWork'][task]['ASPEN_courseWork_values'][ASPEN_input_value]['ASPEN_value']))
                    for repetition in range(Gclassrooms[course]['CourseWork'][task]['ASPEN_courseWork_values'][ASPEN_input_value]['num_of_tabs']):
                        if ASPEN_input_value == "grade term":
                            robot_actions.key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT)
                        else:
                            robot_actions.send_keys(Keys.TAB)
                        print(repetition)
                        time.sleep(.03)  #

                        # print("\nTab")
                    print("done tabbing!")
                    robot_actions.perform()
                    time.sleep(.1) #

                time.sleep(1) # <---for the add assignment tab to load

                aspen_save_button = robot.find_element_by_name('saveButton').click()
                while len(robot.window_handles) > 1:
                    time.sleep(1) # <---for the add assignment tab to load
                robot.switch_to_window(robot.window_handles[0])

                try:
                    topic_bug_patch_try = Gclassrooms[course]['CourseWork'][task]['Gclassroom_topic']
                except:
                    Gclassrooms[course]['CourseWork'][task]['Gclassroom_topic'] = ""

                if 'test' not in Gclassrooms[course]['CourseWork'][task]['Gclassroom_topic'].lower() and 'quiz' not in Gclassrooms[course]['CourseWork'][task]['Gclassroom_topic'].lower() and 'exam' not in Gclassrooms[course]['CourseWork'][task]['Gclassroom_topic'].lower() and 'midterm' not in Gclassrooms[course]['CourseWork'][task]['Gclassroom_topic'].lower():
                    Gclassrooms[course]['CourseWork'][task]['ASPEN_courseWork_values']['category']['ASPEN_value'] = 'completion'
                    Gclassrooms[course]['CourseWork'][task]['ASPEN_courseWork_values']['GB column name']['ASPEN_value'] = \
                        Gclassrooms[course]['CourseWork'][task]['ASPEN_courseWork_values']['GB column name']['ASPEN_value'].replace("-K","-C")

                    print(colored("\t\t" + task + " --------- " + "Completion", 'blue'))

                    robot.find_element_by_css_selector("body").send_keys(Keys.CONTROL, "a")
                    while len(robot.window_handles) == 1:
                        time.sleep(1)  # <---for the add assignment tab to load
                    robot.switch_to_window(robot.window_handles[1])

                    robot_actions = ActionChains(robot)
                    # The following goes to the "Visibility Type" In aspen and makes it public
                    for repetition in range(19):
                        robot_actions.send_keys(Keys.TAB)
                    for repetition in range(2):
                        robot_actions.send_keys(Keys.ARROW_LEFT)
                    for repetition in range(4):
                        robot_actions.send_keys(Keys.TAB)
                    robot_actions.perform()
                    for ASPEN_input_value in Gclassrooms[course]['CourseWork'][task]['ASPEN_coursework_categories']:
                        robot_actions = ActionChains(robot)
                        robot_actions.send_keys(
                            Gclassrooms[course]['CourseWork'][task]['ASPEN_courseWork_values'][ASPEN_input_value][
                                'ASPEN_value'])
                        print(Gclassrooms[course]['CourseWork'][task]['ASPEN_courseWork_values'][ASPEN_input_value]['ASPEN_value'])
                        for repetition in range(
                                Gclassrooms[course]['CourseWork'][task]['ASPEN_courseWork_values'][ASPEN_input_value][
                                    'num_of_tabs']):

                            if Gclassrooms[course]['CourseWork'][task]['ASPEN_courseWork_values'][ASPEN_input_value]['ASPEN_value'] == 'completion':
                                Gclassrooms[course]['CourseWork'][task]['ASPEN_courseWork_values']['Total points']['ASPEN_value'] = 1

                            if ASPEN_input_value == "grade term":
                                robot_actions.key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT)
                            else:
                                robot_actions.send_keys(Keys.TAB)
                                time.sleep(.02)  #
                            # print("\nTab")
                        robot_actions.perform()

                    aspen_save_button = robot.find_element_by_name('saveButton').click()
                    while len(robot.window_handles) > 1:
                        time.sleep(1)  # <---for the add assignment tab to load
                    robot.switch_to_window(robot.window_handles[0])


                courseWork = {
                    'title': Gclassrooms[course]['CourseWork'][task]['title'] + flag,
                }
                service.courses().courseWork().patch(
                    courseId=Gclassrooms[course]['CourseWork'][task]['courseId'],
                    id=Gclassrooms[course]['CourseWork'][task]['id'],
                    updateMask='title',
                    body=courseWork
                ).execute()
    robot.close()
add_assignments_to_ASPEN(Gclassrooms_dictionary,path_were_the_Google_webdriver_is_stored,Gclassroom_service)

def remove_flag(Gclassrooms, service):
    for course in Gclassrooms.keys():
        for task in Gclassrooms[course]['CourseWork'].keys():
            # print(task + " ---- " + Gclassrooms[course]['CourseWork'][task]['description'] + " ---- " + Gclassrooms[course]['CourseWork'][task]['courseId'] + " ---- " + Gclassrooms[course]['CourseWork'][task]['id'])
            courseWork = {
                'title': Gclassrooms[course]['CourseWork'][task]['title'].replace(flag,""),
            }
            service.courses().courseWork().patch(
                courseId=Gclassrooms[course]['CourseWork'][task]['courseId'],
                id=Gclassrooms[course]['CourseWork'][task]['id'],
                updateMask='title',
                body=courseWork
            ).execute()
    print("Flags removed from the Gclassrooms")
# remove_flag(Gclassrooms_dictionary,Gclassroom_service)