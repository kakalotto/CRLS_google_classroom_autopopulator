import configparser
from classroom_assignments_to_aspen import classroom_assignments_to_aspen

config = configparser.ConfigParser()		
config.read("classroom_assignments_to_aspen.ini")

if 'LOGIN' in config:
    login = config['LOGIN']
    username = login['username']
    password = login['password']
else:
    username = ''
    password = ''
if 'OPTIONS' in config:
    options = config['OPTIONS']
    if 'default_category' in options:
        default_category = options['default_category']
else:
    default_category = ''

classes = config['CLASSES']
gc1 = classes['gc_class1']
aspen1 = classes['aspen_class1']
gc2 = classes['gc_class2']
aspen2 = classes['aspen_class2']
gc3 = classes['gc_class3']
aspen3 = classes['aspen_class3']
gc4 = classes['gc_class4']
aspen4 = classes['aspen_class4']
gc5 = classes['gc_class5']
aspen5 = classes['aspen_class5']
gc6 = classes['gc_class6']
aspen6 = classes['aspen_class6']

content_knowledge_completion_value = config.getboolean("OPTIONS", "content_knowledge_completion")
ignore_ungraded_value = config.getboolean("OPTIONS", "ignore_ungraded")

all_classes = {}
if gc1 and aspen1:
    all_classes[gc1] = aspen1
if gc2 and aspen2:
    all_classes[gc2] = aspen2
if gc3 and aspen3:
    all_classes[gc3] = aspen3
if gc4 and aspen4:
    all_classes[gc4] = aspen4
if gc5 and aspen5:
    all_classes[gc5] = aspen5
if gc6 and aspen6:
    all_classes[gc6] = aspen6

for key in all_classes.keys():
    classroom_assignments_to_aspen(key, all_classes[key],
                                   content_knowledge_completion=content_knowledge_completion_value,
                                   ignore_ungraded=ignore_ungraded_value,
                                   username=username, password=password, default_category=default_category)
