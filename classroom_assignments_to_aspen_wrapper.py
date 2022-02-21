import configparser
from classroom_assignments_to_aspen import classroom_assignments_to_aspen
from helper_functions.read_ini_functions import read_classes_info

config = configparser.ConfigParser()		

config_filename = "crls_teacher_tools_assignments.ini"
all_classes = read_classes_info(config_filename)


config = configparser.ConfigParser()
config.read(config_filename)

username = config.get('LOGIN', 'username', fallback='')
password = config.get('LOGIN', 'password', fallback='')
content_knowledge_completion_value = config.getboolean("ASPEN", "content_knowledge_completion", fallback=False)
default_category = config.get("ASPEN", "default_category", fallback='')
ignore_ungraded_value = config.getboolean('CLASSROOM', 'ignore_ungraded', fallback=False)
ignore_noduedate_value = config.getboolean('CLASSROOM', 'ignore_no_duedate', fallback=False)

print(all_classes)

for key in all_classes.keys():
    classroom_assignments_to_aspen(key, all_classes[key],

                                   content_knowledge_completion=content_knowledge_completion_value,
                                   ignore_ungraded=ignore_ungraded_value,
                                   username=username, password=password, default_category=default_category,
                                   ignore_noduedate=ignore_noduedate_value)

input("Press enter 2x to end")
