import configparser
from classroom_assignments_to_aspen import classroom_assignments_to_aspen
from helper_functions.read_ini_functions import read_return_screenshot_assignments
from return_screenshot_assignments import return_screenshot_assignments
config = configparser.ConfigParser()

config_filename = "crls_teacher_tools.ini"
classes_dict = read_return_screenshot_assignments(config_filename)

print(classes_dict)

for key in classes_dict:
    return_screenshot_assignments(key, classes_dict[key])

