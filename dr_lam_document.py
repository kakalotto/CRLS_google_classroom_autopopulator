DOCUMENT_ID = '1KLMCq-Nvq-fCNnkCQ7mayIVOSS-HGupSTG_lPT8EPOI'

from generate_docs_credential import generate_docs_credential
#from generate__credential import generate_sheets_credential
from generate_classroom_credential import generate_classroom_credential

from helper_functions.get_google_drive_id import get_google_drive_id
from helper_functions.get_all_sheets import get_all_sheets
from helper_functions.read_course_id import read_course_id
from helper_functions.read_course_daily_data_all import read_course_daily_data_all
from helper_functions.is_in_past import is_in_past
from helper_functions.read_day_info import read_day_info
from helper_functions.read_lesson_plan import read_lesson_plan
from helper_functions.post_announcement import post_announcement
from helper_functions.post_assignment import post_assignment
from helper_functions.update_sheet_with_id import update_sheet_with_id
from helper_functions.is_work_date_current_date import is_work_date_current_date
from helper_functions.post_assignment_reschedule import post_assignment_reschedule

# Get sheet service credential and service_classroom credential
service_doc = generate_docs_credential()
requests = [
         {
            'insertText': {
                'location': {
                    'index':1,
                },
                'text': 'hello'
            }
        },
                 {
            'insertText': {
                'location': {
                    'index': 2,
                },
                'text': 'world'
            }
        },
                 {
            'insertText': {
                'location': {
                    'index':3,
                },
                'text': 'yes'
            }
        },
    ]

result = service_doc.documents().batchUpdate(documentId=DOCUMENT_ID, body={'requests': requests}).execute()
