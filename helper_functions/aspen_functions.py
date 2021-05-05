def generate_driver():
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager

    chrome_options = Options()
    chrome_options.add_argument("Window-size=6500,12000")
    p_driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    p_driver.get('https://aspen.cpsd.us')
    return p_driver


def aspen_login(p_driver, *, username='', password=''):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.support import expected_conditions as ec
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException, NoSuchElementException

    try:
        element = WebDriverWait(p_driver, 10). \
            until(ec.presence_of_element_located((By.XPATH, "//input[@class='logonInput']")))
    except TimeoutException:
        print("Did not find logon screen")
        print("quitting")
        p_driver.quit()

    if username and password:
        print("Login supplied via script.")
        login = p_driver.find_element_by_xpath("//input[@class='logonInput']").send_keys(username)
        password = p_driver.find_element_by_xpath("//input[@name='password']").send_keys(password)
        submit = p_driver.find_element_by_xpath("//button").click()
    else:
        print("Login credentials not supplied.  Manual login")
        try:
            element = WebDriverWait(p_driver, 30). \
                until(ec.presence_of_element_located((By.XPATH, "//a[@title='Gradebook tab']")))
        except TimeoutException:
            print("Did not log in successfully after 30 seconds")
            print("quitting")
            p_driver.quit()



