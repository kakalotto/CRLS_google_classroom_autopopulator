import configparser
from classroom_grades_to_aspen import classroom_grades_to_aspen
from helper_functions.read_ini_functions import read_classes_info
from mark_missing import mark_missing

# Read in info
config_filename = "crls_teacher_tools.ini"
all_classes = read_classes_info(config_filename)


config = configparser.ConfigParser()
config.read("crls_teacher_tools.ini")

username = config.get('LOGIN', 'username', fallback='')
password = config.get('LOGIN', 'password', fallback='')
content_knowledge_completion_value = config.getboolean("ASPEN", "content_knowledge_completion", fallback=False)
ignore_noduedate_value = config.getboolean('CLASSROOM', 'ignore_no_duedate', fallback=False)
use_stored_gc_students_value = config.getboolean('CLASSROOM', 'use_stored_gc_students', fallback=False)

print(all_classes)
for key in all_classes.keys():
    mark_missing(key, all_classes[key])
