from dr_lam_document import dr_lam_document

DOCUMENT_ID = '12BgUzPEsYC3Z8EuJ9aQEStRw5BSgX-EeowEcPJ3sJ-A'
CLASSROOM_ID = 'MjQ2OTY4NDI4Mzcw'
SPREADSHEET_ID = '1o_YPtSYB75fk9-r79GhNVqTDdkWr0VZA497nrC4r1h0'
SHEET_ID = 'ICS_S2P1'
HEADER_TEXT = 'Intro to Computer Science\n'
COURSE_ID = 246968428370
COURSE_CONTRACT = 'https://docs.google.com/document/d/10UgK6pP2UcaXu8ErPBk_MNNDZ82i93AwijWXLplN01M/edit?usp=drive_open&ouid=110067882309555165220'
ZOOM_LINK_1 = 'https://zoom.us/j/5163593350?pwd=MzVVRktGcVZ4a0tEbXRwRGJDaFAxZz09#success'
ZOOM_LINKS = [ZOOM_LINK_1]
assignments_dictionary = {
    'Create task practice 1': 'Create task practice',
    'Create task practice 2': 'Create task practice',
    'Create task practice 3': 'Create task practice',
    'Create task practice 4': 'Create task practice',
    'Create task practice 5': 'Create task practice',
    'Create task practice 6': 'Create task practice',
    'Create task 1': 'Create task',
    'Create task 2': 'Create task',
    'Create task 3': 'Create task',
    'Create task 4': 'Create task',
    'Create task 5': 'Create task',
    'Create task 6': 'Create task',
    'Create task 7': 'Create task',
    'Create task 8': 'Create task',
    'Create task 9': 'Create task',
    'Create task 10': 'Create task',
    'Create task 11': 'Create task',
    'Create task 12': 'Create task',
}


dr_lam_document(document_id=DOCUMENT_ID, classroom_id=CLASSROOM_ID, spreadsheet_id=SPREADSHEET_ID, sheet_id=SHEET_ID,
                header_text=HEADER_TEXT, course_id=COURSE_ID, zoom_links=ZOOM_LINKS,
                assignments_dictionary=assignments_dictionary, course_contract_link=COURSE_CONTRACT)