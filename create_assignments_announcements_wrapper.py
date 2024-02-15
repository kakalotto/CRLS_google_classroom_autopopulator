import configparser
from helper_functions.read_ini_functions import read_sheets_info
from create_assignments_announcements import create_assignments_announcements


print("Runing create_assignments_announcements_wrapper.py")
config = configparser.ConfigParser()

config_filename = "crls_teacher_tools.ini"
config.read(config_filename)
sheets = read_sheets_info(config_filename)

for sheet in sheets:
    print("Currently Trying to read Google sheet with this spreadsheet ID: " + str(sheet))
    create_assignments_announcements(sheet)