from dr_lam_document2 import dr_lam_document_2

DOCUMENT_ID = '1BXeTkfvxq4qMKOWT2Gshkhg7RbzgSjsW_OWUHCkBqDs'
CLASSROOM_ID = 'MTY0ODk5Mjc3OTU5'
SPREADSHEET_ID = '1x0buDsw6pBjK1GJkZXc5mMo86dX7FnWj4daMn_5CyLc'
SHEET_ID = 'IT2'
HEADER_TEXT = 'Cybersecurity/Info Tech 2 testing\n'
COURSE_ID = 164899277959
COURSE_CONTRACT = 'https://docs.google.com/document/d/1SO6sNLq6W7Bw2k7zYD6qxHuBSgCa0pYeRU14I6YJQTg/edit'
ZOOM_LINK_1 = 'https://zoom.us/j/9332367963?pwd=WElmWmc0dHBqSjY2MDFpaWJsbEFsdz09'
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
fy=True

dr_lam_document_2(document_id=DOCUMENT_ID, classroom_id=CLASSROOM_ID, spreadsheet_id=SPREADSHEET_ID, sheet_id=SHEET_ID,
                header_text=HEADER_TEXT, course_id=COURSE_ID, zoom_links=ZOOM_LINKS,
                assignments_dictionary=assignments_dictionary, course_contract_link=COURSE_CONTRACT, fy='fy')