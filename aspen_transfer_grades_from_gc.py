from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from generate_classroom_credential import generate_classroom_credential
from selenium.webdriver.common.action_chains import ActionChains

import re
import time
from webdriver_manager.chrome import ChromeDriverManager
import datetime
import sqlite3
from sqlite3 import Error
from helper_functions.db_functions import create_connection

def create_table(p_db_conn):
    sql = 'CREATE TABLE IF NOT EXISTS recorded_scores (id varchar(60) PRIMARY KEY, assignment varchar(60),' \
          'name varchar(60), score integer NOT NULL );'
    try:
        c = p_db_conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)


def query_record(p_db_conn, p_id, p_score):
    sql = 'select * from recorded_scores WHERE id ="' + p_id + '" AND score =' + str(p_score)
    p_rows = ''
    try:
        cursor = p_db_conn.cursor()
        cursor.execute(sql)
        p_rows = cursor.fetchall()
    except Error as e:
        print(e)
    return p_rows


def insert_record(p_db_conn, p_id, p_score, p_assignment, p_name):
    sql = 'INSERT INTO recorded_scores VALUES ("' + p_id + '", "' + p_assignment + '", "' + p_name + '", ' + \
            str(p_score) + ' )'
    print(sql)
    try:
        cursor = p_db_conn.cursor()
        cursor.execute(sql)
        p_db_conn.commit()
    except Error as e:
        print(e)


def convert_assignment_name(p_name):
    """
    :param p_name:  name of assignment in Google classroom
    :return: name of assignment in column form aspen form
    """
    new_title = p_name
    new_title = re.sub('Python ', 'py', new_title)
    new_title = re.sub('Scratch ', 'Sc', new_title)
    new_title = re.sub('Autograder', 'AG', new_title)
    new_title = re.sub('Encryption', 'Encrp', new_title)
    new_title = re.sub(r'Final\sreview', 'Frev', new_title, re.X | re.S | re.M)
    print("New title is this " + str(new_title))
    if re.search(r"extra \s credit", new_title.lower(), re.X | re.M | re.S):
        return 'SKIP'
    if re.search(r"create \s task \s checkin", new_title.lower(), re.X | re.M | re.S):
        return 'SKIP'
    if len(new_title) >= 7:
        column_name = new_title[:7] + '-K'
    else:
        column_name = new_title + '-K'
    return column_name


def find_scholar_aspen_id(p_name, aspen_name_dict):
    """
    :param p_name:  name of scholar in Google classroom (string)
    :param aspen_name_dict: dictionaries with student ID and name (dict of strings)
    :return: id of scholar in aspen (str)
    """
    import re

    p_name = p_name.lower()
    g_name_parts = p_name.split()

    # Check for last name match
    candidate_matches = []
    for p_key in aspen_name_dict.keys():
        a_name = p_key.lower()
        a_name_parts = a_name.split(', ')
        if re.search(g_name_parts[-1], a_name_parts[0]):
            candidate_matches.append(p_key)
    if len(candidate_matches) == 1:
        # ony matched one, found it
        return aspen_name_dict[candidate_matches[0]]
    else:
        first_name_matches = []
        for match in candidate_matches:
            print(match)
            match_parts = match.lower().split(', ')
            print(g_name_parts[0])
            if re.search(g_name_parts[0], match_parts[-1]):
                first_name_matches.append(match)
        if len(first_name_matches) == 1:
            return aspen_name_dict[first_name_matches[0]]


def get_assignments_from_classroom(course_id, p_quarter_start_obj):
    """

    :param course_id: Google classroom course ID (string)
    :param p_quarter_start_obj: start of the quarter, datetime format
    :return: dictionary.  Keys are assignment names, value is a list with items [student name, score] i.e. nested list
    """
    from generate_classroom_credential import generate_classroom_credential

    # Read from Google classroom
    p_service_classroom = generate_classroom_credential()

    # Getting students
    students = p_service_classroom.courses().students().list(courseId=course_id,).execute()
    students = students['students']
    gc_students = {}
    print("In getting_assignments, getting students")
    for student in students:
        p_student_id = student['userId']
        student_profiles = p_service_classroom.userProfiles().\
            get(userId=p_student_id,).execute()
        print(student_profiles)
        # print(student_profiles['emailAddress'])
        gc_students[p_student_id] = student_profiles['name']['fullName']
    print(gc_students)
    print("Getting assignments")
    p_courseworks = p_service_classroom.courses().\
        courseWork().list(courseId=course_id).execute().get('courseWork', [])
    assignments_scores_to_aspen = {}
    for coursework in p_courseworks:
        coursework_id = coursework['id']
        coursework_title = coursework['title']
        # print(coursework)
        if 'dueDate' in coursework:
            due_date = coursework['dueDate']
            due_date_obj = datetime.datetime(due_date['year'], due_date['month'], due_date['day'])
            print(f"Coursework {coursework} duedate {due_date_obj} quarter {p_quarter_start_obj}")
            if due_date_obj > p_quarter_start_obj:
                student_works = p_service_classroom.courses(). \
                    courseWork().studentSubmissions().list(courseId=COURSE_ID, courseWorkId=coursework_id).execute()
                student_works = student_works['studentSubmissions']
                for student_work in student_works:
                    # print(f"STUDENT WORK {student_work}")
                    if 'assignedGrade' in student_work.keys():
                        # print("yes")
                        if student_work['state'] == 'RETURNED':
                            print(f"doing this one:  {student_work}")
                            print(coursework_title)
                            print(assignments_scores_to_aspen)
                            coursework_title = re.sub(r'\s:-\)', '', coursework_title)
                            p_student_id = student_work['userId']
                            student_name = gc_students[p_student_id]
                            grade = student_work['assignedGrade']
                            # print(f"grade {grade} student id {student_id} student name {student_name}")

                            if coursework_title in assignments_scores_to_aspen.keys():
                                assignments_scores_to_aspen[coursework_title].append([student_name, grade])
                            else:
                                assignments_scores_to_aspen[coursework_title] = [[student_name, grade]]
    return assignments_scores_to_aspen


COURSE = 'T608-IP-004'
COURSE_ID = 253721407705
quarter = 4
quarter_start_obj = datetime.datetime(2021, 4, 10)


assignments_from_classroom_dict = get_assignments_from_classroom(COURSE_ID, quarter_start_obj)
print("These are the assignments from Google classroom!")
print(assignments_from_classroom_dict)
chrome_options = Options()
chrome_options.add_argument("Window-size=6500,12000")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
driver.get('https://aspen.cpsd.us')

# Logon
try:
    element = WebDriverWait(driver, 10).\
        until(ec.presence_of_element_located((By.XPATH, "//input[@class='logonInput']")))
except TimeoutException:
    print("Did not find logon screen")
    print("quitting")
    driver.quit()
login = driver.find_element_by_xpath("//input[@class='logonInput']").send_keys('ewu')
password = driver.find_element_by_xpath("//input[@name='password']").send_keys('Dimmy123$')
submit = driver.find_element_by_xpath("//button").click()
submit2 = driver.find_element_by_xpath("//a[@title='Gradebook tab']").click()

# Select course
try:
    element = WebDriverWait(driver, 10).\
        until(ec.presence_of_element_located((By.XPATH, "//a[text()='" + COURSE + "']")))
except TimeoutException:
    print("Did not find Course in Aspen ")
    print("quitting")
    driver.quit()
submit3 = driver.find_element_by_xpath("//a[text()='" + COURSE + "']").click()

print("found course looking for scores")
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Click Scores
time.sleep(1)
# try:
#     element = WebDriverWait(driver, 10).\
#         until(ec.presence_of_element_located((By.XPATH, "//a[@title='Gradebook grade input']")))
#    element = WebDriverWait(driver, 5).\
#        until(ec.presence_of_element_located((By.XPATH, "//a[@href='javascript*']")))
# except TimeoutException:
#     print("Did not find scores in Aspen ")
#     print(TimeoutException.message)
#     print("quitting")
#     driver.quit()
print("Trying to switch to correct quarter")
submit4 = driver.find_element_by_xpath("//a[@title='List of assignment records']").click()

submit51 = driver.find_element_by_xpath('//*[@id="filterMenu"]').click()
window_before = driver.window_handles[0]

submit6 = driver.find_element_by_xpath('//*[@id="filterMenu_Option2"]/td[2]').click()
window_after = driver.window_handles[1]

driver.switch_to.window(window_after)

submit888 = driver.find_elements_by_xpath('//input')
for element in submit888:
    print(element.get_attribute('name'))
submit7 = driver.find_element_by_xpath('//input[@name="value(prompt1)"]')
# name="value(prompt1)"
submit7.click()
keys = 'Q' + str(quarter)
submit7.send_keys(keys)
submit8 = driver.find_element_by_xpath('//*[@id="submitButton"]').click()
driver.switch_to.window(window_before)


# find the table of assignments
print("Trying to find table of assignments")
try:
    element = WebDriverWait(driver, 10).\
        until(ec.presence_of_element_located((By.XPATH, "//div[@id='dataGrid']")))
except TimeoutException:
    print("Did not find  assignment in Aspen ")
    print("quitting")
    driver.quit()

columns = 16

# Get assignments and data
aspen_assignment_ids = {}
done = False

while done is False:

    # get rows
    rows = len(driver.find_elements_by_xpath("//tr[@class='listCell listRowHeight   ']"))
    print(f"rows {rows}")

    # get one element test
    el = driver.find_element_by_xpath("//*[@id='dataGrid']/table/tbody/tr[2]/td[8]")
    # print(el.text)
    for i in range(2, rows + 2):
        xpath_string = '//*[@id="dataGrid"]/table/tbody/tr[' + str(i) + ']/td[2]'
        el = driver.find_element_by_xpath(xpath_string)
        assignment_id = el.get_attribute('id')
        xpath_string = '//*[@id="dataGrid"]/table/tbody/tr[' + str(i) + ']/td[8]'
        el = driver.find_element_by_xpath(xpath_string)
        assignment_name = el.text
        print(f"Element ID: {assignment_id} Element name {assignment_name}")
        if re.search('-K$', assignment_name) or re.search('-C$', assignment_name) :
            aspen_assignment_ids[assignment_name] = assignment_id
    try:
        button = driver.find_element_by_xpath('//*[@id="topnextPageButton"]')
        disabled = button.get_attribute('disabled')
        print(disabled)
        if disabled is None:
            clicked = button.click()
        elif disabled:
            done = True
    except NoSuchElementException:
        done = True

# get list of names and IDs:

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# print("WAITING")
# time.sleep(4)
id_scholars = {}
# delete line? scr = driver.find_element_by_xpath("//div[@class='scrollCell invisible-horizontal-scrollbar']")
height = 0


# get list of names and IDs:
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


time.sleep(1)
# should do some try excep magic here
submit4 = driver.find_element_by_xpath("//a[@title='Gradebook grade input']").click()

# Select current quarter
try:
    element = WebDriverWait(driver, 10).\
        until(ec.
              presence_of_element_located((By.XPATH, "//select[@name='termFilter']")))
except TimeoutException:
    print("Did not find termfilter")
    print("quitting")
    driver.quit()


submit5 = driver.find_element_by_xpath(
    "//select[@name='termFilter']/option[text()='Q" + str(quarter) + "']").click()

# change to grade columns ALL
try:
    element = WebDriverWait(driver, 10).\
        until(ec.presence_of_element_located
                            ((By.XPATH, '//*[@id="contentArea"]/table[2]/tbody/tr[1]/td[2]/table[3]/tbody/tr[2]/td[1]/table/tbody/tr/td[1]/select')))
except TimeoutException:
    print("Did not find Pull down menu w/Grade columns in Aspen ")
    print("quitting")
    driver.quit()
driver.find_element_by_xpath('//*[@id="contentArea"]/table[2]/tbody/tr[1]/td[2]/table[3]/tbody/tr[2]/td[1]/table/tbody/tr/td[1]/select/option[1]').click()


id_scholars = {}
# scr = driver.find_element_by_xpath("//div[@class='scrollCell invisible-horizontal-scrollbar']")

try:
    element = WebDriverWait(driver, 10).\
        until(ec.
              presence_of_element_located((By.XPATH, "//div[@class='scrollCell invisible-horizontal-scrollbar']")))
except TimeoutException:
    print("Did not find scrollbar ")
    print("quitting")
    driver.quit()

id_scholars = {}
scr = driver.find_element_by_xpath("//div[@class='scrollCell invisible-horizontal-scrollbar']")
height = 0

try:
    element = WebDriverWait(driver, 10).\
        until(ec.
              presence_of_element_located((By.XPATH, "//a")))
except TimeoutException:
    print("Did not find a href elements ")
    print("quitting")
    driver.quit()

old_names = []
for i in range(10):
    names = driver.find_elements_by_xpath("//a")
    counter = 0
    new_names = []
    for a in names:
        a_attrib = a.get_attribute('href')
        if re.search('openGradeInputDetail', a_attrib) and \
                (re.search('STD', a_attrib) or re.search('std', a_attrib)):
            match_obj = re.match(r"javascript:openGradeInputDetail\('((std|STD).+)'\)",
                                 a_attrib, re.X | re.M | re.S)
            first_id = match_obj.group(1)
            name = a.text
            if name:
                new_names.append(name)
                id_scholars[name] = first_id
    new_names.sort()
    old_names.sort()
    if new_names == old_names:
        break
    else:
        old_names = new_names
        height += 120
        driver.execute_script("arguments[0].scrollTo(0," + str(height) + ") ", scr)

print(id_scholars)

print(aspen_assignment_ids)

# Read from Google classroom
service_classroom = generate_classroom_credential()
print("Getting assignments")
courseworks = service_classroom.courses().courseWork().list(courseId=COURSE_ID).execute().get('courseWork', [])


# Input to aspen!
db_filename = COURSE + '.db'
db_conn = create_connection(db_filename)
create_table(db_conn)

for key in assignments_from_classroom_dict.keys():
    test_assignment = key
    scores = assignments_from_classroom_dict[key]
    test_name = ''
    test_score = 0
    for entry in scores:
        test_name = entry[0]
        test_score = entry[1]

        print(f"test assignment {test_assignment} test_name {test_name} test_score {test_score}")

# test_assignment = 'test assignment'
# test_score = 100
# test_name = 'Shahnawaz Fakir'

        assignment_aspen = convert_assignment_name(test_assignment)
        # print(assignment_aspen_id)
        scholar_aspen_id = find_scholar_aspen_id(test_name, id_scholars)
        # print(scholar_aspen_id)

        cell_id = aspen_assignment_ids[assignment_aspen] + '|' + scholar_aspen_id
        edit_cell_id = 'e' + cell_id
        completion_assignment = assignment_aspen
        completion_assignment = re.sub('-K$', '-C', completion_assignment)
        cell2_id = aspen_assignment_ids[completion_assignment] + '|' + scholar_aspen_id
        edit_cell2_id = 'e' + cell2_id
        # print(cell_id)
        # print(edit_cell_id)

        rows = query_record(db_conn, cell_id, test_score)
        temp_words = cell_id.split('|')
        student_id = temp_words[1]
        test_name = ''
        for key2 in id_scholars:
            # print(f"key {key} student {student_id} value {id_scholars[key]}")
            if id_scholars[key2] == student_id:
                print(f"YES     key {key} student {student_id} value {id_scholars[key2]}")
                test_name = key2
        print(f"This is what the query returns {rows} ")
        if len(rows) == 0:
            grade_element = driver.find_element_by_id(cell_id)
            # create action chain object
            action = ActionChains(driver)
            action.move_to_element(grade_element).perform()

            grade_element.click()
            grade_element2 = driver.find_element_by_id(edit_cell_id)
            grade_element2.send_keys(test_score)
            grade_element2.send_keys(Keys.RETURN)

            grade_element3 = driver.find_element_by_id(cell2_id)
            # create action chain object
            action = ActionChains(driver)
            action.move_to_element(grade_element3).perform()
            grade_element3.click()
            grade_element4 = driver.find_element_by_id(edit_cell2_id)
            grade_element4.send_keys('1')
            grade_element4.send_keys(Keys.RETURN)

            insert_record(db_conn, cell_id, test_score, test_assignment, test_name)
            print(f"adding  this record.  Assignment: {test_assignment} scholar: {test_name} score: {test_score}")

        else:
            print(f"Record is in the DB already.  Assignment: {test_assignment} scholar: {test_name} score: {test_score}")
