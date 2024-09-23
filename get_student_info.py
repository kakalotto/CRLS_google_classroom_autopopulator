from selenium.webdriver.common.by import By
import getpass
from selenium.webdriver.support.ui import Select

from helper_functions.aspen_functions import generate_driver, get_student_ids_from_class, aspen_login, generate_driver,\
    goto_student_profile_by_id, get_birthday, get_name, get_caretaker_emails, get_student_email, click_button
from helper_functions.read_ini_functions import read_classes_info

classes = read_classes_info('crls_teacher_tools.ini')
aspen_username = input("Give me your aspen username (include .cpsd.us, i.e. ewu@cpsd.us) ")
aspen_password = getpass.getpass('Give me the password for Aspen ')
driver = generate_driver()
aspen_login(driver, username=aspen_username, password=aspen_password)

final_dictionary = {}
for gc_class in classes.keys():
    aspen_class = classes[gc_class]
    class_dictionary = {}
    print(f"This is the aspen class to loop over {aspen_class}")
    student_ids = get_student_ids_from_class(driver, aspen_class)
    print(f"These are the student_ids {student_ids}")
    counter = 0
    class_students = []
    for student_id in student_ids:
        # if aspen_class == 'T986-001' and counter > 0:
        #     continue
        # counter = counter + 1
        goto_student_profile_by_id(driver, student_id)
        name = get_name(driver)
        email = get_student_email(driver)
        birthday = get_birthday(driver)
        caretaker_emails = get_caretaker_emails(driver)
        print(f"name {name} birthday {birthday} email {email} caretaker emails {caretaker_emails}")
        class_students.append({'name': name,
                               'email': email,
                               'caretaker_emails': caretaker_emails,
                               'birthday': birthday,
                               })
    class_dictionary['gc'] = gc_class
    class_dictionary['students'] = class_students
    print(f"temporary state of final dictionary {final_dictionary}")
    # Reset for nexts class
    final_dictionary[aspen_class] = class_dictionary
    # Student reset to student 1
    click_button(driver, By.PARTIAL_LINK_TEXT, "Student", 2)
    try:
        click_button(driver, By.PARTIAL_LINK_TEXT, "Student List", 2)
        print("clicked student list")
    except:
        print("Did not click student list")
    select = Select(driver.find_element(By.NAME, 'topPageSelected'))
    # select by visible text
    select.select_by_index(0)


    # Back to gradebook
    gradebook = click_button(driver, By.PARTIAL_LINK_TEXT, "Gradebook", 5)
    print("clicked gradebook")


fh = open('get_student_info_config.py', 'w')
fh.write('class_students_dict = ' + str(final_dictionary))
fh.close()

print(final_dictionary)