from dr_lam_document import dr_lam_document

DOCUMENT_ID = '12thEXqiR-M2ligPF5Y2g4VR7jYRR4si2pwpkEeNRSqE'
CLASSROOM_ID = 'MjM0MzU5NDg1Njg2'
SPREADSHEET_ID = '1HBh9DcDUaKiyH_X5w_-qCh-Aw_0JZD-Rtzg_PfiER3Y'
SHEET_ID = 'APCSP_S2_P1'
HEADER_TEXT = 'AP CSP\n'
COURSE_ID = 234359485686
COURSE_CONTRACT = 'https://docs.google.com/document/d/1eR5rxgTZ0PXy_fYIFK2SS_Ro770IXxT9sM90vZr_OcU/edit'
ZOOM_LINK_1 = 'https://zoom.us/j/4968074808?pwd=ZVBJQzQ4Uk1NREpGNEhLakJ4blExUT09#success'
ZOOM_LINK_2 = 'https://zoom.us/j/9332367963?pwd=WElmWmc0dHBqSjY2MDFpaWJsbEFsdz09'
ZOOM_LINKS = [ZOOM_LINK_1, ZOOM_LINK_2]
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