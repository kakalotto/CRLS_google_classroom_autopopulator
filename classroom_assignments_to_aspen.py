

def classroom_assignments_to_aspen(*, username='', password=''):
    from generate_classroom_credential import generate_classroom_credential
    from helper_functions.aspen_functions import generate_driver, aspen_login
    service_classroom = generate_classroom_credential()
    driver = generate_driver()
    aspen_login(driver, username=username, password=password)