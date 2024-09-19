import datetime
import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from helper_functions.skills_functions import skills_login, which_rotation
from helper_functions.skills_functions import generate_driver as generate_skills_driver
from helper_functions.aspen_functions import generate_driver, aspen_login, add_assignments, \
    check_new_aspen_names, get_assignments_from_aspen, goto_assignments, \
    goto_assignments_this_quarter, get_assignments_and_assignment_ids_from_aspen, goto_scores_this_quarter, \
    get_student_ids_from_aspen, wait_for_element_clickable, match_gc_name_with_aspen_id, click_button
from classroom_grades_to_aspen import classroom_grades_to_aspen
from helper_functions.db_functions import create_connection, execute_sql, query_db
import getpass
from helper_functions.quarters import which_quarter_today, which_quarter_today_string, which_next_quarter
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

now = datetime.datetime.now()
aspen_username = input("Give me your aspen username (include .cpsd.us, i.e. ewu@cpsd.us) ")
aspen_password = getpass.getpass('Give me the password for Aspen ')
# programs = ['Info Technology']
programs = ['Biotechnology']
programs = ['Culinary Arts']
# programs_dict = {'Biotechnology': {'letter': 'B'},
#                  'Info Technology': {'letter': 'L'}}
programs_dict = {
                 'Early Ed & Care': {'letter': 'G'}}
programs_dict = {
                 'Info Technology': {'letter': 'L'}}
programs_dict = {'Biotechnology': {'letter': 'B'}}

course_prefix = 'T120'
course_letter = 'L'
course_letter = 'B'

t_username = 'ewu@cpsd.us'
t_password = 'silverstreet11'
p_content_knowledge_completion = False
dates = ['9/3/2024',
         '9/4/2024',
         '9/5/2024',
         '9/6/2024',
         '9/9/2024',
         '9/10/2024',
         '9/11/2024',
         '9/12/2024',
         '9/13/2024',
         '9/16/2024',
         '9/17/2024',
         '9/18/2024',
         '9/19/2024',
         '9/20/2024',
         '9/23/2024',
         '9/24/2024',
         '9/25/2024',
         '9/26/2024',
         '9/27/2024',
         '9/30/2024',
         '10/1/2024',
         '10/2/2024',
         '10/4/2024',
         '10/7/2024',
         '10/8/2024',
         '10/9/2024',
         '10/10/2024',
         '10/11/2024',
         '10/15/2024',
         '10/16/2024',
         '10/17/2024',
         '10/18/2024',
         '10/21/2024',
         '10/22/2024',
         '10/23/2024',
         '10/24/2024',
         '10/25/2024',
         '10/28/2024',
         '10/29/2024',
         '10/30/2024',
         '10/31/2024',
         '11/1/2024',
         '11/4/2024',
         '11/6/2024',
         '11/7/2024',
         '11/8/2024',
         '11/12/2024',
         '11/13/2024',
         '11/14/2024',
         '11/15/2024',
         '11/18/2024',
         '11/19/2024',
         '11/20/2024',
         '11/21/2024',
         '11/22/2024',
         '11/25/2024',
         '11/26/2024',
         '11/27/2024',
         '12/2/2024',
         '12/3/2024',
         '12/4/2024',
         '12/5/2024',
         '12/6/2024',
         '12/9/2024',
         '12/10/2024',
         '12/11/2024',
         '12/12/2024',
         '12/13/2024',
         '12/16/2024',
         '12/17/2024',
         '12/18/2024',
         '12/19/2024',
         '12/20/2024',
         '12/23/2024',
         '1/3/2025',
         '1/6/2025',
         '1/7/2025',
         '1/8/2025',
         '1/9/2025',
         '1/10/2025',
         '1/13/2025',
         '1/14/2025',
         '1/15/2025',
         '1/16/2025',
         '1/17/2025'
         ]
rotation_change = [
    2,
    6,
    9,
    13,
    17,
    20,
    24,
    28,
    32,
    35,
    38,
    43,
    59,
    75,
]


# course_letter = 'B' # BioTech


# Figure out what days are already done
all_completed_days = []
for rotation_number in range(1, 12):

    if rotation_number < 10:
        course_number = course_prefix + course_letter + '-I-00' + str(rotation_number)
    else:
        course_number = course_prefix + course_letter + '-I-0' + str(rotation_number)
    db_filename = 'database_gc_grades_put_in_aspen_' + course_number + '.db'

    db_conn = create_connection(db_filename)

    sql = 'CREATE TABLE IF NOT EXISTS  "completed_days" ("id"	varchar(60),  PRIMARY KEY("id"));'
    execute_sql(db_conn, sql)

    sql = 'SELECT * FROM completed_days;'
    style = ''
    rows = query_db(db_conn, sql)
    completed_days = [x[0] for x in rows]
    # this_class_posted_assignments = set(this_class_posted_assignments)
    all_completed_days.extend(completed_days)
    # print(f"all previous assignment now {all_previous_assignments}")

print(f"final all  completed days {all_completed_days}")


driver = generate_skills_driver()
skills_login(driver,  username=t_username, password=t_password)

# Extract data from skills
for program in programs_dict.keys():
    print(f"Clicking program {program}")
    select = Select(driver.find_element(By.ID, 'whatprogramnumber'))
    # select by visible text
    select.select_by_visible_text(program)
    choose = click_button(driver, By.XPATH, '/html/body/div/div/section/div/div[2]/form/fieldset/input', 2)
    # choose = driver.find_element(By.XPATH, '/html/body/div/div/section/div/div[2]/form/fieldset/input')
    # choose.click()

    # Choose date
    grade_dict = {}
    for day_number in range(2, 90):  # each assignment
        print(f"Here is the date! {dates[day_number - 1]}")

        # Don't read days you've already finished putting into aspen
        day_string = 'day_' + str(day_number)
        if day_string in all_completed_days:
            print(f"Done this day already, skip the reading {day_string}")
            continue

        # Don't read grades for days after today
        current_date_obj = datetime.datetime.strptime(dates[day_number - 1], '%m/%d/%Y')
        print(current_date_obj)
        if current_date_obj > now:
            print("no need to read in grades after today: breaking")
            break

        grade_dict[day_number] = {}
        print(f"trying a date with this index {day_number}")
        select = Select(driver.find_element(By.ID, 'choosedate'))
        print("chose date")
        time.sleep(1)
        select.select_by_index(day_number)
        select_day = driver.find_element(By.XPATH, '//*[@id="frm2"]/fieldset/input')
        continue_button = click_button(driver, By.XPATH, '//*[@id="frm2"]/fieldset/input', 2, )

        print("about to get everybody's grade")
        for student_number in range(2, 25):
            try:
                id_xpath = f'/html/body/div/fieldset[1]/form/table/tbody/tr[{student_number}]/td[3]'
                grade_xpath = f'/html/body/div/fieldset[1]/form/table/tbody/tr[{student_number}]/td[9]'
                # try:
                id = driver.find_element(By.XPATH, id_xpath).text
                # print(id)
                grade = driver.find_element(By.XPATH, grade_xpath).text
                # print(grade_dict)
                grade_dict[day_number][id] = grade
                # print(grade_dict)
            except NoSuchElementException:
                break
        time.sleep(1)

    # raise Exception("stop testing")

    # all done reading from Skills for this program
    print(f"this is the grade dictionary {grade_dict}")
    print("final sleeping")
    driver.close()
# # {1:[{2:{}}, {3:{}}, {4:{}}]   }
# # key 2, 3, 4, 5 (day)
# # val dict {id: grade}
#
# # key 1 2 3  (rotation
# # val {2: {val dict} , 3: {val dict}}
    final_aspen_grade_dict = {}
    for day in grade_dict.keys():  # assignment
        rotation = which_rotation(rotation_change, day)
        if rotation in final_aspen_grade_dict.keys():
            final_aspen_grade_dict[rotation][day] = grade_dict[day]
        else:
            final_aspen_grade_dict[rotation] = {}
            final_aspen_grade_dict[rotation][day] = grade_dict[day]
    print("format: first number, rotation.  second number day.  3rd: dict of ID and grades")
    for rotation in final_aspen_grade_dict.keys():
        print(f"rotation {rotation}")
        rotation_grades_dict = final_aspen_grade_dict[rotation]
        for day in rotation_grades_dict.keys():
            print(f"     day: {day}  grades: {rotation_grades_dict[day]}")

    # rotation 1
    #      day: 2  grades: {'8000613': '96', '8000671': '95', '8001990': '92.7', '8000663': '93', '8005951': '95.7', '8000905': '95.3', '8012709': '95', '
    # 8014819': '95', '8015613': '92.7', '8000537': '95.3', '8002254': '95.3', '7003389': '96', '8012285': '95.3', '8001478': '95.3', '8001762': '96.3'}
    #      day: 3  grades: {'8000613': '95', '8000671': '95', '8001990': '93.3', '8000663': '96', '8005951': '96', '8000905': '95', '8012709': '80', '8014
    # 819': '95', '8015613': '95', '8000537': '95', '8002254': '95.7', '7003389': '96', '8012285': '81', '8001478': '96', '8001762': '80'}
    #      day: 4  grades: {'8000613': '96', '8000671': '98', '8001990': '76.7', '8000663': '94', '8005951': '97.3', '8000905': '95', '8012709': '76.7', '
    # 8014819': '91.7', '8015613': '83.3', '8000537': '83.3', '8002254': '86.7', '7003389': '97.3', '8012285': '76.7', '8001478': '97.3', '8001762': '76.7'8000613': '0', '8000671': '0', '8001990': '0', '8000663': '0', '8005951': '0', '8000905': '0', '8012709': '0', '8014819': '0', '8015613': '0', '8000537': '0', '8002254': '0', '7003389': '0', '8012285': '0', '8001478': '0', '8001762': '0'}}}

    print("FINAL FINAL")
#     final_aspen_grade_dict = {1:
#                                 {2: {'Aklilu, Helam': '96', 'Austin-Realpe, Gaspar': '95', 'Charles, Kayli': '92.7', 'De Sola, Roland': '93', 'Gray-Pai, Iyla': '95.7', 'Mengesha, Nardose': '95.3', 'Murphy, Mairenn': '95',   'Pantoja Morales, Hillary Valentina': '95',   'Parham Freeman, Raziyah': '92.7', 'Pollard-Pearson, Leah': '95.3', 'Rashid, Zulekha': '95.3', 'Rivas, Langdon': '96',   'Saintil, Dany': '95.3', 'Shacklewood, Jessica': '95.3', 'Yard-Findley, Malia': '96.3'},
#                                  3: {'Aklilu, Helam': '95', 'Austin-Realpe, Gaspar': '95', 'Charles, Kayli': '93.3', 'De Sola, Roland': '96', 'Gray-Pai, Iyla': '96',   'Mengesha, Nardose': '95',   'Murphy, Mairenn': '80',   'Pantoja Morales, Hillary Valentina': '95',   'Parham Freeman, Raziyah': '95',   'Pollard-Pearson, Leah': '95',   'Rashid, Zulekha': '95.7', 'Rivas, Langdon': '96',   'Saintil, Dany': '81',   'Shacklewood, Jessica': '96',  'Yard-Findley, Malia': '80'},
#                                  4: {'Aklilu, Helam': '96', 'Austin-Realpe, Gaspar': '98', 'Charles, Kayli': '76.7', 'De Sola, Roland': '94', 'Gray-Pai, Iyla': '97.3', 'Mengesha, Nardose': '95',   'Murphy, Mairenn': '76.7', 'Pantoja Morales, Hillary Valentina': '91.7', 'Parham Freeman, Raziyah': '83.3', 'Pollard-Pearson, Leah': '83.3', 'Rashid, Zulekha': '86.7', 'Rivas, Langdon': '97.3', 'Saintil, Dany': '76.7', 'Shacklewood, Jessica': '97.3', 'Yard-Findley, Malia': '76.7'},
#                                  5: {'Aklilu, Helam': '95', 'Austin-Realpe, Gaspar': '97', 'Charles, Kayli': '95', 'De Sola, Roland': '95', 'Gray-Pai, Iyla': '95', 'Mengesha, Nardose': '95', 'Murphy, Mairenn': '95', 'Pantoja Morales, Hillary Valentina': '95', 'Parham Freeman, Raziyah': '95', 'Pollard-Pearson, Leah': '95', 'Rashid, Zulekha':'95', 'Rivas, Langdon': '95.3', 'Saintil, Dany': '95', 'Shacklewood, Jessica': '95.3', 'Yard-Findley, Malia': '95'}},
#                               2: {6: {'Armitage, Ella': '95.7', 'Beard, Sydney': '97.3', 'Caporiccio, Ziamara': '90.3', 'Dacosta, Ari': '97.3', 'Fisher Seufert, Abigail': '95.3', 'Hailegiorgis, Amanuel': '87', 'Hicks, Kenji': '0', 'Jean, Ishmaiah': '97', 'McNamara, Giselle': '87', 'Norman, William': '90.3', 'Poulain, Madeleine': '90.3', 'Scott, Benjamin': '95.3', 'Utsugi, Mei': '7.3', 'Younker, Alisandra': '98'},
#                                   7: {'Armitage, Ella': '95.7', 'Beard, Sydney': '97.3', 'Caporiccio, Ziamara': '90.3','Dacosta, Ari': '97.3', 'Fisher Seufert, Abigail': '95.3', 'Hailegiorgis, Amanuel': '87', 'Hicks, Kenji': '0', 'Jean, Ishmaiah': '97', 'McNamara, Giselle': '87', 'Norman, William': '90.3', 'Poulain, Madeleine': '90.3', 'Scott, Benjamin': '95.3', 'Utsugi, Mei': '97.3', 'Younker, Alisandra': '98'},
#                                   8: {'Armitage, Ella': '95', 'Beard, Sydney': '91.7', 'Caporiccio, Ziamara': '95', 'Dacosta, Ari': '95', 'Fisher Seufert, Abigail': '91.7', 'Hailegiorgis, Amanuel': '91.7', 'Hicks, Kenji': '0', 'Jean, Ishmaiah': '95', 'McNamara, Giselle': '75', 'Norman, William': '81.7', 'Poulain, Madeleine': '91.7', 'Scott, Benjamin': '78.3', 'Utsugi, Mei': '97', 'Younker, Alisandra': '91.7'}},
#                               3: {9: {'Alvarado, Christian': '0', 'Beard, Thomas': '95', 'Bernard, Briana': '95.7', 'Cali, Anisa': '0', 'Chandler, Lorelei': '95', 'Chernov, Lila': '95', 'Conrad, Maxx': '95', 'Crittenden, Jimmy': '95', 'Day-Williams, Emma': '95', 'Flackett, Dashiell': '95', 'Inocente, Isadora': '96', 'Kelsey, Henry': '95.3', 'Okbagzy, Gelilah': '95', 'Paris, Neveah': '97.3', 'Poitevien, Lissa-Geriane': '0'},
#                                   10: {'Alvarado, Christian': '0', 'Beard, Thomas': '95', 'Bernard, Briana': '95', 'Cali, Anisa': '0', 'Chandler, Lorelei': '95', 'Chernov, Lila': '95', 'Conrad, Maxx': '95', 'Crittenden, Jimmy': '95', 'Day-Williams, Emma': '95', 'Flackett, Dashiell': '95', 'Inocente, Isadora': '95', 'Kelsey, Henry': '95', 'Okbagzy, Gelilah': '95', 'Paris, Neveah': '95', 'Poitevien, Lissa-Geriane': '0'},
#                                   11: {'Alvarado, Christian': '95', 'Beard, Thomas': '95', 'Bernard, Briana': '95', 'Cali, Anisa': '0', 'Chandler, Lorelei': '95', 'Chernov, Lila': '95', 'Conrad, Maxx': '95', 'Crittenden, Jimmy': '96', 'Day-Williams, Emma': '98.3', 'Flackett, Dashiell': '95.3', 'Inocente, Isadora': '95', 'Kelsey, Henry': '95', 'Okbagzy, Gelilah': '96', 'Paris, Neveah': '100', 'Poitevien, Lissa-Geriane': '0'}}}
# # print(final_aspen_grade_dict)

    # program = 'Info Technology'
    # Figure out what is done



    # Here is the aspen part
    for rotation in final_aspen_grade_dict.keys():
        # Rotation gives the course number
        rotation_grades_dict = final_aspen_grade_dict[rotation]
        # Keys are day, values are dicts {ID: score}
        for key in rotation_grades_dict.keys():
            # All dictionaries for a particular rotation have same # of students
            num_students = len(rotation_grades_dict[key])
            break

        # Get rid of ones already done
        new_rotation_grades_dict = {}
        for day in rotation_grades_dict:
            day_string = 'day_' + str(day)
            if day_string not in all_completed_days:
                new_rotation_grades_dict[day] = rotation_grades_dict[day]
        rotation_grades_dict = new_rotation_grades_dict
        print(f"Here is the dictionary after removing ones already done {rotation_grades_dict}")

        print(f"Number of students in this rotation {rotation} is this: {num_students} ")
        print(f"final go around.  This is the rotation {rotation} ")
        program_letter = programs_dict[program]['letter']  # add a variable later
        if int(rotation) < 10:
            course_number = course_prefix + program_letter + '-I-' + '00' + str(rotation)
        else:
            course_number = course_prefix + program_letter + '-I-' + '0' + str(rotation)
        print(f"course number is this: {course_number} ")

        print("Opening DB/getting students")
        db_filename = 'database_gc_grades_put_in_aspen_' + course_number + '.db'
        db_conn = create_connection(db_filename)
        # sql = 'CREATE TABLE IF NOT EXISTS recorded_scores (id varchar(60) PRIMARY KEY, assignment varchar(60),' \
        #       'name varchar(60), score integer NOT NULL );'
        sql = 'CREATE TABLE IF NOT EXISTS  "recorded_scores" ("id"	varchar(60), "assignment"	varchar(60), ' \
              '"name"	varchar(60), "score" integer NOT NULL, PRIMARY KEY("id","score"));'
        execute_sql(db_conn, sql)
        sql = 'CREATE TABLE IF NOT EXISTS  "gc_students" ("id"	varchar(60), "name"	varchar(60), PRIMARY KEY("id"));'
        execute_sql(db_conn, sql)
        # skip student profiles
        print(f"This is the ")
        for key in final_aspen_grade_dict[rotation].keys():
            num_gc_students = len(final_aspen_grade_dict[rotation][key])
        print(f"This many students {num_gc_students}")
        sql = 'SELECT * FROM recorded_scores;'
        rows = query_db(db_conn, sql)
        print(f"rows from DB {rows} for this course {course_number}")
        if num_gc_students != 0:
            print("Opening up Aspen now")
            driver = generate_driver()
            aspen_login(driver, username=aspen_username, password=aspen_password)
            print("Getting this quarter's assignments from Aspen")
            quarter = which_quarter_today_string()
            goto_assignments_this_quarter(driver, course_number, quarter)
            aspen_assignments = get_assignments_and_assignment_ids_from_aspen(driver)
            print("Here are the aspen assignments and IDs from this quarter:")
            for key in aspen_assignments:
                print(f"{key}       {aspen_assignments[key]}")

        # Put in the scores
        students_done = False
        counter = 0
        while students_done is False:
            counter += 1
            print("Getting the Aspen student ID's")
            goto_scores_this_quarter(driver, course_number, quarter)
            print("Got the scores")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print("getting student IDs")
            aspen_students = get_student_ids_from_aspen(driver)
            print("here are the aspen student IDs")
            num_aspen_students = len(aspen_students)
            for key in aspen_students:
                print(f"{key}        {aspen_students[key]}")
            if len(aspen_students) + 6 > num_gc_students or counter > 10:
                students_done = True
        print("Putting in the grades now")
        good_load = False
        counter = 0

        print(f"number of students for this rotation is this: {num_students}")
        while good_load is False:
            time.sleep(1.0)
            # inputs = driver.find_elements_by_xpath('//tr')
            inputs = driver.find_elements(By.XPATH, '//tr')
            row_count = 0
            for p_input in inputs:
                # print('xxx')
                # print(p_input)
                if re.search(r'grdrow[0-9]+', p_input.get_attribute('id')):
                    row_count += 1
            if abs(row_count - num_students) > 3  and counter != 10:
                print('row count found in page' + str(row_count))
                # print(p_aspen_student_ids)
                print(f'Num students is {num_students}')
                # print('aspen student ids from original ' + str(len(p_aspen_student_ids)))
                print("Aspen bug in loading page, reloading now...")
                driver.get(driver.current_url)
                driver.refresh()
                wait_for_element_clickable(driver,
                                           p_xpath_el="//div[@class='scrollCell invisible-horizontal-scrollbar']")
                time.sleep(1.5)
                print("restarting, current counter is this: " + str(counter))
                counter += 1
            else:
                good_load = True
            if counter == 10:
                print("Could not get this page to work after 10 reloads! Try again later")
                raise ValueError
                good_load = False
        print("finished with the load of student grades in aspen!")

        p_assignments_from_classroom = rotation_grades_dict
        p_aspen_assignments = aspen_assignments
        print(f"p_aspen_assignments {p_aspen_assignments}")
        assignment_col_names = []
        for key in rotation_grades_dict.keys():
            assignment_col_names.append(key)

        for day_key in p_assignments_from_classroom.keys():

            gc_assignment_name = 'day_' + str(day_key)
            print(f"name scores is gonna be this {rotation_grades_dict[key]} and key is this {day_key}")
            name_scores = rotation_grades_dict[day_key]

            aspen_scholar_id = 1
            scores_put_in = 0 # check to see if over 7 are 0.  If so, skip
            num_zeros = 0
            for name_key in name_scores.keys():
                gc_score = name_scores[name_key]
                if gc_score == '0':
                    print("zero here")
                    num_zeros = num_zeros + 1
            if num_zeros > 7:
                print("over 7 0 scores - probably didn't fill out yet")
                continue
            for name_key in name_scores.keys():
                old_aspen_scholar_id = aspen_scholar_id
                skills_name = name_key
                gc_score = name_scores[name_key]
                if abs(float(gc_score)) < .01:
                    gc_score = 'EXC'
                    print("Score of 0, excused.  Keep on ")
                    # continue  # skip because didn't put this in
                [skills_lastname, skills_firstname] = skills_name.split(', ')
                skills_lastname = skills_lastname.lower()
                skills_firstname = skills_firstname.lower()
                print(f"Skills first {skills_firstname} and last {skills_lastname} and score is {gc_score}")
                # Match up names
                candidate_matches = []
                for orig_aspen_name in aspen_students.keys():
                    aspen_name = orig_aspen_name.lower()
                    # print(f"aspen name {aspen_name} and orig aspen name {orig_aspen_name}")

                    [aspen_lastname, aspen_firstname] = aspen_name.split(', ')
                    # print(f"aspen first {aspen_firstname} and aspen last {aspen_lastname}")
                    if re.search(skills_lastname, aspen_lastname):
                        candidate_matches.append(orig_aspen_name)
                        print(f"Match! {candidate_matches}")

                if len(candidate_matches) == 1:
                    # ony matched one, found it
                    aspen_scholar_id = aspen_students[candidate_matches[0]]
                else:
                    first_name_matches = []
                    for orig_aspen_name in aspen_students.keys():
                        aspen_name = orig_aspen_name.lower()
                        [aspen_lastname, aspen_firstname] = aspen_name.split(', ')
                        if re.search(skills_firstname, aspen_firstname):
                            first_name_matches.append(orig_aspen_name)
                    if len(first_name_matches) == 1:
                        aspen_scholar_= aspen_students[first_name_matches[0]]
                if old_aspen_scholar_id == aspen_scholar_id:
                    print(f"Could not a find a match for this student {skills_name} ")
                    print(f"In this {aspen_students}")
                    continue
                print(f"Before putting in.  ID and score {aspen_scholar_id} and {gc_score}")
                print(f"Looping over assignment col names {assignment_col_names}")
                # print(f"p_aspen assignments {p_aspen_assignments}")
                col_name = 'day_' + str(day_key)

                print(f"This is col name {col_name} and this is assignment keys {p_aspen_assignments}")
                if col_name in p_aspen_assignments.keys():
                    print("attempting")
                    try:
                        cell_id = p_aspen_assignments[col_name] + '|' + aspen_scholar_id
                        print(f"cell_id is this {cell_id}, assignment is {col_name} and aspen assignment code is "
                              f"{p_aspen_assignments[col_name]}")
                    except TypeError:
                        print("Could not concatenate assignment col and ID.  Does student exist in aspen?")
                        continue
                    # need a try and except here to see otherwise need to reload page
                    edit_cell_id = 'e' + cell_id
                    # if gc_score != 'M' and gc_score != 'MISS':

                    if gc_score == 'MISS':
                        sql = 'select * from recorded_scores WHERE id ="' + cell_id + '" AND score ="' + str(
                            gc_score) \
                              + '"'
                    else:
                        if gc_score != 'EXC':
                            sql = 'select * from recorded_scores WHERE id ="' + cell_id + '" AND score =' + str(
                            gc_score)
                        else:
                            sql = 'select * from recorded_scores WHERE id ="' + cell_id + '" AND score =' + '0'

                    print(f"www this is sql {sql}")
                    rows = query_db(db_conn, sql)

                    action = ActionChains(driver)

                    old_score = 0
                    if len(rows) == 0:
                        print("aspen_functions/input_assignments_into_aspen sql is this " + str(sql))
                        # print("HERE IS CELL ID " + str(cell_id))
                        # wait_for_element(p_driver, p_id=cell_id)
                        if p_content_knowledge_completion and re.search('-C$', col_name):
                            old_score = gc_score
                            gc_score = 1
                        wait_for_element_clickable(driver, p_id=cell_id)
                        # time.sleep(1)
                        grade_element = driver.find_element(By.ID, cell_id)

                        # grade_element = p_driver.find_element_by_id(cell_id)
                        action.move_to_element(grade_element).perform()
                        # print("jjj this cell ID " + str(cell_id))
                        grade_element.click()
                        time.sleep(2)
                        # wait_for_element(p_driver, p_id=edit_cell_id)
                        # grade_element2 = p_driver.find_element_by_id(edit_cell_id)
                        grade_element2 = driver.find_element(By.ID, edit_cell_id)
                        grade_element2.send_keys(gc_score)
                        grade_element2.send_keys(Keys.RETURN)
                        if gc_score != 'M' and gc_score != 'MISS':
                            if gc_score != 'EXC':
                                sql = 'INSERT INTO recorded_scores VALUES ("' + \
                                      cell_id + '", "' + gc_assignment_name + '", "' + skills_name + '", ' + \
                                      str(gc_score) + ' )'
                            else:
                                sql = 'INSERT INTO recorded_scores VALUES ("' + \
                                      cell_id + '", "' + gc_assignment_name + '", "' + skills_name + '", ' + \
                                      '0' + ' )'

                            print(f"ttt this is sqL! {sql}")
                            execute_sql(db_conn, sql)
                            print(
                                f"adding this record.  Assignment: {gc_assignment_name} scholar: {skills_name} score: {gc_score}")
                            gc_score = old_score
                            scores_put_in = scores_put_in + 1
                            print(f"scores put in went up! {scores_put_in}")
                    else:
                        print(f"score {gc_score} for {skills_name} is in the DB skipping")
                else:
                    print(
                        f"Assignment needs to be put into Aspen   "
                        f"Assignment: {gc_assignment_name} scholar: {aspen_scholar_id} score: {gc_score}")
            print(f"Finished a day scores_put_in {scores_put_in}, students {num_aspen_students}")
            if scores_put_in == num_aspen_students:
                print("SAME NUMBER scores put in ")
                sql = 'INSERT INTO completed_days VALUES ("' + \
                      gc_assignment_name + '")'
                execute_sql(db_conn, sql)
            else:
                print(f"Looking for this assignment name {gc_assignment_name}")
                sql = 'SELECT * FROM recorded_scores WHERE assignment = \'' + gc_assignment_name + "'"
                execute_sql(db_conn, sql)
                rows = query_db(db_conn, sql)
                added_grades = [x[0] for x in rows]
                if len(added_grades) == num_aspen_students:
                    print("SAME NUMBER put in and added")
                    sql = 'INSERT INTO completed_days VALUES ("' + \
                          gc_assignment_name + '")'
                    execute_sql(db_conn, sql)
                else:
                    print(f"last check to add completed added grades {added_grades} num_aspen_students {num_aspen_students} ")
        driver.close()
        # time.sleep(400)
# gc_assignments_scores_student_id
# {'cpus': [[monique, 63], ['apollo barua', 63] }
# aspen students {'barua, apoollo' : 'stdx2002029840', "bennet-richard":'stdX2002104663}
# aspen assignments: {'course co': 'gcd000010ph1x', 'day 1 sur': 'gcd0000'
# content knowledge: false
#         classroom_grades_to_aspen(key, all_classes[key],
#                                   content_knowledge_completion=content_knowledge_completion_value,
#                                   username=username, password=password, p_config_filename=config_filename,
#                                   p_ignore_noduedate=ignore_noduedate_value,
#                                   p_use_stored_gc_students=use_stored_gc_students_value)