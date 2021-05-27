from create_google_calendar_entries import create_google_calendar_entries
import create_dr_lam_document_config

for gc_class in create_dr_lam_document_config.classes:
    if 'calendar_name' not in gc_class.keys():
        continue
    classname = gc_class['calendar_name']
    spreadsheet_id = gc_class['spreadsheet_id']
    sheet_id = gc_class['sheet_id']
    print(f"Doing this class now: {classname} ")
    create_google_calendar_entries(classname=classname,
                                   spreadsheet_id=spreadsheet_id,
                                   sheet_id=sheet_id)
