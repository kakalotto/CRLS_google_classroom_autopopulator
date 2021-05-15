from helper_functions.read_ini_functions import read_classes_info, read_mailer_info
from missing_assignments_mailer import missing_assignments_mailer

# Read in info
config_filename = "crls_teacher_tools.ini"

mailerinfo = read_mailer_info(config_filename)
classes = mailerinfo[0]
student_guardians = mailerinfo[2]
send_email = mailerinfo[4]

for i, gc_name in enumerate(classes):
    print("Sending emails for this class: " + str(gc_name))
    teacherccs = mailerinfo[1]
    teachercc = teacherccs[i]
    messages = mailerinfo[2]
    message = teacherccs[i]
    missing_assignments_mailer(config_filename, gc_name, p_send_email=send_email, p_teachercc=teachercc,
                               p_message=message, p_student_guardian=student_guardians)

input("Press enter 2x to end")
