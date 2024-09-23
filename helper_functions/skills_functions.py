def generate_driver():
    """
        Creates a selenium driver object and returns it
    :return: Selenium driver object
    """
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service

    chrome_options = Options()

    service = Service()
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    p_driver = webdriver.Chrome(service=service, options=options)
    p_driver.get('https://skillslibrary-rsta.com/')
    return p_driver


def skills_login(p_driver, *, username='', password=''):
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
    from helper_functions.aspen_functions import click_button
    import time
    try:
#        WebDriverWait(p_driver, 10).until(ec.presence_of_element_located((By.XPATH, "//input[@class='logonInput']")))
           WebDriverWait(p_driver, 10).until(ec.presence_of_element_located((By.XPATH,
                                                                             '//*[@id="main-box"]/div/form/div[1]/input')))

    except TimeoutException:
        print("Did not find username  button")
        print("quitting")
        p_driver.quit()

    username_field = click_button(p_driver, By.XPATH, '//*[@id="main-box"]/div/form/div[1]/input', 2, )
    username_field.send_keys(username)
    password_field = click_button(p_driver, By.XPATH, '//*[@id="main-box"]/div/form/div[2]/input', 2, )
    password_field.send_keys(password)
    time.sleep(0.5)
    sign_in_button = click_button(p_driver, By.XPATH, '//*[@id="sign-in-btn"]', 2, )
    continue_button = click_button(p_driver, By.XPATH, '//*[@id="continue-btn"]', 2, )
    exploratory_button = click_button(p_driver, By.XPATH,
                                      '/html/body/div/div/section/div/div[1]/div/ul/li[3]/div[1]', 2, )
    exploratory_attendance_rubric_button = click_button(p_driver, By.XPATH,
                                      '/html/body/div/div/section/div/div[1]/div/ul/li[3]/div[2]/div[3]/form/input[3]', 2, )

    # time.sleep(0.5)
    # username_field = p_driver.find_element(By.XPATH, '//*[@id="main-box"]/div/form/div[1]/input')
    # username_field.click()

    # password_field = p_driver.find_element(By.XPATH, '//*[@id="main-box"]/div/form/div[2]/input')
    # password_field.click()

    # sign_in_button = p_driver.find_element(By.XPATH, '//*[@id="sign-in-btn"]')
    # sign_in_button.click()
    # continue_button = p_driver.find_element(By.XPATH, '//*[@id="continue-btn"]')
    # continue_button.click()
    # exploratory = p_driver.find_element(By.XPATH, '/html/body/div/div/section/div/div[1]/div/ul/li[3]/div[1]')
    # exploratory.click()
    # exploratory_attendance_rubric = p_driver.find_element(By.XPATH, '/html/body/div/div/section/div/div[1]/div/ul/li[3]/div[2]/div[3]/form/input[3]')
    # exploratory_attendance_rubric.click()
    # continue_button.click()
    # buttons = p_driver.find_element(By.XPATH, "//button")
    # print(buttons)
    # t


def which_rotation(p_changes: list, p_day: int) -> int:
    """

    Args:
        list: list of day changes [1, 4, 9] means rotations change on 1, 4, 9
        int: which day we're at now

    Returns:
        int: rotation number
    """
    for rotation, change_date in reversed(list(enumerate(p_changes))):

        # print(f" in functioni p_day {p_day} and change date {change_date}")
        if p_day >= change_date:
            return rotation + 1


def date_to_classroom_date(google_date:str) -> str :
    google_date_only = google_date.split('T')[0]
    google_date_numbers = google_date_only.split('/')
    print(google_date_numbers)
    p_year = int(google_date_numbers[2])
    p_month = int(google_date_numbers[0])
    p_day = int(google_date_numbers[1])
    year_str = str(p_year)
    if p_month < 10:
        month_str = '0' + str(p_month)
    else:
        month_str = str(p_month)
    if p_day < 10:
        day_str = '0' + str(p_day)
    else:
        day_str = str(p_day)
    return_str = year_str + '-' + month_str + '-' + day_str + 'T08:00:00.000Z'
    return return_str


def date_to_classroom_creation_date(google_date:str) -> str :
    google_date_only = google_date.split('T')[0]
    google_date_numbers = google_date_only.split('/')
    print(google_date_numbers)
    p_year = int(google_date_numbers[2])
    p_month = int(google_date_numbers[0])
    p_day = int(google_date_numbers[1])
    year_str = str(p_year)
    if p_month < 10:
        month_str = '0' + str(p_month)
    else:
        month_str = str(p_month)
    if p_day < 10:
        day_str = '0' + str(p_day)
    else:
        day_str = str(p_day)
    return_str = year_str + '-' + month_str + '-' + day_str + 'T08:00:00.000Z'
    return return_str

def date_to_classroom_due_date(google_date:str) -> dict :
    google_date_only = google_date.split('T')[0]
    google_date_numbers = google_date_only.split('/')
    p_year = int(google_date_numbers[2])
    p_month = int(google_date_numbers[0])
    p_day = int(google_date_numbers[1])
    return {'year': p_year, 'month': p_month, 'day': p_day}