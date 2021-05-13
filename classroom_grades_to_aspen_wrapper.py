import configparser
from classroom_grades_to_aspen import classroom_grades_to_aspen
from helper_functions.read_ini_functions import read_classes_info


# Read in info
config_filename = "crls_teacher_tools.ini"
all_classes = read_classes_info(config_filename)


config = configparser.ConfigParser()
config.read("crls_teacher_tools.ini")

username = config.get('LOGIN', 'username', fallback='')
password = config.get('LOGIN', 'password', fallback='')
content_knowledge_completion_value = config.getboolean("ASPEN", "content_knowledge_completion", fallback=False)

for key in all_classes.keys():
    classroom_grades_to_aspen(key, all_classes[key],
                              content_knowledge_completion=content_knowledge_completion_value,
                              username=username, password=password, p_config_filename=config_filename)
input("Press enter 2x to end")