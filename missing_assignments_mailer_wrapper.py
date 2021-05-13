import os
import shutil
from helper_functions.read_ini_functions import read_classes_info, read_mailer_info
from missing_assignments_mailer import missing_assignments_mailer

# Read in info
config_filename = "crls_teacher_tools.ini"

all_classes = read_classes_info(config_filename)
mailerinfo = read_mailer_info(config_filename)

for gc_name in all_classes.keys():
    print("Sending emails for this class: " + str(gc_name))
    missing_assignments_mailer(config_filename, gc_name, mailerinfo)

input("Press enter 2x to end")