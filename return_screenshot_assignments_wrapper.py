import configparser
from classroom_assignments_to_aspen import classroom_assignments_to_aspen
from helper_functions.read_ini_functions import read_return_screenshot_assignments
from return_screenshot_assignments import return_perfect_scores
config = configparser.ConfigParser()

config_filename = "crls_teacher_tools.ini"
classes_dict = read_return_screenshot_assignments(config_filename)

print(classes_dict)

for key in classes_dict:

    return_perfect_scores(key, classes_dict[key])

# for key in all_classes.keys():
#     classroom_assignments_to_aspen(key, all_classes[key],
#                                    content_knowledge_completion=content_knowledge_completion_value,
#                                    ignore_ungraded=ignore_ungraded_value,
#                                    username=username, password=password, default_category=default_category,
#                                    ignore_noduedate=ignore_noduedate_value)

