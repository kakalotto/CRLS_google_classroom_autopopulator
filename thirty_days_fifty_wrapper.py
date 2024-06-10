import configparser
from classroom_assignments_to_aspen import classroom_assignments_to_aspen
from helper_functions.read_ini_functions import read_thirty_days
from thirty_days_fifty import thirty_days_fifty
config = configparser.ConfigParser()

config_filename = "crls_teacher_tools.ini"
classes = read_thirty_days(config_filename)
print(classes)

for single_class in classes:

    thirty_days_fifty(single_class)

# for key in all_classes.keys():
#     classroom_assignments_to_aspen(key, all_classes[key],
#                                    content_knowledge_completion=content_knowledge_completion_value,
#                                    ignore_ungraded=ignore_ungraded_value,
#                                    username=username, password=password, default_category=default_category,
#                                    ignore_noduedate=ignore_noduedate_value)

