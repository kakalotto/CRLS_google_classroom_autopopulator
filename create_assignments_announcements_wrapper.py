import configparser
from helper_functions.read_ini_functions import read_sheets_info
from create_assignments_announcements import create_assignments_announcements

print("Running create_assignments_announcements_wrapper.py")
config = configparser.ConfigParser()
config_filename = "google_classroom_tools.ini"
config.read(config_filename)
sheets = read_sheets_info(config_filename)

for sheet in sheets:
    print(sheet)
    print("Trying to read Google sheet with this spreadsheet ID: " + str(sheet))
    create_assignments_announcements(sheet)