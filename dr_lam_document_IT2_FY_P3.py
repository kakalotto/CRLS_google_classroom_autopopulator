from dr_lam_document import dr_lam_document

DOCUMENT_ID = '1BXeTkfvxq4qMKOWT2Gshkhg7RbzgSjsW_OWUHCkBqDs'
CLASSROOM_ID = 'MTY0ODk5Mjc3OTU5'
SPREADSHEET_ID = '1x0buDsw6pBjK1GJkZXc5mMo86dX7FnWj4daMn_5CyLc'
SHEET_ID = 'IT2'
HEADER_TEXT = 'IT2 \n'
COURSE_ID = 164899277959
COURSE_CONTRACT = 'https://docs.google.com/document/d/1eR5rxgTZ0PXy_fYIFK2SS_Ro770IXxT9sM90vZr_OcU/edit'
ZOOM_LINK_1 = 'https://zoom.us/j/9332367963?pwd=WElmWmc0dHBqSjY2MDFpaWJsbEFsdz09'
ZOOM_LINKS = [ZOOM_LINK_1,]
assignments_dictionary = {
}


dr_lam_document(document_id=DOCUMENT_ID, classroom_id=CLASSROOM_ID, spreadsheet_id=SPREADSHEET_ID, sheet_id=SHEET_ID,
                header_text=HEADER_TEXT, course_id=COURSE_ID, zoom_links=ZOOM_LINKS,
                assignments_dictionary=assignments_dictionary, course_contract_link=COURSE_CONTRACT)