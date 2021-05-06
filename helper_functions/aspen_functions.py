def generate_driver():
    """
    Creates a selenium driver object and returns it
    :return: Selenium driver object
    """
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager

    chrome_options = Options()
    chrome_options.add_argument("Window-size=6500,12000")
    p_driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    p_driver.get('https://aspen.cpsd.us')
    return p_driver


def aspen_login(p_driver, *, username='', password=''):
    """
    Logs in to Aspen
    :param p_driver:  Selenium driver object
    :param username: username (string)
    :param password: password (string)
    :return: none
    """
    from selenium.webdriver.support import expected_conditions as ec
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException

    try:
        WebDriverWait(p_driver, 10).until(ec.presence_of_element_located((By.XPATH, "//input[@class='logonInput']")))
    except TimeoutException:
        print("Did not find logon screen")
        print("quitting")
        p_driver.quit()

    if username and password:
        print("Login supplied via script.")
        p_driver.find_element_by_xpath("//input[@class='logonInput']").send_keys(username)
        p_driver.find_element_by_xpath("//input[@name='password']").send_keys(password)
        p_driver.find_element_by_xpath("//button").click()
    else:
        print("Login credentials not supplied.  Manual login")
        wait_for_element(p_driver, p_xpath_el="//a[@title='Gradebook tab']", timeout=30,
                         message=f'Did not login sucessfully after 30 seconds')
        try:
            WebDriverWait(p_driver, 30).until(ec.presence_of_element_located((By.XPATH, "")))
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
    wait_for_element(p_driver, p_link_text='Gradebook')
    p_driver.find_element_by_link_text("Gradebook").click()
    # Do this twice, because Aspen is flaky
    wait_for_element(p_driver, p_link_text='Gradebook')
    p_driver.find_element_by_link_text("Gradebook").click()
    wait_for_element(p_driver, p_link_text=p_aspen_class,
                     message="Be sure this EXACT class really exists in Aspen!\n" + str(p_aspen_class))
    p_driver.find_element_by_link_text(p_aspen_class).click()
    wait_for_element(p_driver, p_link_text='Scores')
    p_driver.find_element_by_link_text("Scores").click()


def goto_assignment(p_driver, p_aspen_class):
    """
    Goto Assignments.  Assumes are are at the aspen login.
    :param p_driver: Selenium driver object
    :param p_aspen_class: Name of the class in Aspen.
    :return:
    """
    goto_gradebook(p_driver, p_aspen_class)
    wait_for_element(p_driver, p_link_text='Assignments')
    p_driver.find_element_by_link_text("Assignments").click()


def add_assignment(p_driver, p_coursework, p_content_knowledge_completion):
    import datetime
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.action_chains import ActionChains
    import time
    from helper_functions import constants
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as ec

    # get aspen assignment and column names
    assignment_name = p_coursework['title']
    gb_column_name = convert_assignment_name(p_coursework['title'])

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
    grade_term = 'nonono'
    if python_due_date <= constants.Q1:
        grade_term = 'Q1'
    elif python_due_date <= constants.Q2:
        grade_term = 'Q2'
    elif python_due_date <= constants.Q3:
        grade_term = 'Q3'
    elif python_due_date <= constants.Q4:
        grade_term = 'Q4'

    # get aspen Due date
    aspen_date_due = str(p_coursework['dueDate']['month']) + "/" + \
                     str(p_coursework['dueDate']['day']) + "/" + \
                     str(p_coursework['dueDate']['year'])


    if p_content_knowledge_completion:
        category = 'blah'
    else:
        category = p_coursework['aspen_category']


    # get aspen points
    total_points = p_coursework['maxPoints']
    extra_credit = str(round(int(total_points) * .05))

    print(
        f"{assignment_name} {gb_column_name} {date_assigned} {aspen_date_due} {grade_term}  {category} {total_points} {extra_credit}")
    wait_for_element(p_driver, p_xpath_el='/html/body')
    p_driver.find_element_by_xpath('/html/body').click()

    while len(p_driver.window_handles) == 1:
        time.sleep(1)
        p_driver.find_element_by_xpath('/html/body').send_keys(Keys.CONTROL, "a")
    window_before = p_driver.window_handles[0]
    window_after = p_driver.window_handles[1]
    p_driver.switch_to.window(window_after)

    print("this worked!")

  #  p_driver.find_element_by_xpath('/html/body').send_keys(Keys.CONTROL, "a")




    action = ActionChains(p_driver)
    field_value = {'propertyValue(gcdColCode)': gb_column_name, "propertyValue(gcdColName)": assignment_name,
                   'propertyValue(gcdTotalPoints)': total_points, 'propertyValue(gcdExtraCredPt)': extra_credit,
                   '#propertyValue(gcdGctOID)': category, 'propertyValue(gcdDateDue)': aspen_date_due,
                   'propertyValue(gcdDateAsgn)': date_assigned, '#propertyValue(gcdGtmOID)': grade_term,
    }
    for key in field_value.keys():
        wait_for_element(p_driver, p_name=key)
        element = p_driver.find_element_by_name(key)
        action.move_to_element(element).perform()
        element.click()
        for i in range(10):
            element.send_keys(Keys.BACKSPACE)
        element.send_keys(field_value[key])

    raise ValueError("Debugging stop here")
    # p_driver.find_element_by_css_selector("body").send_keys(Keys.CONTROL, "a")



    # time.sleep(3)
# /html/body/form/table/tbody/tr[2]/td/div/table[2]/tbody/tr[1]/td[2]/table[1]/tbody/tr/td[2]/div[1]

def add_assignments(p_driver, p_courseworks, p_content_knowledge_completion):

    # get the name of the first category
    if p_content_knowledge_completion is False:
        full_xpath = '/ html / body / form / table / tbody / tr[2] / td ' \
                     '/ div / table[2] / tbody / tr[1] / td[2] / div / table / tbody / tr[2] / td[2] / a'
        wait_for_element(p_driver, p_link_text='Categories')
        p_driver.find_element_by_link_text("Categories").click()
        category_element = p_driver.find_element_by_xpath(full_xpath)
        category = category_element.get_attribute('text')
        wait_for_element(p_driver, p_link_text='Assignments')
        p_driver.find_element_by_link_text("Assignments").click()
        wait_for_element(p_driver, p_link_text='Assignments')
        p_driver.find_element_by_link_text("Scores").click()
        wait_for_element(p_driver, p_link_text='Scores')
        for coursework in p_courseworks:
            coursework['aspen_category'] = category
    for coursework in p_courseworks:
        add_assignment(p_driver, coursework, p_content_knowledge_completion)


def check_new_aspen_names(p_dict):
    """
    Loops over proposed aspen assignment names (converted from Google Classroom dictionary).  If any duplicates, quits
    :param p_dict:
    :return: Boolean (True if good)
    """
    print("Checking Google classroom names to be sure there are no duplicates after we shrink them to 7 characters for "
          "Aspen")
    proposed_names = []
    for coursework in p_dict:
        gc_name = coursework['title']
        aspen_name = convert_assignment_name(gc_name)
        proposed_names.append(aspen_name)
    for name in proposed_names:
        if proposed_names.count(name) > 1:
            raise ValueError(f"This name will conflict (two assignments that are the same after you shrink them)"
                             f" Rename your Google classroom assignments.  Here is the shrunk name:\n{name}"
                             f"\nand it appears this many times: {proposed_names.count(name)}")


def convert_assignment_name(p_name):
    import re
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
        column_name = new_title[:7]
    else:
        column_name = new_title
    return column_name


def wait_for_element(p_driver, *, message='', timeout=10, p_link_text='', p_xpath_el='', p_id='', p_name=''):
    """

    :param p_driver: Selenium driver object
    :param message: Message to print in case unsuccessful (string)
    :param timeout: Time out in seconds (int)
    :param p_xpath_el: Xpath of element we are looking for (string)
    :param p_link_text: Text element we are looking for (string)
    :param p_link_text: ID of element we are looking for (string)
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
            raise ValueError(f"Could not find this Xpath element in the page:{p_xpath_el}")
    elif p_link_text:
        try:
            WebDriverWait(p_driver, timeout).until(ec.presence_of_element_located((By.LINK_TEXT, p_link_text)))
        except TimeoutException:
            if message:
                print(message)
            p_driver.quit()
            raise ValueError(f"Could not find this exact link text in the page:{p_link_text}")
    elif p_id:
        try:
            WebDriverWait(p_driver, timeout).until(ec.presence_of_element_located((By.ID, p_link_text)))
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