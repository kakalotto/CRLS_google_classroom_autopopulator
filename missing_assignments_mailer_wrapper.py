from helper_functions.read_ini_functions import read_mailer_info
from missing_assignments_mailer import missing_assignments_mailer
import get_student_info_config  # gives us class_students_dict
import missing_assignments_mailer_assignments_dict
classes_students_dict = get_student_info_config.class_students_dict
# nicknames_dict = get_student_info_config.nicknames_dict
past_blurbs_dict = missing_assignments_mailer_assignments_dict.past_days
future_blurbs_dict = missing_assignments_mailer_assignments_dict.future_days
nicknames_dict = missing_assignments_mailer_assignments_dict.nicknames_dict
# Read in info
config_filename = "crls_teacher_tools.ini"

mailerinfo = read_mailer_info(config_filename)
classes = mailerinfo[0]
scholar_guardians = mailerinfo[3]
send_email = mailerinfo[4]
spreadsheet_ids = mailerinfo[5]
sheet_ids = mailerinfo[6]
# class_students_dict

print(classes_students_dict)
for i, gc_name in enumerate(classes):
    if not gc_name:
        continue
    print("Sending emails for this class: " + str(gc_name))
    teacherccs = mailerinfo[1]
    teachercc = teacherccs[i]
    messages = mailerinfo[2]
    message = messages[i]
    missing_assignments_mailer(config_filename, gc_name, p_send_email=send_email, p_teachercc=teachercc,
                               p_message=message, p_scholar_guardians=scholar_guardians,
                               p_classes_students_dict=classes_students_dict, p_nicknames_dict=nicknames_dict,
                               p_spreadsheet_id=spreadsheet_ids[i], p_sheet_id=sheet_ids[i],
                               p_past_blurbs_dict=past_blurbs_dict, p_future_blurbs_dict=future_blurbs_dict)

input("Press enter 2x to end")
