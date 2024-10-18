import configparser
from classroom_grades_to_aspen import classroom_grades_to_aspen
from helper_functions.read_ini_functions import read_classes_info


# Read in info
config_filename = "crls_teacher_tools.ini"
print(f"Opening up this config file now: {config_filename}")
all_classes = read_classes_info(config_filename)


config = configparser.ConfigParser()
config.read("crls_teacher_tools.ini")

username = config.get('LOGIN', 'username', fallback='')
password = config.get('LOGIN', 'password', fallback='')
content_knowledge_completion_value = config.getboolean("ASPEN", "content_knowledge_completion", fallback=False)
ignore_noduedate_value = config.getboolean('CLASSROOM', 'ignore_no_duedate', fallback=False)
use_stored_gc_students_value = config.getboolean('CLASSROOM', 'use_stored_gc_students', fallback=False)

counter = 1
for key in all_classes.keys():
    print(f"We are in classroom_grades_to_aspen_wrapper, on this class number: {counter}")
    classroom_grades_to_aspen(key, all_classes[key],
                              content_knowledge_completion=content_knowledge_completion_value,
                              username=username, password=password, p_config_filename=config_filename,
                              p_ignore_noduedate=ignore_noduedate_value,
                              p_use_stored_gc_students=use_stored_gc_students_value)
    counter = counter + 1

input("Press enter 2x to end")

# ("https://www.googleapis.com/auth/classroom.courses "
#  "https://www.googleapis.com/auth/documents "
#  "https://www.googleapis.com/auth/classroom.topics "
#  "https://www.googleapis.com/auth/spreadsheets "
#  "https://www.googleapis.com/auth/classroom.coursework.students "
#  "https://www.googleapis.com/auth/classroom.courseworkmaterials "
#  "https://www.googleapis.com/auth/classroom.announcements "
#  "https://www.googleapis.com/auth/classroom.profile.emails ")
# to
# ("https://www.googleapis.com/auth/classroom.courses "
#  "https://www.googleapis.com/auth/documents "
#  "https://www.googleapis.com/auth/classroom.topics "
#  "https://www.googleapis.com/auth/spreadsheets "
#  "https://www.googleapis.com/auth/classroom.coursework.students "
#  "https://www.googleapis.com/auth/classroom.courseworkmaterials"
#  " https://www.googleapis.com/auth/classroom.announcements "
#  "https://www.googleapis.com/auth/classroom.profile.emails").
