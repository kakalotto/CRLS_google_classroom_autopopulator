from helper_functions.read_ini_functions import read_mailer_info
from missing_assignments_mailer import missing_assignments_mailer

# Read in info
config_filename = "crls_teacher_tools.ini"

mailerinfo = read_mailer_info(config_filename)
classes = mailerinfo[0]
scholar_guardians = mailerinfo[3]
send_email = mailerinfo[4]

print(classes)
for i, gc_name in enumerate(classes):
    if not gc_name:
        continue
    print("Sending emails for this class: " + str(gc_name))
    teacherccs = mailerinfo[1]
    teachercc = teacherccs[i]
    messages = mailerinfo[2]
    message = messages[i]
    missing_assignments_mailer(config_filename, gc_name, p_send_email=send_email, p_teachercc=teachercc,
                               p_message=message, p_scholar_guardians=scholar_guardians)

input("Press enter 2x to end")
