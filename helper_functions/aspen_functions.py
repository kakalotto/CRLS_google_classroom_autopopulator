def generate_driver():
    """
        Creates a selenium driver object and returns it
    :return: Selenium driver
    """
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service

    chrome_options = Options()

#    chrome_options.add_argument("Window-size=6500,12000")
#    p_driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
#    p_driver = webdriver.Chrome(ChromeDriverManager().install())
    service = Service()
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    p_driver = webdriver.Chrome(service=service, options=options)
    # p_driver.get('https://aspen.cpsd.us')
    p_driver.get('https://aspen.cpsd.us/aspen/logonSSO.do?deploymentId=ma-cambridge&districtId=*dst&idpName=Cambridge%20Google%20SAML')
    return p_driver


def aspen_login(p_driver, *, username='', password=''):
    """
    Logs in to Aspen
    :param p_driver:  Selenium driver object
    :param username: username (string)
    :param password: password (string)
    :return: none
    """
    import time
    from selenium.webdriver.support import expected_conditions as ec
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.action_chains import ActionChains

#     try:
# #        WebDriverWait(p_driver, 10).until(ec.presence_of_element_located((By.XPATH, "//input[@class='logonInput']")))
#            WebDriverWait(p_driver, 10).until(ec.presence_of_element_located((By.CLASS_NAME, "login-button")))
#
#     except TimeoutException:
#         print("Did not find logon button")
#         print("quitting")
#         p_driver.quit()
    # time.sleep(500)

    # buttons = p_driver.find_element(By.XPATH, "//button")
    # print(buttons)
    # time.sleep(500)

    if username and password:

        print("Yes!")
        print("Login supplied via script.")
        time.sleep(2)
        # p_driver.find_element(By.CLASS_NAME, "login-button").click()
        # # Second login button
        # WebDriverWait(p_driver, 10).until(ec.presence_of_element_located((By.CLASS_NAME, "login-button")))
        # p_driver.find_element(By.CLASS_NAME, "login-button").click()
        # time.sleep(50)
        print("hopefully at Google sscreen")
        p_driver.find_element(By.NAME, "identifier").send_keys(username)
        p_driver.find_element(By.NAME, "identifier").send_keys(Keys.ENTER)
        time.sleep(5)

        actions = ActionChains(p_driver)
        actions.send_keys(password + Keys.ENTER)
        actions.perform()

    else:
        print("Login credentials not supplied.  Manual login")
        wait_for_element(p_driver, p_xpath_el="//a[@title='Gradebook tab']", timeout=30,
                         message=f'Did not login sucessfully after 30 seconds')
        try:
            WebDriverWait(p_driver, 30).until(ec.presence_of_element_located((By.ID, "contextMenu")))
        except TimeoutException:
            print("Did not log in successfully after 30 seconds")
            print("quitting")
            p_driver.quit()


def goto_gradebook(p_driver, p_aspen_class):
    """
    Goto gradebook.  Assumes are are at the aspen login.
    :param p_driver: Selenium driver object
    :param p_aspen_class: Name of the class in Aspen.
    :return:
    """
    import time
    from selenium.webdriver.common.by import By

    # print("Trying to go to gradebook")
    # wait_for_element(p_driver, message='Trying to find gradebook but failed?', p_link_text='Gradebook')
    # # p_driver.find_ele
    # p_driver.find_element(By.LINK_TEXT, "Gradebook").click()
    # Do this twice, because Aspen is flaky
    # wait_for_element(p_driver, p_link_text='Gradebook')
    # p_driver.find_element(By.LINK_TEXT, "Gradebook").click()
    # time.sleep(5)

    gradebook = click_button(p_driver, By.LINK_TEXT, 'Gradebook', 10)
    gradebook = click_button(p_driver, By.LINK_TEXT, 'Gradebook', 10)
    aspen_class = click_button(p_driver, By.LINK_TEXT, p_aspen_class, 10)
    print("bbb clicking scores")
    time.sleep(3)
    scores = click_button(p_driver, By.LINK_TEXT, 'Scores', 10)

    # wait_for_element(p_driver, p_link_text=p_aspen_class,
    #                  message="Be sure this EXACT class really exists in Aspen!\n" + str(p_aspen_class))
    # p_driver.find_element(By.LINK_TEXT, p_aspen_class).click()

    # p_driver.find_element_by_link_text(p_aspen_class).click()
    # wait_for_element(p_driver, p_link_text='Scores')
    # print("bbb clicking scores")
    # time.sleep(2)
    # p_driver.find_element(By.LINK_TEXT, "Scores").click()

    # p_driver.find_element_by_link_text("Scores").click()
    # time.sleep(2)


def goto_students(p_driver):
    """
    Goto Students tab in navbar.
    :param p_driver: Selenium driver object
    :return:
    """
    from selenium.webdriver.common.by import By

    wait_for_element(p_driver, p_link_text='Student')
    p_driver.find_element(By.LINK_TEXT, "Student").click()
    # p_driver.find_element_by_link_text("Student").click()

def search_name(p_driver, p_name):
    """
    Clicks on lasaid to sort assumes already in students navtab.
    :param p_driver: Selenium driver object
    :return:
    """
    wait_for_element(p_driver, p_id='findMenuBarWidget-textInput')
    p_driver.find_element_by_id('findMenuBarWidget-textInput').click()
    p_driver.find_element_by_id('findMenuBarWidget-textInput').send_keys(p_name)
    wait_for_element(p_driver, p_id='findMenuBarWidget-searchButton')
    p_driver.find_element_by_id("findMenuBarWidget-searchButton").click()



def goto_sort_lasid(p_driver):
    """
    Clicks on lasaid to sort assumes already in students navtab.
    :param p_driver: Selenium driver object
    :return:
    """
    wait_for_element(p_driver, p_id='stdIDLocal')
    p_driver.find_element_by_id('stdIDLocal').click()



def goto_student(p_driver, p_student_id):
    """
    Goto Student, given an id. assumes already in students navtab.
    :param p_driver: Selenium driver object
    :return:
    """
    from selenium.webdriver.common.by import By
    p_driver.find_element(By.LINK_TEXT, "Student").click()


    wait_for_element(p_driver, p_link_text=p_student_id)
    from selenium.webdriver.common.by import By
    p_driver.find_element(By.LINK_TEXT, p_student_id).click()

    # p_driver.find_element_by_link_text(p_student_id).click()


def extract_email(p_driver):
    # assumes already on page
    wait_for_element(p_driver, p_id='propertyValue(relStdPsnOid_psnEmail02)-span')
    abc =  p_driver.find_element_by_id('propertyValue(relStdPsnOid_psnEmail02)-span').text
    return abc


def goto_assignments(p_driver, p_aspen_class):
    """
    Goto Assignments.  Assumes are are at the aspen login.
    :param p_driver: Selenium driver object
    :param p_aspen_class: Name of the class in Aspen.
    :return:
    """
    from selenium.webdriver.common.by import By

    goto_gradebook(p_driver, p_aspen_class)
    assignments_button = click_button(p_driver, By.LINK_TEXT, "Assignments", 5, )

    # wait_for_element(p_driver, p_link_text='Assignments')
    # p_driver.find_element(By.LINK_TEXT, "Assignments").click()

    # p_driver.find_element_by_link_text("Assignments").click()


# Maya
def get_student_ids_from_class(p_driver, class_code):
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import NoSuchElementException
    import time
    print('ggg gradebook')
    gradebook = click_button(p_driver, By.PARTIAL_LINK_TEXT, "Gradebook", 9)
    print('hhh class button gradebook')

    class_button = click_button(p_driver, By.PARTIAL_LINK_TEXT, class_code, 9)
    time.sleep(1)
    print('hhh roster')

    roster_button = click_button(p_driver, By.PARTIAL_LINK_TEXT, "Roster", 9)
    if gradebook == "dne" or class_button == "dne" or roster_button == "dne":
        return False
    try:
        raw_data = p_driver.find_elements(by=By.CSS_SELECTOR, value="td")
    except NoSuchElementException:
        return False
    str_data = [item.text for item in raw_data]
    student_ids = [student_id for student_id in str_data if student_id.isdigit() and len(student_id) == 7]
    return student_ids

# Written by Maya
def click_button(p_driver, by_value, value_value, wait_time):
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support import expected_conditions as ec
    from selenium.common.exceptions import TimeoutException

    if wait_time:
        try:
            wait = WebDriverWait(p_driver, timeout=wait_time)
            wait.until(ec.element_to_be_clickable((by_value, value_value)))

        except TimeoutException:
            return "dne"

    button = (p_driver.find_element(by=by_value, value=value_value))
    button.click()
    return button

# Maya
def goto_student_profile_by_id(p_driver, student_id):
    from selenium.webdriver.common.by import By
    import time
    click_button(p_driver, By.PARTIAL_LINK_TEXT, "Student", 2)
    try:
        click_button(p_driver, By.PARTIAL_LINK_TEXT, "Student List", 2)
        print("clicked student list")
    except:
        print("Did not click student list")
    can_continue = True
    student_nonexistant = False
    while can_continue and click_button(p_driver, By.PARTIAL_LINK_TEXT, student_id, 1) == "dne":
        student_nonexistant = click_button(p_driver, By.PARTIAL_LINK_TEXT, student_id, 1) == "dne"
        time.sleep(.2)
        next_button = p_driver.find_element(by=By.NAME, value="nextPageButton")
        can_continue = next_button.is_enabled()
        time.sleep(.2)
        next_button.click()
    if student_nonexistant and not can_continue:
        return "na" + student_id
    return True


# Maya
def get_birthday(p_driver):
    from selenium.webdriver.common.by import By

    bday_box = p_driver.find_element(By.ID, "propertyValue(relStdPsnOid_psnDob)-span")
    return bday_box.text[:bday_box.text.index(" ")]

def goto_categories(p_driver, p_aspen_class):
    """
    Goto Assignments.  Assumes are are at the aspen login.
    :param p_driver: Selenium driver object
    :param p_aspen_class: Name of the class in Aspen.
    :return:
    """
    from selenium.webdriver.common.by import By

    goto_gradebook(p_driver, p_aspen_class)
    categories_button = click_button(p_driver, By.LINK_TEXT, "Categories", 5, )

    # wait_for_element(p_driver, p_link_text='Categories')
    # p_driver.find_element(By.LINK_TEXT, "Categories").click()
    # p_driver.find_element_by_link_text("Assignments").click()


def add_skills_category(p_driver, category):
    """
    Goto Assignments.  Assumes are are at the aspen login.
    :param p_driver: Selenium driver object
    :param p_aspen_class: Name of the class in Aspen.
    :return:
    """
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import Select
    import time
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.common.keys import Keys

    # select = Select(p_driver.find_element(By.LINK_TEXT, 'Options'))
    # # select by visible text
    # select.select_by_visible_text('Add')
    print("In add skill category")
    wait_for_element(p_driver, p_id='options')
    p_driver.find_element(By.ID, "options").click()
    wait_for_element(p_driver, p_id='options_Option1')
    p_driver.find_element(By.ID, "options_Option1").click()
    # for="propertyValue(gctColType)"
    # for="propertyValue(gctTypeDesc)"
    field_value = { 'propertyValue(gctColType)': 'exp-avg',
                    'propertyValue(gctTypeDesc)': 'Exploratory Average',
                    'propertyValue(gctTypeWeight)': '1'}
    print(f"Field value! {field_value}")
    action = ActionChains(p_driver)

    for key in field_value.keys():
        time.sleep(2)
        wait_for_element(p_driver, p_name=key)
        print(f"finding the element {key}")
        element = p_driver.find_element(By.NAME, key)
        # element = p_driver.find_element_by_name(key)
        action.move_to_element(element).perform()
        time.sleep(1)
        element.click()
        print("backspacing")
        for i in range(35):
            print(f"i {i}")
            element.send_keys(Keys.BACKSPACE)
        element.send_keys(field_value[key])
    wait_for_element(p_driver, p_name='saveButton')
    time.sleep(4)
    # p_driver.find_element_by_name('saveButton').click()
    p_driver.find_element(By.NAME, 'saveButton').click()

    # wait_for_element(p_driver, p_link_text='Add')
    # p_driver.find_element(By.LINK_TEXT, "Add").click()
    # p_driver.find_element_by_link_text("Assignments").click()


def goto_assignments_this_quarter(p_driver, p_aspen_class, p_quarter):
    """
    Goto Assignments and select this quarter.  Assumes are are past the aspen login.
    :param p_driver: Selenium driver object
    :param p_aspen_class: Name of the class in Aspen.
    :param p_quarter: This quarter (Q1, Q3, Q3, etc...) (string)
    :return: none
    """
    from selenium.webdriver.common.by import By

    goto_assignments(p_driver, p_aspen_class)
    p_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    wait_for_element(p_driver, p_xpath_el="//a[@title='List of assignment records']")  # assignments on the left
    wait_for_element(p_driver, p_xpath_el='//*[@id="filterMenu"]')  # funnel icon
    p_driver.find_element(By.XPATH, '//*[@id="filterMenu"]').click()
    # p_driver.find_element_by_xpath('//*[@id="filterMenu"]').click()
    wait_for_element(p_driver, p_xpath_el='//*[@id="filterMenu_Option2"]/td[2]')  # term= pulldown
    p_driver.find_element(By.XPATH, '//*[@id="filterMenu_Option2"]/td[2]').click()

    # p_driver.find_element_by_xpath('//*[@id="filterMenu_Option2"]/td[2]').click()
    window_before = p_driver.window_handles[0]
    window_after = p_driver.window_handles[1]
    p_driver.switch_to.window(window_after)
    wait_for_element(p_driver, p_xpath_el='//input[@name="value(prompt1)"]')  # term ID field
    # term_id_field = p_driver.find_element_by_xpath('//input[@name="value(prompt1)"]')
    term_id_field = p_driver.find_element(By.XPATH, '//input[@name="value(prompt1)"]')
    term_id_field.click()  # Click in the popup termID field
    term_id_field.send_keys(p_quarter)  # type in the quarter
    wait_for_element(p_driver, p_xpath_el='//*[@id="submitButton"]')  # Submit button
    p_driver.find_element(By.XPATH, '//*[@id="submitButton"]').click()

    # p_driver.find_element_by_xpath('//*[@id="submitButton"]').click()
    p_driver.switch_to.window(window_before)


def goto_scores(p_driver, p_aspen_class):
    """
    Goto Assignments.  Assumes are are past the aspen login.
    :param p_driver: Selenium driver object
    :param p_aspen_class: Name of the class in Aspen.
    :return:
    """
    import time
    from selenium.webdriver.common.by import By

    goto_gradebook(p_driver, p_aspen_class)
    wait_for_element(p_driver, p_link_text='Assignments')  # just to be sure loading is done
    p_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    wait_for_element_clickable(p_driver, p_link_text='Scores')  # just to be sure loading is done
    p_driver.find_element(By.LINK_TEXT, "Scores").click()

    wait_for_element(p_driver, p_link_text='Scores')  # just to be sure loading is done
    #        wait.until(EC.invisibility_of_element_located((By.XPATH, '//img[contains(@src, "loading")]')))


def goto_scores_this_quarter(p_driver, p_aspen_class, p_quarter):
    """
    Goto gradebook and select this quarter, click on all categories  Assumes are are past the aspen login.
    :param p_driver: Selenium driver object
    :param p_aspen_class: Name of the class in Aspen.
    :param p_quarter: This quarter (Q1, Q3, Q3, etc...) (string)
    :return: none
    """
    from selenium.webdriver.support import expected_conditions as ec
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.common.exceptions import TimeoutException
    import time

    goto_scores(p_driver, p_aspen_class)
    good_to_go = False
    while good_to_go is False:
        try:
            WebDriverWait(p_driver, 10).until(
                ec.presence_of_element_located((By.XPATH,"//select[@name='termFilter']")))
            good_to_go = True
        except TimeoutException:
            p_driver.refresh()
   #  wait_for_element(p_driver, p_xpath_el="//select[@name='termFilter']")  # term pulldown menu
    xpath = "//select[@name='termFilter']/option[text()='" + str(p_quarter) + "']"
    wait_for_element(p_driver, p_xpath_el=xpath)  # term pulldown menu
    p_driver.find_element(By.XPATH, xpath).click()

    # p_driver.find_element_by_xpath(xpath).click()
    print("found pulldown maybe")

  # xpath = '//*[@id="contentArea"]/table[2]/tbody/tr[1]/td[2]/table[3]/tbody/tr[2]/td[1]/table/tbody/tr/td[1]/select'
    xpath = '//*[@id="contentArea"]/table[2]/tbody/tr[1]/td[2]/table[3]/tbody/tr[2]/td[2]/table/tbody/tr/td[1]/select/option[1]'
    time.sleep(4) #can't figure this out, something.
    wait_for_element(p_driver, p_xpath_el=xpath)
# /html/body/form/table/tbody/tr[2]/td/div/table[2]/tbody/tr[1]/td[2]/table[3]/tbody/tr[2]/td[4]/select/option[4]
# /html/body/form/table/tbody/tr[2]/td/div/table[2]/tbody/tr[1]/td[2]/table[3]/tbody/tr[2]/td[2]/table/tbody/tr/td[1]/select/option[1]
#           //*[@id="contentArea"]/table[2]/tbody/tr[1]/td[2]/table[3]/tbody/tr[2]/td[2]/table/tbody/tr/td[1]/select/option[1]

    # p_driver.find_element_by_xpath(xpath).click()  # clicks on Grade Columns ALL (all categories)
    p_driver.find_element(By.XPATH, xpath).click()  # clicks on Grade Columns ALL (all categories)

    # xpath += "/option[text()='All']"
    # wait_for_element(p_driver, p_xpath_el=xpath)
    # p_driver.find_element_by_xpath(xpath).click()
    good_to_go = False
    while good_to_go is False:
        try:
            WebDriverWait(p_driver, 10).until(
                ec.presence_of_element_located((By.XPATH,"//div[@class='scrollCell invisible-horizontal-scrollbar']")))
            good_to_go = True
        except TimeoutException:
            p_driver.refresh()

    wait_for_element(p_driver, p_xpath_el="//div[@class='scrollCell invisible-horizontal-scrollbar']")
    wait_for_element(p_driver, p_xpath_el="//a")
    wait_for_element(p_driver, p_xpath_el="//select[@name='termFilter']")  # term pulldown menu


def add_assignment(p_driver, p_coursework, p_content_knowledge_completion, p_db_conn, p_category='c',
                   p_style="no_due_dates"):
    import datetime
    import re
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.action_chains import ActionChains
    import time
    # from helper_functions import constants
    from helper_functions.db_functions import execute_sql
    from helper_functions.quarters import which_quarter_today_string
    from selenium.webdriver.common.by import By


    # get aspen assignment and column names
    assignment_name = p_coursework['title']
    gb_column_name = convert_assignment_name(p_coursework['title'], p_content_knowledge_completion)
    if p_content_knowledge_completion and p_category == 'c':
        gb_column_name += '-C'
        assignment_name += '-completion'
    elif p_content_knowledge_completion and p_category == 'k':
        gb_column_name += '-K'
        assignment_name += '-content knowledge'
    # get aspen ssign date
    if p_coursework['state'] == 'PUBLISHED':
        year_assigned = p_coursework['creationTime'].split("T")[0].split('-')[0]
        month_assigned = p_coursework['creationTime'].split("T")[0].split('-')[1]
        day_assigned = p_coursework['creationTime'].split("T")[0].split('-')[2]
    else:
        year_assigned = p_coursework['scheduledTime'].split("T")[0].split('-')[0]
        month_assigned = p_coursework['scheduledTime'].split("T")[0].split('-')[1]
        day_assigned = p_coursework['scheduledTime'].split("T")[0].split('-')[2]
    date_assigned = month_assigned + "/" + day_assigned + "/" + year_assigned

    # Get aspen Grade term, using datetime
    python_due_date = datetime.datetime(int(p_coursework['dueDate']['year']), int(p_coursework['dueDate']['month']),
                                        int(p_coursework['dueDate']['day']))
    one_minute = datetime.timedelta(minutes=1)
    if python_due_date.hour == 0 and python_due_date.minute == 0:
        python_due_date -= one_minute
    print("in add assignemtns, due hour, due minute  " + str(python_due_date.hour) + " " + str(python_due_date.minute))
    print("in add assignments python due date " + str(python_due_date))
    grade_term = which_quarter_today_string(datetime_obj=python_due_date)
#    print(constants.Q1, constants.Q2, constants.Q3)
#    if constants.Q1 <= python_due_date < constants.Q2:
#         grade_term = 'Q1'
#     elif constants.Q2 <= python_due_date < constants.Q3:
#         grade_term = 'Q2'
#     elif constants.Q3 <= python_due_date < constants.Q4:
#         grade_term = 'Q3'
#     elif constants.Q4 <= python_due_date <= constants.summer:
#         grade_term = 'Q4'
#     else:  # doesn't fit at all, change the due date
#         grade_term = 'Q4'
#     if grade_term == 'Q4':
#         p_coursework['dueDate']['month'] = constants.summer.month
#         p_coursework['dueDate']['day'] = constants.summer.day
#         p_coursework['dueDate']['year'] = constants.summer.year

    # print('grade_term  ' + str(grade_term))
    # print(python_due_date)
    # print(constants.Q1)
    # print(constants.Q2)
    # print(constants.Q3)
    # print(constants.Q4)

    # print(p_coursework['dueDate']['month'])
    # print(p_coursework['dueDate']['day'] )
    # raise ValueError("wut")
    # get aspen Due date
    aspen_date_due = str(p_coursework['dueDate']['month']) + "/" + str(p_coursework['dueDate']['day']) \
        + "/" + str(p_coursework['dueDate']['year'])

    if p_content_knowledge_completion:
        category = 'blah'
    else:
        category = p_coursework['aspen_category']

    # get aspen points
    if p_content_knowledge_completion and p_category == 'c':
        total_points = 1
        extra_credit = 0
        category = 'completion'
    elif p_content_knowledge_completion and p_category == 'k':
        total_points = p_coursework['maxPoints']
        extra_credit = str(round(int(total_points) * .05))
        category = 'content_knowledge'
    else:  # Case of p_content_knowledge is False
        total_points = p_coursework['maxPoints']
        extra_credit = str(round(int(total_points) * .05))

    wait_for_element(p_driver, p_xpath_el='/html/body')
    p_driver.find_element(By.XPATH, '/html/body').click()

    # p_driver.find_element_by_xpath('/html/body').click()
    while len(p_driver.window_handles) == 1:
        time.sleep(1)
        p_driver.find_element(By.XPATH, '/html/body').send_keys(Keys.CONTROL, "a")

        # p_driver.find_element_by_xpath('/html/body').send_keys(Keys.CONTROL, "a")
    window_before = p_driver.window_handles[0]
    window_after = p_driver.window_handles[1]

    p_driver.switch_to.window(window_after)

    action = ActionChains(p_driver)
    field_value = { '#propertyValue(gcdGtmOID)': grade_term,
                    'propertyValue(gcdColCode)': gb_column_name, "propertyValue(gcdColName)": assignment_name,
                   'propertyValue(gcdTotalPoints)': total_points, 'propertyValue(gcdExtraCredPt)': extra_credit,
                   '#propertyValue(gcdGctOID)': category, 'propertyValue(gcdDateDue)': aspen_date_due,
                   'propertyValue(gcdDateAsgn)': date_assigned,
                    'propertyValue(gcdVisType)': 'Public',}
    print(f"Field value! {field_value}")

    print(f"MMMMM {grade_term} MMM DATE {aspen_date_due}")
    for key in field_value.keys():
        # time.sleep(1)
        wait_for_element(p_driver, p_name=key)
        print(f"finding the element {key}")
        element = p_driver.find_element(By.NAME, key)
        # element = p_driver.find_element_by_name(key)
        action.move_to_element(element).perform()
        # time.sleep(1)
        element.click()
        print("backspacing")
        for i in range(35):
            time.sleep(.01)
            print(f"{i}", end=' ')
            element.send_keys(Keys.BACKSPACE)
        element.send_keys(field_value[key])
    wait_for_element(p_driver, p_name='saveButton')
    time.sleep(5)
    # p_driver.find_element_by_name('saveButton').click()
    p_driver.find_element(By.NAME, 'saveButton').click()

    p_driver.switch_to.window(window_before)

    # Put it in the DB
    if p_style == 'no_due_dates':
        sql = 'INSERT INTO aspen_assignments VALUES ("' + gb_column_name + '");'
    else:
        year = p_coursework['dueDate']['year']
        month = p_coursework['dueDate']['month']
        day = p_coursework['dueDate']['day']
        sql = 'INSERT INTO aspen_assignments VALUES ("' + gb_column_name + '", "' + \
              str(year) + '-' + str(month) + '-' + str(day) + '");'
        print(f"This is the SQL! {sql}")
    # sql = 'INSERT INTO aspen_assignments VALUES ("' + gb_column_name + '");'

    execute_sql(p_db_conn, sql)


#
    # raise ValueError("Debugging stop here")


def add_assignments(p_driver, p_courseworks, p_content_knowledge_completion, p_db_conn, p_default_category,
                    p_style):
    import time
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import NoSuchElementException

    print("tt att add assignments")
    #
    # get the name of the first category
    if p_default_category:  # category is set
        for coursework in p_courseworks:
            coursework['aspen_category'] = p_default_category
    elif p_content_knowledge_completion is False:  # Category is default
        full_xpath = '/ html / body / form / table / tbody / tr[2] / td ' \
                     '/ div / table[2] / tbody / tr[1] / td[2] / div / table / tbody / tr[2] / td[2] / a'
        wait_for_element(p_driver, p_link_text='Categories')
        p_driver.find_element(By.LINK_TEXT, "Categories").click()

        # p_driver.find_element_by_link_text("Categories").click()
        try:
            category_element = p_driver.find_element(By.XPATH, full_xpath)
        except NoSuchElementException as e:
            raise Exception(f"Error: {e}.  Possibly you did not add category to this classroom")
        # category_element = p_driver.find_element_by_xpath(full_xpath)
        category = category_element.get_attribute('text')
        wait_for_element(p_driver, p_link_text='Assignments')
        print("ttt found assignments")
        p_driver.find_element(By.LINK_TEXT, "Assignments").click()

        # p_driver.find_element_by_link_text("Assignments").click()
        wait_for_element(p_driver, p_link_text='Assignments')
        for coursework in p_courseworks:
            coursework['aspen_category'] = category

    print("ttt found scores")
    p_driver.find_element(By.LINK_TEXT, "Scores").click()

    # p_driver.find_element_by_link_text("Scores").click()
    wait_for_element(p_driver, p_link_text='Scores')
    for coursework in p_courseworks:
        if p_content_knowledge_completion:
            add_assignment(p_driver, coursework, p_content_knowledge_completion, p_db_conn,
                           p_category='c', p_style=p_style)
            add_assignment(p_driver, coursework, p_content_knowledge_completion, p_db_conn,
                           p_category='k', p_style=p_style)
        else:
            print(f"Adding this one: {coursework}")
            add_assignment(p_driver, coursework, p_content_knowledge_completion, p_db_conn,
                           p_style=p_style)


def check_new_aspen_names(p_dict, p_content_knowledge_completion):
    """
    Loops over proposed aspen assignment names (converted from Google Classroom dictionary).  If any duplicates, quits
    :param p_dict: Dictionary of Google classroom assignments:
    :param p_content_knowledge_completion Boolean whether you are going to have two categories
    :return: Boolean (True if good)
    """
    import re
    print("Checking Google classroom names to be sure there are no duplicates after"
          " we shrink them to 7 or 9 characters for "
          "Aspen")
    proposed_names = []
    for coursework in p_dict:
        gc_name = coursework['title']
        aspen_name = convert_assignment_name(gc_name, p_content_knowledge_completion)
        if re.search(r':-\)', gc_name):
            print("skipping " + str(gc_name))
            continue
        if re.search(r'SKIPTHI', aspen_name):
            continue
        print(aspen_name)
        proposed_names.append(aspen_name)
    for name in proposed_names:
        if proposed_names.count(name) > 1:
            print(f"ERROR: This name will conflict (two assignments that are the same after you shrink them)"
                  f" Rename your Google classroom assignments.  Here is the shrunk name:\n{name}"
                  f"\nand it appears this many times: {proposed_names.count(name)}")
            input("Press enter to continue")
            raise ValueError(f"ERROR: This name will conflict (two assignments that are the same after you shrink them)"
                             f" Rename your Google classroom assignments.  You can edit  convert_assignment_name"
                             f"in aspen functions.  Here is the shrunk name:\n{name}"
                             f"\nand it appears this many times: {proposed_names.count(name)}")


def convert_assignment_name(p_name, p_content_knowledge_completion):
    import re
    """
    :param p_name:  name of assignment in Google classroom
    :return: name of assignment in column form aspen form
    """
    if p_content_knowledge_completion:
        len_title = 7
    else:
        len_title = 9

    new_title = p_name
    new_title = re.sub(r'Python - Dictionaries', 'Dict', new_title, re.X | re.S | re.M)
    new_title = re.sub('Anchor', 'A', new_title)
    new_title = re.sub('DO NOW', 'DN', new_title)
    new_title = re.sub('Why lists part ', 'l-p', new_title)
    new_title = re.sub('Databases', 'DB', new_title)
    new_title = re.sub('Coding challenge', 'cc', new_title)

    new_title = re.sub('Module', 'M', new_title)
    new_title = re.sub('JavaScript', 'J', new_title)
    new_title = re.sub('section', 's', new_title)
    new_title = re.sub('Quiz', 'Q', new_title)
    new_title = re.sub('Python ', 'py', new_title)
    new_title = re.sub('Arduino Day ', 'ar', new_title)
    new_title = re.sub('Scratch ', 'Sc', new_title)
    new_title = re.sub('Autograder', 'AG', new_title)
    new_title = re.sub('Encryption', 'Encrp', new_title)
    new_title = re.sub('Encoding', 'Enc', new_title)
    new_title = re.sub(r'Final\sreview', 'Frev', new_title, re.X | re.S | re.M)
    new_title = re.sub(r'Post\sgraduate\splans,\s', 'grad', new_title, re.X | re.S | re.M)
    new_title = re.sub(r'Wireless', 'W', new_title, re.X | re.S | re.M)
    new_title = re.sub('Printers', 'P', new_title)
    new_title = re.sub(r'Cracking', 'Cr', new_title, re.X | re.S | re.M)
    new_title = re.sub(r'AWS: Computing Solutions', 'A C S', new_title, re.X | re.S | re.M)
    new_title = re.sub(r'AWS: Cloud Computing Essentials', 'A C E', new_title, re.X | re.S | re.M)

    new_title = re.sub(r'AWS: Cloud', 'A', new_title, re.X | re.S | re.M)
    new_title = re.sub(r'AWS:', 'A', new_title, re.X | re.S | re.M)

    new_title = re.sub(r'Warmup', 'wup', new_title, re.X | re.S | re.M)
    new_title = re.sub(r'Create Task Practice', 'CrTaPr', new_title, re.X | re.S | re.M)
    new_title = re.sub(r'Project', 'P w', new_title, re.X | re.S | re.M)
    new_title = re.sub(r'Block model - ', '', new_title, re.X | re.S | re.M)
    new_title = re.sub(r'shorthand', 'sh', new_title, re.X | re.S | re.M)
    new_title = re.sub(r'Font size', 'FS', new_title, re.X | re.S | re.M)
    new_title = re.sub(r'Challenge', 'Ch', new_title, re.X | re.S | re.M)
    new_title = re.sub(r'Offline\spassword\scrack', 'Oline', new_title, re.X | re.S | re.M)
    new_title = re.sub(r'MIT600\sPS', 'M', new_title, re.X | re.S | re.M)
    new_title = re.sub(r'MIT\s600\sPS', 'M', new_title, re.X | re.S | re.M)
    new_title = re.sub(r'Create\sTask', 'CT', new_title, re.X | re.S | re.M)
    new_title = re.sub(r'Responsive', 'R', new_title, re.X | re.S | re.M)
    new_title = re.sub(r'Typescript', 'TS', new_title, re.X | re.S | re.M)
    new_title = re.sub(r'Node', 'N', new_title, re.X | re.S | re.M)
    new_title = re.sub(r'Install', 'I', new_title, re.X | re.S | re.M)
    new_title = re.sub(r'Motherboard', 'MB', new_title)

#
    new_title = re.sub(r'Set up Dev Env Part', 'Devenv', new_title, re.X | re.S | re.M)

    new_title = re.sub(r'Javascript', 'JS', new_title, re.X | re.S | re.M)
    new_title = re.sub(r'Portfolio', 'Pfolio', new_title, re.X | re.S | re.M)
    new_title = re.sub(r'box\smodel', 'BM', new_title, re.X | re.S | re.M)
    new_title = re.sub(r'\s+$', '', new_title)

    if re.search(r"extra \s credit", new_title.lower(), re.X | re.M | re.S):
        return 'SKIPTHIS'
    if re.search(r"create \s task \s checkin", new_title.lower(), re.X | re.M | re.S):
        return 'SKIPTHIS'
    if len(new_title) >= len_title:
        column_name = new_title[:len_title]
    else:
        column_name = new_title
    column_name = re.sub(r'\s+$', '', column_name)
    print(f"aspen functions/convert_assignment_name final title {column_name}")

    return column_name


def get_student_email(p_driver):
    from selenium.webdriver.common.by import By
    student_email = p_driver.find_element(By.ID, "propertyValue(relStdPsnOid_psnEmail01)-span").text
    return student_email

def get_caretaker_emails(p_driver):
    from selenium.webdriver.common.by import By
    click_button(p_driver, By.PARTIAL_LINK_TEXT, "Contacts", 5)
    raw_data = p_driver.find_elements(by=By.CSS_SELECTOR, value="a")
    an_emails = [item.text for item in raw_data if "@" in item.text]
    return list(set(an_emails))


def get_name(p_driver):
    from selenium.webdriver.common.by import By
    import time
    time.sleep(1)
    std_name = p_driver.find_element(By.ID, "propertyValue(stdViewName)-span").text
    i = std_name.index(",")
    return std_name[i + 2:] + " " + std_name[:i]


def get_student_ids_from_aspen(p_driver):
    """
    Gets the aspen IDs from aspen
    :param p_driver: driver
    :return: dictionary key is name in Aspen, value is Aspen student ID.  i.e.
    {'Fakir, Shahnawaz': 'STD0000007I3ZV', 'Hailemichael, Daniel': 'stdX2002052929'}
    """
    from selenium.webdriver.common.by import By

    import re
    import time
    id_scholars = {}
    height = 0
    wait_for_element(p_driver, p_xpath_el="//div[@class='scrollCell invisible-horizontal-scrollbar']")

    # scr = p_driver.find_element_by_xpath("//div[@class='scrollCell invisible-horizontal-scrollbar']")
    scr = p_driver.find_element(By.XPATH, "//div[@class='scrollCell invisible-horizontal-scrollbar']")

    old_names = []
    for i in range(10):
        wait_for_element_clickable(p_driver, p_xpath_el="//a")
        time.sleep(1.5)  # wut?  can't redefine names inside of list so  will just sleep
        names = p_driver.find_elements(By.XPATH, "//a")

        # names = p_driver.find_elements_by_xpath("//a")
        new_names = []
        for a in names:
            try:
                a_attrib = a.get_attribute('href')
               # print(f"current name: {a_attrib}")
            except:
                print("FAILED ONE!")
                continue
            # print("sleeping")
            try:
                # p_driver.find_elements_by_xpath("//a")
                p_driver.find_elements(By.XPATH, "//a")

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
            except:
                print("FAILURE!")
                continue

        # Basically you will run this an extra time.
        # If the names you extract both times are the same, you are done scrolling down.
        new_names.sort()
        old_names.sort()
        if new_names == old_names:
            break
        else:
            old_names = new_names
            height += 120
            try:
                p_driver.execute_script("arguments[0].scrollTo(0," + str(height) + ") ", scr)
            except:
                print("FAILURE TO MOVE AND SCROLL")
    return id_scholars


def get_assignments_from_aspen(p_driver):
    """
    gets all assignments from aspen for a particular class.  Assumes that we're already in that class.
    :param p_driver:   Selenium driver object
    :return: list of Aspen assignment column names (string)
    """
    from selenium.webdriver.common.by import By
    import time
    from selenium.common.exceptions import NoSuchElementException
    print("Getting assignments from Aspen")

    # Navigate to assignments page
    wait_for_element(p_driver, p_link_text='Assignments')

    # p_driver.find_element_by_link_text("Assignments").click()
    p_driver.find_element(By.LINK_TEXT, "Assignments").click()

    wait_for_element(p_driver, p_xpath_el="//div[@id='dataGrid']", message='Did not find assignments')

    # Extract assignments
    print("Navigated, now extracting assignments")
    done = False
    aspen_column_names = []
    while done is False:
        # time.sleep(4000)
        # //*[@id="dataGrid"]/table/tbody/tr[2]
        try:
            # time.sleep(4000)
            time.sleep(2)
            # wait_for_element(p_driver, p_xpath_el="//tr[@class='listCell listRowHeight   ']")
            rows = len(p_driver.find_elements(By.XPATH, "//tr[@class='listCell listRowHeight   ']"))
        except NoSuchElementException as e:
            raise Exception(f"Error is this: {e}\n.  Couldn't find listCell listRowHeight.")
        for i in range(2, rows + 2):
            xpath_string = '//*[@id="dataGrid"]/table/tbody/tr[' + str(i) + ']/td[8]'
            gb_column_name_el = p_driver.find_element(By.XPATH,xpath_string)

            # gb_column_name_el = p_driver.find_element_by_xpath(xpath_string)
            gb_column_name = gb_column_name_el.text
            aspen_column_names.append(gb_column_name)
        try:
            button = p_driver.find_element(By.XPATH, '//*[@id="topnextPageButton"]')

            # button = p_driver.find_element_by_xpath('//*[@id="topnextPageButton"]')
            disabled = button.get_attribute('disabled')
            if disabled is None:
                button.click()
            elif disabled:
                done = True
        except NoSuchElementException:
            done = True
    return aspen_column_names


def get_assignments_and_assignment_ids_from_aspen(p_driver):
    """
    gets all assignments from aspen for a particular class.  Assumes that we're already in that class.
    :param p_driver:   Selenium driver object
    :return: list of Aspen assignment column names (string)
    """
    import time
    from selenium.common.exceptions import NoSuchElementException
    from selenium.webdriver.common.by import By

    print("Getting assignments and IDs from Aspen")

    # Navigate to assignments page
    print("lll navigating to assignments page")
    time.sleep(2)
    wait_for_element(p_driver, p_link_text='Assignments')
    # p_driver.find_element_by_link_text("Assignments").click()
    p_driver.find_element(By.LINK_TEXT, "Assignments").click()

    wait_for_element(p_driver, p_xpath_el="//div[@id='dataGrid']", message='Did not find assignments')

    print("ooo")
    p_aspen_assignment_ids = {}
    done = False
    while done is False:
        wait_for_element(p_driver, p_xpath_el="//tr[@class='listCell listRowHeight   ']")
        # rows = len(p_driver.find_elements_by_xpath("//tr[@class='listCell listRowHeight   ']"))
        rows = len(p_driver.find_elements(By.XPATH, "//tr[@class='listCell listRowHeight   ']"))

        # print(f"rows {rows}")
        # Looop over all rows in this table<
        for i in range(2, rows + 2):
            # //*[@id="dataGrid"] //*[@id="dataGrid"]/table/tbody/tr[1]
            xpath_string = '//*[@id="dataGrid"]/table/tbody/tr[' + str(i) + ']/td[2]'
            wait_for_element(p_driver, p_xpath_el=xpath_string)
            # aspen_assignment_id_el = p_driver.find_element_by_xpath(xpath_string)
            aspen_assignment_id_el = p_driver.find_element(By.XPATH, xpath_string)
            aspen_assignment_id = aspen_assignment_id_el.get_attribute('id')
            xpath_string = '//*[@id="dataGrid"]/table/tbody/tr[' + str(i) + ']/td[9]'
            wait_for_element(p_driver, p_xpath_el=xpath_string)
            # gb_column_name_el = p_driver.find_element_by_xpath(xpath_string)
            gb_column_name_el = p_driver.find_element(By.XPATH, xpath_string)

            gb_column_name = gb_column_name_el.text
            p_aspen_assignment_ids[gb_column_name] = aspen_assignment_id
        try:
            button = p_driver.find_element(By.XPATH, '//*[@id="topnextPageButton"]')

            # button = p_driver.find_element_by_xpath('//*[@id="topnextPageButton"]')
            disabled = button.get_attribute('disabled')
            if disabled is None:
                button.click()
            elif disabled:
                done = True
        except NoSuchElementException:
            done = True
    print()
    return p_aspen_assignment_ids


def match_gc_name_with_aspen_id(p_name, aspen_name_dict):
    """
    Given a name in Google classroom, returns that scholar's ASPEN ID.
    :param p_name:  name of scholar in Google classroom (string)
    :param aspen_name_dict: dictionaries with student ID and name  (dict of strings)
                           i.e. this: {'Fakir, Shahnawaz': 'STD0000007I3ZV', 'Hailemichael, Daniel': 'stdX2002052929'}

    :return: id of scholar in aspen (str)
    """
    import re

    # print(f"p_name {p_name}, dict {aspen_name_dict}")
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


def input_assignments_into_aspen(p_driver, p_assignments_from_classroom, p_aspen_student_ids,
                                 p_aspen_assignments,
                                 p_content_knowledge_completion, p_db_conn):
    """

    :param p_driver:  Selenium driver object
    :param p_assignments_from_classroom: Assignments dictionary from Google classroom.  Looks like this:
       {'abcdefg': [['DANIEL HAILEMICHAEL', 55], ['Shahnawaz Fakir', 33]],
        'def': [['DANIEL HAILEMICHAEL', 22], ['Shahnawaz Fakir', 5]]
        }
    :param p_aspen_student_ids: Student IDs dictionary from Aspen.  Looks like this:
       {'Fakir, Shahnawaz': 'STD0000007I3ZV', 'Hailemichael, Daniel': 'stdX2002052929'}
    :param  p_aspen_assignments: Aspen column names and IDs. .  Looks like this:
       {'GCD000000UDRPL': 'Creepy -C', 'GCD000000UDRPP': 'Creepy -K', 'GCD000000UDRPX': 'Web scr-C',
       'GCD000000UDRPn': 'Web scr-K', 'GCD000000UDRPy': 'ffff ig-C', 'GCD000000UDRQ2': 'ffff ig-K',
       'GCD000000UDRP7': 'def-C', 'GCD000000UDRPB': 'def-K'}
    :param p_content_knowledge_completion Boolean whether you are going to have two categories completion and
        content_knowledge, for every assignment in Google classroom.  True if yes.
    :param p_db_conn: database connection object
    :return:
    """
    # assignments from aspen looks like this, where def is an assignment
    import re
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.common.keys import Keys
    import time
    from helper_functions.db_functions import execute_sql, query_db

    print("These are all th e aspen assignments! " + str(p_aspen_assignments))
    good_load = False
    counter = 0
    while good_load is False:
        time.sleep(1.0)
        inputs = p_driver.find_elements_by_xpath('//tr')
        row_count = 0
        for p_input in inputs:
            # print('xxx')
            # print(p_input)
            if re.search(r'grdrow[0-9]+', p_input.get_attribute('id')):
                row_count += 1
        if row_count != len(p_aspen_student_ids) and counter != 10:
            print('row count found in page' + str(row_count))
            print(p_aspen_student_ids)
            print('aspen student ids from original ' + str(len(p_aspen_student_ids)))
            print("Aspen bug in loading page, reloading now...")
            p_driver.get(p_driver.current_url)
            p_driver.refresh()
            time.sleep(1)
            wait_for_element_clickable(p_driver, p_xpath_el="//div[@class='scrollCell invisible-horizontal-scrollbar']")
            time.sleep(2)
            print("restarting, current counter is this: " + str(counter))
            counter += 1
        else:
            good_load = True
        if counter == 10:
            print("Could not get this page to work after 10 reloads! Try again later")
            raise ValueError
            good_load = False
    print("finished with the load of student grades in aspen!")
    # print(row_count)
    # print(p_aspen_student_ids)
    # print(len(p_aspen_student_ids))

    for key in p_assignments_from_classroom.keys():
        gc_assignment_name = key
        name_scores = p_assignments_from_classroom[key]
        for name_score in name_scores:
            gc_student = name_score[0]
            gc_score = name_score[1]
            if abs(int(gc_score) - gc_score) > 0.01:
                print("Rounding up assignment score to nearest 1")
                gc_score = round(gc_score)
            if gc_score == -9999:
                gc_score = 'MISS'
            print(f"test assignment {gc_assignment_name} test_name {gc_student} test_score {gc_score}")

            assignment_col_names = []
            if p_content_knowledge_completion:
                aspen_assignment_col_name = convert_assignment_name(gc_assignment_name, p_content_knowledge_completion)
                if aspen_assignment_col_name == 'SKIPTHIS':
                    continue
                aspen_assignment_col_name += '-C'
                assignment_col_names.append(aspen_assignment_col_name)
                aspen_assignment_col_name = convert_assignment_name(gc_assignment_name, p_content_knowledge_completion)
#                aspen_scholar_id = match_gc_name_with_aspen_id(gc_student, p_aspen_student_ids)
                aspen_assignment_col_name += '-K'
                assignment_col_names.append(aspen_assignment_col_name)
            else:
                aspen_assignment_col_name = convert_assignment_name(gc_assignment_name, p_content_knowledge_completion)
                if aspen_assignment_col_name == 'SKIPTHIS':
                    continue
                assignment_col_names.append(aspen_assignment_col_name)
            aspen_scholar_id = match_gc_name_with_aspen_id(gc_student, p_aspen_student_ids)
            # print(f'assignments {assignment_col_names}')
            # print("keys are here!")
            # print(p_aspen_assignments.keys())
            # print("assignment col names")
            # print(assignment_col_names)
            for col_name in assignment_col_names:
                # print(f"aspen col name XX{aspen_assignment_col_name}XX scholar_id {aspen_scholar_id}")
                # print(f"p_aspen_assignments {p_aspen_assignments}")
                # print(f"Col name is this: {col_name}")
                # #print(f"p_aspen_assignments[col_name] {p_aspen_assignments[col_name]}")

                # print(f"p_aspen_asisgnment_keys is this: {p_aspen_assignments.keys()}")
                if col_name in p_aspen_assignments.keys():
                    # print(f"p_aspen_assignments[col_name] {p_aspen_assignments[col_name]}  aspen_scholar_id {aspen_scholar_id} "
                    #       f"student name {gc_student}")
                    try:
                        cell_id = p_aspen_assignments[col_name] + '|' + aspen_scholar_id
                    except TypeError:
                        print("Could not concatenate assignment col and ID.  Does student exist in aspen?")
                        continue
                    # need a try and except here to see otherwise need to reload page
                    edit_cell_id = 'e' + cell_id
                    # if gc_score != 'M' and gc_score != 'MISS':

                    if gc_score == 'MISS':
                        sql = 'select * from recorded_scores WHERE id ="' + cell_id + '" AND score ="' + str(gc_score)\
                              + '"'

                    else:
                        sql = 'select * from recorded_scores WHERE id ="' + cell_id + '" AND score =' + str(gc_score)
                    print(f"www this is sql {sql}")
                    rows = query_db(p_db_conn, sql)

                    action = ActionChains(p_driver)

                    old_score = 0
                    if len(rows) == 0:
                        print("aspen_functions/input_assignments_into_aspen sql is this " + str(sql))
                        # print("HERE IS CELL ID " + str(cell_id))
                        # wait_for_element(p_driver, p_id=cell_id)
                        if p_content_knowledge_completion and re.search('-C$', col_name):
                            old_score = gc_score
                            gc_score = 1
                        # wait_for_element_clickable(p_driver, p_id=cell_id)
                        grade_element = p_driver.find_element_by_id(cell_id)
                        action.move_to_element(grade_element).perform()
                        # print("jjj this cell ID " + str(cell_id))
                        grade_element.click()
                        time.sleep(2.5)
                        # wait_for_element(p_driver, p_id=edit_cell_id)
                        grade_element2 = p_driver.find_element_by_id(edit_cell_id)
                        grade_element2.send_keys(gc_score)
                        grade_element2.send_keys(Keys.RETURN)
                        if gc_score != 'M' and gc_score != 'MISS':
                            sql = 'INSERT INTO recorded_scores VALUES ("' + \
                                  cell_id + '", "' + gc_assignment_name + '", "' + gc_student + '", ' + \
                                  str(gc_score) + ' )'
                            print(f"ttt this is sqL! {sql}")
                            execute_sql(p_db_conn, sql)
                            print(f"adding  this record.  Assignment: {gc_assignment_name} scholar: {gc_student} score: {gc_score}")
                            gc_score = old_score
                    else:
                        print(f"'{col_name}' is not in aspen assignments {p_aspen_assignments}")
                        print(f"'keys what the heck {p_aspen_assignments.keys()}")

                else:
                    print(
                        f"Assignment needs to be put into Aspen   "
                        f"Assignment: {gc_assignment_name} scholar: {gc_student} score: {gc_score}")


def wait_for_element(p_driver, *, message='', timeout=10, p_link_text='', p_xpath_el='',
                     p_id='', p_name='', p_class=''):
    """

    :param p_driver: Selenium driver object
    :param message: Message to print in case unsuccessful (string)
    :param timeout: Time out in seconds (int)
    :param p_xpath_el: Xpath of element we are looking for (string)
    :param p_link_text: Text element we are looking for (string)
    :param p_id: ID of element we are looking for (string)
    :param p_name: name of element we are looking for (string)
    :param p_class: class of element we are looking for (string)

    :return: none
    """
    from selenium.webdriver.support import expected_conditions as ec
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.common.exceptions import TimeoutException

    if p_xpath_el:
        try:
            WebDriverWait(p_driver, timeout).until(ec.presence_of_element_located((By.XPATH, p_xpath_el)))
        except TimeoutException:
            if message:
                print(message)
            p_driver.quit()
            raise ValueError("Could not find this Xpath element in the page:" + str(p_xpath_el))
    elif p_link_text:
        try:
            WebDriverWait(p_driver, timeout).until(ec.presence_of_element_located((By.LINK_TEXT, p_link_text)))
        except TimeoutException:
            if message:
                print(message)
            p_driver.quit()
            raise ValueError(f"Could not find this exact link text in the page:{p_link_text},\n"
                             f"Potential issues: You have no categories. ")
    elif p_id:
        try:
            WebDriverWait(p_driver, timeout).until(ec.presence_of_element_located((By.ID, p_id)))
        except TimeoutException:
            if message:
                print(message)
            p_driver.quit()
            raise ValueError(f"Could not find this exact ID in the page:{p_id}")
    elif p_name:
        try:
            WebDriverWait(p_driver, timeout).until(ec.presence_of_element_located((By.NAME, p_name)))
        except TimeoutException:
            if message:
                print(message)
            p_driver.quit()
            raise ValueError(f"Could not find this exact name in the page:{p_name}")
    elif p_class:
        try:
            WebDriverWait(p_driver, timeout).until(ec.presence_of_element_located((By.CLASS_NAME, p_class)))
        except TimeoutException:
            if message:
                print(message)
            p_driver.quit()
            raise ValueError(f"Could not find this exact name in the page:{p_class}")


def wait_for_element_clickable(p_driver, *, message='', timeout=10, p_link_text='', p_xpath_el='',
                               p_id='', p_name='', p_class=''):
    """

    :param p_driver: Selenium driver object
    :param message: Message to print in case unsuccessful (string)
    :param timeout: Time out in seconds (int)
    :param p_xpath_el: Xpath of element we are looking for (string)
    :param p_link_text: Text element we are looking for (string)
    :param p_id: ID of element we are looking for (string)
    :param p_name: name of element we are looking for (string)
    :param p_class: class of element we are looking for (string)

    :return: none
    """
    from selenium.webdriver.support import expected_conditions as ec
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.common.exceptions import TimeoutException

    if p_xpath_el:
        try:
            WebDriverWait(p_driver, timeout).until(ec.element_to_be_clickable((By.XPATH, p_xpath_el)))
        except TimeoutException:
            if message:
                print(message)
            p_driver.quit()
            raise ValueError("Could not find this Xpath element in the page:" + str(p_xpath_el))
    elif p_link_text:

        try:
                WebDriverWait(p_driver, timeout).until(ec.element_to_be_clickable((By.LINK_TEXT, p_link_text)))

        except TimeoutException:
            if message:
                print(message)
            p_driver.quit()
            raise ValueError(f"Could not find this exact link text in the page:{p_link_text}")
    elif p_id:
        try:
            WebDriverWait(p_driver, timeout).until(ec.element_to_be_clickable((By.ID, p_id)))
        except TimeoutException:
            if message:
                print(message)
            p_driver.quit()
            raise ValueError(f"Could not find this exact ID in the page:{p_id}")
    # elif p_name:
    #     try:
    #         WebDriverWait(p_driver, timeout).until(ec.presence_of_element_located((By.NAME, p_name)))
    #     except TimeoutException:
    #         if message:
    #             print(message)
    #         p_driver.quit()
    #         raise ValueError(f"Could not find this exact name in the page:{p_name}")
    # elif p_class:
    #     try:
    #         WebDriverWait(p_driver, timeout).until(ec.presence_of_element_located((By.CLASS_NAME, p_class)))
    #     except TimeoutException:
    #         if message:
    #             print(message)
    #         p_driver.quit()
    #         raise ValueError(f"Could not find this exact name in the page:{p_class}")
