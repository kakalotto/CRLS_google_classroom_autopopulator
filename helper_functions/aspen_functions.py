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
    # print("Trying to go to gradebook")
    wait_for_element(p_driver, message='Trying to find gradebook but failed?', p_link_text='Gradebook')
    p_driver.find_element_by_link_text("Gradebook").click()
    # Do this twice, because Aspen is flaky
    wait_for_element(p_driver, p_link_text='Gradebook')
    p_driver.find_element_by_link_text("Gradebook").click()
    wait_for_element(p_driver, p_link_text=p_aspen_class,
                     message="Be sure this EXACT class really exists in Aspen!\n" + str(p_aspen_class))
    p_driver.find_element_by_link_text(p_aspen_class).click()
    wait_for_element(p_driver, p_link_text='Scores')
    p_driver.find_element_by_link_text("Scores").click()


def goto_assignments(p_driver, p_aspen_class):
    """
    Goto Assignments.  Assumes are are at the aspen login.
    :param p_driver: Selenium driver object
    :param p_aspen_class: Name of the class in Aspen.
    :return:
    """
    goto_gradebook(p_driver, p_aspen_class)
    wait_for_element(p_driver, p_link_text='Assignments')
    p_driver.find_element_by_link_text("Assignments").click()


def goto_assignments_this_quarter(p_driver, p_aspen_class, p_quarter):
    """
    Goto Assignments and select this quarter.  Assumes are are past the aspen login.
    :param p_driver: Selenium driver object
    :param p_aspen_class: Name of the class in Aspen.
    :param p_quarter: This quarter (Q1, Q3, Q3, etc...) (string)
    :return: none
    """
    goto_assignments(p_driver, p_aspen_class)
    p_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    wait_for_element(p_driver, p_xpath_el="//a[@title='List of assignment records']")  # assignments on the left
    wait_for_element(p_driver, p_xpath_el='//*[@id="filterMenu"]')  # funnel icon
    p_driver.find_element_by_xpath('//*[@id="filterMenu"]').click()
    wait_for_element(p_driver, p_xpath_el='//*[@id="filterMenu_Option2"]/td[2]')  # term= pulldown
    p_driver.find_element_by_xpath('//*[@id="filterMenu_Option2"]/td[2]').click()
    window_before = p_driver.window_handles[0]
    window_after = p_driver.window_handles[1]
    p_driver.switch_to.window(window_after)
    wait_for_element(p_driver, p_xpath_el='//input[@name="value(prompt1)"]')  # term ID field
    term_id_field = p_driver.find_element_by_xpath('//input[@name="value(prompt1)"]')
    term_id_field.click()  # Click in the popup termID field
    term_id_field.send_keys(p_quarter)  # type in the quarter
    wait_for_element(p_driver, p_xpath_el='//*[@id="submitButton"]')  # Submit button
    p_driver.find_element_by_xpath('//*[@id="submitButton"]').click()
    p_driver.switch_to.window(window_before)


def goto_scores(p_driver, p_aspen_class):
    """
    Goto Assignments.  Assumes are are past the aspen login.
    :param p_driver: Selenium driver object
    :param p_aspen_class: Name of the class in Aspen.
    :return:
    """
    goto_gradebook(p_driver, p_aspen_class)
    wait_for_element(p_driver, p_link_text='Assignments')  # just to be sure loading is done
    p_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    wait_for_element(p_driver, p_link_text='Scores')  # just to be sure loading is done
    p_driver.find_element_by_link_text("Scores").click()
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
    goto_scores(p_driver, p_aspen_class)
    wait_for_element(p_driver, p_xpath_el="//select[@name='termFilter']")  # term pulldown menu
    xpath = "//select[@name='termFilter']/option[text()='" + str(p_quarter) + "']"
    wait_for_element(p_driver, p_xpath_el=xpath)  # term pulldown menu
    p_driver.find_element_by_xpath(xpath).click()
    xpath = '//*[@id="contentArea"]/table[2]/tbody/tr[1]/td[2]/table[3]/tbody/tr[2]/td[1]/table/tbody/tr/td[1]/select'
    wait_for_element(p_driver, p_xpath_el=xpath)
    p_driver.find_element_by_xpath(xpath).click()  # clicks on Grade Columns ALL (all categories)
    wait_for_element(p_driver, p_xpath_el="//div[@class='scrollCell invisible-horizontal-scrollbar']")
    wait_for_element(p_driver, p_xpath_el="//a")


def add_assignment(p_driver, p_coursework, p_content_knowledge_completion, p_db_conn, p_category='c'):
    import datetime
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.action_chains import ActionChains
    import time
    from helper_functions import constants
    from helper_functions.db_functions import execute_sql

    # get aspen assignment and column names
    assignment_name = p_coursework['title']
    gb_column_name = convert_assignment_name(p_coursework['title'], p_content_knowledge_completion)
    if p_content_knowledge_completion and p_category == 'c':
        gb_column_name += '-C'
    elif p_content_knowledge_completion and p_category == 'k':
        gb_column_name += '-K'
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
    if python_due_date <= constants.Q1:
        grade_term = 'Q1'
    elif python_due_date <= constants.Q2:
        grade_term = 'Q2'
    elif python_due_date <= constants.Q3:
        grade_term = 'Q3'
    elif python_due_date <= constants.Q4:
        grade_term = 'Q4'
    else:  # doesn't fit at all, change the due date
        grade_term = 'Q4'
        p_coursework['dueDate']['month'] = constants.summer.month
        p_coursework['dueDate']['day'] = constants.summer.day
        p_coursework['dueDate']['year'] = constants.summer.year

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
    p_driver.find_element_by_xpath('/html/body').click()
    while len(p_driver.window_handles) == 1:
        time.sleep(1)
        p_driver.find_element_by_xpath('/html/body').send_keys(Keys.CONTROL, "a")
    window_before = p_driver.window_handles[0]
    window_after = p_driver.window_handles[1]

    p_driver.switch_to.window(window_after)

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
    wait_for_element(p_driver, p_name='saveButton')
    p_driver.find_element_by_name('saveButton').click()
    p_driver.switch_to.window(window_before)

    # Put it in the DB
    sql = 'INSERT INTO aspen_assignments VALUES ("' + gb_column_name + '");'
    execute_sql(p_db_conn, sql)


#
    # raise ValueError("Debugging stop here")


def add_assignments(p_driver, p_courseworks, p_content_knowledge_completion, p_db_conn):

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
    else:
        p_driver.find_element_by_link_text("Scores").click()
        wait_for_element(p_driver, p_link_text='Scores')
    for coursework in p_courseworks:
        if p_content_knowledge_completion:
            add_assignment(p_driver, coursework, p_content_knowledge_completion, p_db_conn, p_category='c')
            add_assignment(p_driver, coursework, p_content_knowledge_completion, p_db_conn, p_category='k')
        else:
            add_assignment(p_driver, coursework, p_content_knowledge_completion, p_db_conn,)


def check_new_aspen_names(p_dict, p_content_knowledge_completion):
    """
    Loops over proposed aspen assignment names (converted from Google Classroom dictionary).  If any duplicates, quits
    :param p_dict: Dictionary of Google classroom assignments:
    :param p_content_knowledge_completion Boolean whether you are going to have two categories
    :return: Boolean (True if good)
    """
    print("Checking Google classroom names to be sure there are no duplicates after"
          " we shrink them to 7 or 9 characters for "
          "Aspen")
    proposed_names = []
    for coursework in p_dict:
        gc_name = coursework['title']
        aspen_name = convert_assignment_name(gc_name, p_content_knowledge_completion)
        proposed_names.append(aspen_name)
    for name in proposed_names:
        if proposed_names.count(name) > 1:
            print(f"This name will conflict (two assignments that are the same after you shrink them)"
                  f" Rename your Google classroom assignments.  Here is the shrunk name:\n{name}"
                  f"\nand it appears this many times: {proposed_names.count(name)}")
            input("Press enter to continue")
            raise ValueError(f"This name will conflict (two assignments that are the same after you shrink them)"
                             f" Rename your Google classroom assignments.  Here is the shrunk name:\n{name}"
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
    new_title = re.sub('Python ', 'py', new_title)
    new_title = re.sub('Scratch ', 'Sc', new_title)
    new_title = re.sub('Autograder', 'AG', new_title)
    new_title = re.sub('Encryption', 'Encrp', new_title)
    new_title = re.sub(r'Final\sreview', 'Frev', new_title, re.X | re.S | re.M)
    # print("New title is this " + str(new_title))
    if re.search(r"extra \s credit", new_title.lower(), re.X | re.M | re.S):
        return 'SKIP'
    if re.search(r"create \s task \s checkin", new_title.lower(), re.X | re.M | re.S):
        return 'SKIP'
    if len(new_title) >= len_title:
        column_name = new_title[:len_title]
    else:
        column_name = new_title
    return column_name


def get_student_ids_from_aspen(p_driver):
    """
    Gets the aspen IDs from aspen
    :param p_driver: driver
    :return: dictionary key is name in Aspen, value is Aspen student ID.  i.e.
    {'Fakir, Shahnawaz': 'STD0000007I3ZV', 'Hailemichael, Daniel': 'stdX2002052929'}
    """
    import re
    id_scholars = {}
    height = 0
    wait_for_element(p_driver, p_xpath_el="//div[@class='scrollCell invisible-horizontal-scrollbar']")
    scr = p_driver.find_element_by_xpath("//div[@class='scrollCell invisible-horizontal-scrollbar']")
    old_names = []
    for i in range(10):
        wait_for_element(p_driver, p_xpath_el="//a")
        names = p_driver.find_elements_by_xpath("//a")
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

        # Basically you will run this an extra time.
        # If the names you extract both times are the same, you are done scrolling down.
        new_names.sort()
        old_names.sort()
        if new_names == old_names:
            break
        else:
            old_names = new_names
            height += 120
            p_driver.execute_script("arguments[0].scrollTo(0," + str(height) + ") ", scr)
    return id_scholars


def get_assignments_from_aspen(p_driver):
    """
    gets all assignments from aspen for a particular class.  Assumes that we're already in that class.
    :param p_driver:   Selenium driver object
    :return: list of Aspen assignment column names (string)
    """
    from selenium.common.exceptions import NoSuchElementException
    print("Getting assignments from Aspen")

    # Navigate to assignments page
    wait_for_element(p_driver, p_link_text='Assignments')
    p_driver.find_element_by_link_text("Assignments").click()
    wait_for_element(p_driver, p_xpath_el="//div[@id='dataGrid']", message='Did not find assignments')

    # Extract assignments
    done = False
    aspen_column_names = []
    while done is False:
        rows = len(p_driver.find_elements_by_xpath("//tr[@class='listCell listRowHeight   ']"))
        for i in range(2, rows + 2):
            xpath_string = '//*[@id="dataGrid"]/table/tbody/tr[' + str(i) + ']/td[8]'
            gb_column_name_el = p_driver.find_element_by_xpath(xpath_string)
            gb_column_name = gb_column_name_el.text
            aspen_column_names.append(gb_column_name)
        try:
            button = p_driver.find_element_by_xpath('//*[@id="topnextPageButton"]')
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
    from selenium.common.exceptions import NoSuchElementException
    print("Getting assignments and IDs from Aspen")

    # Navigate to assignments page
    wait_for_element(p_driver, p_link_text='Assignments')
    p_driver.find_element_by_link_text("Assignments").click()
    wait_for_element(p_driver, p_xpath_el="//div[@id='dataGrid']", message='Did not find assignments')

    p_aspen_assignment_ids = {}
    done = False
    while done is False:
        wait_for_element(p_driver, p_xpath_el="//tr[@class='listCell listRowHeight   ']")
        rows = len(p_driver.find_elements_by_xpath("//tr[@class='listCell listRowHeight   ']"))
        # print(f"rows {rows}")
        # Looop over all rows in this table
        for i in range(2, rows + 2):
            xpath_string = '//*[@id="dataGrid"]/table/tbody/tr[' + str(i) + ']/td[2]'
            wait_for_element(p_driver, p_xpath_el=xpath_string)
            aspen_assignment_id_el = p_driver.find_element_by_xpath(xpath_string)
            aspen_assignment_id = aspen_assignment_id_el.get_attribute('id')
            xpath_string = '//*[@id="dataGrid"]/table/tbody/tr[' + str(i) + ']/td[8]'
            wait_for_element(p_driver, p_xpath_el=xpath_string)
            gb_column_name_el = p_driver.find_element_by_xpath(xpath_string)
            gb_column_name = gb_column_name_el.text
            p_aspen_assignment_ids[gb_column_name] = aspen_assignment_id
        try:
            button = p_driver.find_element_by_xpath('//*[@id="topnextPageButton"]')
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
    :param p_aspen_student_ids: Student IDs dictionary from Google classroom.  Looks like this:
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
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.common.keys import Keys

    from helper_functions.db_functions import execute_sql, query_db

    for key in p_assignments_from_classroom.keys():
        gc_assignment_name = key
        name_scores = p_assignments_from_classroom[key]
        for name_score in name_scores:
            gc_student = name_score[0]
            gc_score = name_score[1]

            # print(f"test assignment {gc_assignment_name} test_name {gc_student} test_score {gc_score}")

            aspen_assignment_col_name = convert_assignment_name(gc_assignment_name, p_content_knowledge_completion)
            aspen_scholar_id = match_gc_name_with_aspen_id(gc_student, p_aspen_student_ids)

            # print(f"aspen col name XX{aspen_assignment_col_name}XX scholar_id {aspen_scholar_id}")
            # print(f"p_aspen_assignments {p_aspen_assignments}")
            cell_id = p_aspen_assignments[aspen_assignment_col_name] + '|' + aspen_scholar_id
            edit_cell_id = 'e' + cell_id

    # 617 761774974 9403
            # This will be the second cell.  If we have to do this, will do
            # completion_assignment = assignment_aspen
            # completion_assignment = re.sub('-K$', '-C', completion_assignment)
            # cell2_id = aspen_assignment_ids[completion_assignment] + '|' + scholar_aspen_id
            # edit_cell2_id = 'e' + cell2_id
            # print(cell_id)
            # print(edit_cell_id)
            sql = 'select * from recorded_scores WHERE id ="' + cell_id + '" AND score =' + str(gc_score)
            rows = query_db(p_db_conn, sql)
            # print(f"This is what the query returns {rows} ")
            # If not found in DB, add it
            action = ActionChains(p_driver)

            if len(rows) == 0:
                # print("HERE IS CELL ID " + str(cell_id))
                # wait_for_element(p_driver, p_id=cell_id)
                grade_element = p_driver.find_element_by_id(cell_id)
                action.move_to_element(grade_element).perform()
                grade_element.click()
                # wait_for_element(p_driver, p_id=edit_cell_id)
                grade_element2 = p_driver.find_element_by_id(edit_cell_id)
                grade_element2.send_keys(gc_score)
                grade_element2.send_keys(Keys.RETURN)

                sql = 'INSERT INTO recorded_scores VALUES ("' + \
                      cell_id + '", "' + gc_assignment_name + '", "' + gc_student + '", ' + \
                      str(gc_score) + ' )'
                execute_sql(p_db_conn, sql)
                print(f"adding  this record.  Assignment: {gc_assignment_name} scholar: {gc_student} score: {gc_score}")

            else:
                print(
                    f"Record is in the DB already.   "
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
    elif p_class:
        try:
            WebDriverWait(p_driver, timeout).until(ec.presence_of_element_located((By.CLASS_NAME, p_class)))
        except TimeoutException:
            if message:
                print(message)
            p_driver.quit()
            raise ValueError(f"Could not find this exact name in the page:{p_class}")
