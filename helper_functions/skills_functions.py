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
    import time
    try:
#        WebDriverWait(p_driver, 10).until(ec.presence_of_element_located((By.XPATH, "//input[@class='logonInput']")))
           WebDriverWait(p_driver, 10).until(ec.presence_of_element_located((By.XPATH,
                                                                             '//*[@id="main-box"]/div/form/div[1]/input')))

    except TimeoutException:
        print("Did not find username  button")
        print("quitting")
        p_driver.quit()

    username_field = p_driver.find_element(By.XPATH, '//*[@id="main-box"]/div/form/div[1]/input')
    username_field.click()
    username_field.send_keys(username)
    time.sleep(0.5)
    password_field = p_driver.find_element(By.XPATH, '//*[@id="main-box"]/div/form/div[2]/input')
    password_field.click()
    password_field.send_keys(password)
    time.sleep(0.5)
    sign_in_button = p_driver.find_element(By.XPATH, '//*[@id="sign-in-btn"]')
    sign_in_button.click()
    print("CLICKED!")
    time.sleep(2)
    continue_button = p_driver.find_element(By.XPATH, '//*[@id="continue-btn"]')
    continue_button.click()
    exploratory = p_driver.find_element(By.XPATH, '/html/body/div/div/section/div/div[1]/div/ul/li[3]/div[1]')
    exploratory.click()
    exploratory_attendance_rubric = p_driver.find_element(By.XPATH, '/html/body/div/div/section/div/div[1]/div/ul/li[3]/div[2]/div[3]/form/input[3]')
    exploratory_attendance_rubric.click()

    # continue_button.click()
    # buttons = p_driver.find_element(By.XPATH, "//button")
    # print(buttons)
    # t