from dr_lam_document import dr_lam_document

DOCUMENT_ID = '1miz7EgIEna8W5fn8wJPqn0U3TL2i49tTORKTOaGoLQs'
CLASSROOM_ID = 'MjUzNzIxNDA3NzA1'
SPREADSHEET_ID = '1ZenTcQlCQhbYvBvPOVq8XIB2FQgseIGHH4gTBTcw-KY'
SHEET_ID = 'APCSP_S2_P4'
HEADER_TEXT = 'AP CSP\n'
COURSE_ID = 253721407705
COURSE_CONTRACT = 'https://docs.google.com/document/d/1eR5rxgTZ0PXy_fYIFK2SS_Ro770IXxT9sM90vZr_OcU/edit'
ZOOM_LINK_1 = 'https://zoom.us/j/9332367963?pwd=WElmWmc0dHBqSjY2MDFpaWJsbEFsdz09'
ZOOM_LINK_2 = 'https://zoom.us/j/4968074808?pwd=ZVBJQzQ4Uk1NREpGNEhLakJ4blExUT09'
ZOOM_LINK_3 = 'https://us02web.zoom.us/j/7890036306?pwd=WlpkV1JKUXZlQ3orYTd2dFBhZkdzdz09'
ZOOM_LINKS = [ZOOM_LINK_1, ZOOM_LINK_2, ZOOM_LINK_3]
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