from create_google_calendar_entries import create_google_calendar_entries
create_google_calendar_entries(classname='test this calendar',
                               spreadsheet_id='1S_Uht3qBT_VY1AVMlutGeNVcUyYYc6BIzDYEJbFMvO8',
                               sheet_id='testing')
#from create_dr_lam_document import create_dr_lam_document
# for gc_class in create_dr_lam_document_config.classes:
#     document_id = gc_class['document_id']
#     classroom_id = gc_class['classroom_id']
#     spreadsheet_id = gc_class['spreadsheet_id']
#     sheet_id = gc_class['sheet_id']
#     header_text = gc_class['header_text']
#     course_id = gc_class['course_id']
#     course_contract = gc_class['course_contract']
#     zoom_links = gc_class['zoom_links']
#     assignments_dictionary = gc_class['assignments_dictionary']
#     fy = gc_class['fy']
#     print(f"Doing this class now: {header_text} ")
#     create_dr_lam_document(document_id=document_id, classroom_id=classroom_id,
#                            spreadsheet_id=spreadsheet_id, sheet_id=sheet_id,
#                            header_text=header_text, course_id=course_id, zoom_links=zoom_links,
#                            assignments_dictionary=assignments_dictionary,
#                            course_contract_link=course_contract, fy=fy)
