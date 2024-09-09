import datetime
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from helper_functions.skills_functions import generate_driver, skills_login, which_rotation
from helper_functions.aspen_functions import generate_driver, aspen_login, add_assignments, \
    check_new_aspen_names, get_assignments_from_aspen, goto_assignments


now = datetime.datetime.now()

programs = ['Info Technology']
programs_dict = {'Info Technology': {'letter': 'L'}}
course_prefix = 'T120'
t_username = 'ewu@cpsd.us'
t_password = 'silverstreet11'
aspen_username = 'ewu@cpsd.us'
aspen_password = '***REMOVED***'
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


driver = generate_driver()
skills_login(driver,  username=t_username, password=t_password)
for program in programs_dict.keys():
    print(f"Clicking program {program}")
    select = Select(driver.find_element(By.ID, 'whatprogramnumber'))
    # select by visible text
    select.select_by_visible_text(program)
    print("clicking")
    choose = driver.find_element(By.XPATH, '/html/body/div/div/section/div/div[2]/form/fieldset/input')
    choose.click()

# /html/body/div/fieldset[1]/form/table/tbody/tr[2]/td[2]/
# /html/body/div/fieldset[1]/form/table/tbody/tr[2]/td[9]

# /html/body/div/fieldset[1]/form/table/tbody/tr[3]/td[2]
# /html/body/div/fieldset[1]/form/table/tbody/tr[3]/td[9]


    # Choose date
    grade_dict = {}
    for day_number in range(2, 90):
        print(f"Here is the date! {dates[day_number - 1]}")

        # Don't read grades for days after today; quiz
        current_date_obj = datetime.datetime.strptime(dates[day_number - 1], '%m/%d/%Y')
        print(current_date_obj)
        if current_date_obj > now:
            print("no need to read in grades after today: breaking")
            break

        grade_dict[day_number] =  {}
        print(f"trying a date with this index {day_number}")
        select = Select(driver.find_element(By.ID, 'choosedate'))
        print("chose date")
        time.sleep(1)
        select.select_by_index(day_number)
        select_day = driver.find_element(By.XPATH, '//*[@id="frm2"]/fieldset/input')
        continue_button = driver.find_element(By.XPATH, '//*[@id="frm2"]/fieldset/input')
        continue_button.click()
        print("about to get everybody's grade")
        for student_number in range(2, 25):
            try:
                id_xpath = f'/html/body/div/fieldset[1]/form/table/tbody/tr[{student_number}]/td[2]'
                grade_xpath = f'/html/body/div/fieldset[1]/form/table/tbody/tr[{student_number}]/td[9]'
                # try:
                id = driver.find_element(By.XPATH, id_xpath).text
                # print(id)
                grade = driver.find_element(By.XPATH, grade_xpath).text
                # print(grade_dict)
                grade_dict[day_number][id]= grade
                # print(grade_dict)
            except NoSuchElementException:
                break
        time.sleep(2)
    print(grade_dict)
print("final sleeping")
# {1:[{2:{}}, {3:{}}, {4:{}}]   }
# key 2, 3, 4, 5 (day)
# val dict {id: grade}

# key 1 2 3  (rotation
# val {2: {val dict} , 3: {val dict}}
final_aspen_grade_dict = {}
for day in grade_dict.keys():
    rotation = which_rotation(rotation_change, day)
    if rotation in final_aspen_grade_dict.keys():
        final_aspen_grade_dict[rotation][day] = grade_dict[day]
    else:
        final_aspen_grade_dict[rotation] = {}
        final_aspen_grade_dict[rotation][day] = grade_dict[day]
print(final_aspen_grade_dict)

# {1: {2: {'8000613': '96', '8000671': '95', '8001990': '92.7', '8000663': '93', '8005951': '95.7', '8000905': '95.3', '8012709': '95', '8014819': '95', '8015613': '92.7', '8000537': '95.3', '8002254': '95.3', '7003389': '96', '8012285': '95.3', '8001478': '95.3', '8001762': '96.3'},
#      3: {'8000613': '95', '8000671': '95', '8001990': '93.3', '8000663': '96', '8005951': '96', '8000905': '95', '8012709': '80', '8014819': '95', '8015613': '95', '8000537': '95', '8002254': '95.7', '7003389': '96', '8012285': '81', '8001478': '96', '8001762': '80'},
#      4: {'8000613': '0', '8000671': '0', '8001990': '0', '8000663': '0', '8005951': '0', '8000905': '0', '8012709': '0', '8014819': '0', '8015613': '0', '8000537': '0', '8002254': '0', '7003389': '0', '8012285': '0', '8001478': '0', '8001762': '0'}}}
