DOCUMENT_ID = '1KLMCq-Nvq-fCNnkCQ7mayIVOSS-HGupSTG_lPT8EPOI'
ORIGINAL_DOC_ID = '1N-kPKpq3qQXONAsUS7iveyJGAhE0OGoqXzYYTn38lRM'
CLASSROOM_ID = 'MTY0OTY1NDEyNjg3'
COURSE_CONTRACT = 'https://docs.google.com/document/d/1eR5rxgTZ0PXy_fYIFK2SS_Ro770IXxT9sM90vZr_OcU/edit'
ZOOM_LINK = 'https://zoom.us/j/4968074808?pwd=ZVBJQzQ4Uk1NREpGNEhLakJ4blExUT09#success'
CLASSROOM_LINK = 'https://classroom.google.com/u/0/c/MTY0OTc4MDQwMjg4'
ASSIGNED_LINK = 'https://classroom.google.com/u/0/a/not-turned-in/MTY0OTc4MDQwMjg4'
ASPEN_LINK = 'https://aspen.cpsd.us'
COURSE_ID = 164978040288


def get_text(p_service, document_id):
    document = p_service.documents().get(documentId=document_id).execute()
    doc_content = document.get('body').get('content')
    return doc_content


def delete_entire_document(p_service, document_id, p_doc_content):
    import re

    matches = re.findall(r"'endIndex':\s([0-9]+)", str(p_doc_content), re.X | re.M | re.S)
    if matches:
        last_number = matches[-1]
        print(last_number)
    last_number = int(last_number)
    last_number -= 1
    print(last_number)
    p_requests = [
        {
            'deleteContentRange': {
                'range': {
                    'startIndex': 1,
                    'endIndex': last_number,
                }

            }

        },
    ]
    if last_number > 2:
        result = p_service.documents().batchUpdate(documentId=document_id, body={'requests': p_requests}).execute()
        return result
    else:
        return None


from generate_docs_credential import generate_docs_credential
from generate_sheets_credential import generate_sheets_credential
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

# Start over
doc_contents = get_text(service_doc, DOCUMENT_ID)
delete_entire_document(service_doc, DOCUMENT_ID, doc_contents)
print("Deletion done")
# Header
header_text = 'AP CSP S1 P1\n'

# ends at 14
requests = [
    {
        'insertText': {
            'location': {
                'index': 1,
            },
            'text': header_text
        }
    },
    {
        'insertText': {
            'location': {
                'index': 14,
            },
            'text': 'Semester schedule and calendar\n\n\n'
        }
    },
    {
        'updateTextStyle': {
            'range': {
                'startIndex': 1,
                'endIndex': 47
            },
            'textStyle': {
                'bold': True,
                'fontSize': {"magnitude": 16, "unit": "pt"},
            },
            'fields': '*'
        }
    },
    {
        "updateParagraphStyle": {
            "range": {
                "startIndex": 1,
                "endIndex": 47
            },
            "paragraphStyle": {
                "alignment": "CENTER"
            },
            "fields": "alignment"
        }
    },
    {
        'insertText': {
            'location': {
                'index': 47,
            },
            'text': 'This document contains the schedule of activities for the entire semester. It includes links and '
                    'resources that you’ll need before, during, and after class. It should be your first point of '
                    'reference when you need to know what to do. Please have it open during every class session.\n\n\n'
                    'This document is automatically generated via computer script.  '
                    'Schedules are subject to change.  Dates that are further out are less likely to be accurate.\n\n'
        }
    },
    {
        'insertText': {
            'location': {
                'index': 488,
            },
            'text': 'Please see the course contract for information on grading and class policies\n\n'
        }
    },
    {
        'updateTextStyle': {
            'range': {
                'startIndex': 503,
                'endIndex': 518
            },
            'textStyle': {
                'link': {
                    'url': 'https://docs.google.com/document/d/1eR5rxgTZ0PXy_fYIFK2SS_Ro770IXxT9sM90vZr_OcU/edit#bookmark=id.gs88mpq2vwt'
                }
            },
            'fields': 'link'
        }
    },
    {
        'insertText': {
            'location': {
                'index': 566,
            },
            'text': 'Links\n\n'
        }
    },
    {
        'updateTextStyle': {
            'range': {
                'startIndex': 566,
                'endIndex': 571
            },
            'textStyle': {
                'bold': True,
                'fontSize': {"magnitude": 16, "unit": "pt"},
            },
            'fields': '*'
        }
    },
    {
        'insertTable': {
            'rows': 1,
            'columns': 5,
            'endOfSegmentLocation': {
                'segmentId': ''
            }
        },
    },

]
requests2 = [
    {
        'insertInlineImage': {
            'location': {
                'index': 577
            },
            'uri':
                'http://crls-autograder.herokuapp.com/static/zoom.PNG',
            'objectSize': {
                'height': {
                    'magnitude': 75,
                    'unit': 'PT'
                },
                'width': {
                    'magnitude': 75,
                    'unit': 'PT'
                }
            }
        }
    },
    {
        'insertText': {
            'location': {
                'index': 578,
            },
            'text': '    Zoom'
        }
    },
    {
        'updateTextStyle': {
            'range': {
                'startIndex': 578,
                'endIndex': 587
            },
            'textStyle': {
                'link': {
                    'url': ZOOM_LINK
                }
            },
            'fields': 'link'
        }
    },
    {
        "updateParagraphStyle": {
            "range": {
                "startIndex": 578,
                "endIndex": 587
            },
            "paragraphStyle": {
                "alignment": "CENTER"
            },
            "fields": "alignment"
        }
    },



    {
        'insertInlineImage': {
            'location': {
                'index': 588
            },
            'uri':
                'http://crls-autograder.herokuapp.com/static/classroom.PNG',
            'objectSize': {
                'height': {
                    'magnitude': 75,
                    'unit': 'PT'
                },
                'width': {
                    'magnitude': 75,
                    'unit': 'PT'
                }
            }
        }
    },
    {
        'insertText': {
            'location': {
                'index': 589,
            },
            'text': 'Google classroom'
        }
    },
    {
        'updateTextStyle': {
            'range': {
                'startIndex': 589,
                'endIndex': 605
            },
            'textStyle': {
                'link': {
                    'url': CLASSROOM_LINK
                }
            },
            'fields': 'link'
        }
    },
    {
        "updateParagraphStyle": {
            "range": {
                "startIndex": 589,
                "endIndex": 600
            },
            "paragraphStyle": {
                "alignment": "CENTER"
            },
            "fields": "alignment"
        }
    },
    {
        'insertInlineImage': {
            'location': {
                'index': 607
            },
            'uri':
                'http://crls-autograder.herokuapp.com/static/assigned.PNG',
            'objectSize': {
                'height': {
                    'magnitude': 75,
                    'unit': 'PT'
                },
                'width': {
                    'magnitude': 75,
                    'unit': 'PT'
                }
            }
        }
    },
    {
        'insertText': {
            'location': {
                'index': 608,
            },
            'text': 'Google classroom assigned work'
        }
    },
    {
        'updateTextStyle': {
            'range': {
                'startIndex': 608,
                'endIndex': 640
            },
            'textStyle': {
                'link': {
                    'url': ASSIGNED_LINK
                }
            },
            'fields': 'link'
        }
    },
    {
        "updateParagraphStyle": {
            "range": {
                "startIndex": 608,
                "endIndex": 620
            },
            "paragraphStyle": {
                "alignment": "CENTER"
            },
            "fields": "alignment"
        }
    },


    {
        'insertInlineImage': {
            'location': {
                'index': 640
            },
            'uri':
                'http://crls-autograder.herokuapp.com/static/missing.PNG',
            'objectSize': {
                'height': {
                    'magnitude': 75,
                    'unit': 'PT'
                },
                'width': {
                    'magnitude': 75,
                    'unit': 'PT'
                }
            }
        }
    },
    {
        'insertText': {
            'location': {
                'index': 641,
            },
            'text': 'Google classroom missing work'
        }
    },
    {
        'updateTextStyle': {
            'range': {
                'startIndex': 641,
                'endIndex': 670
            },
            'textStyle': {
                'link': {
                    'url': ASSIGNED_LINK
                }
            },
            'fields': 'link'
        }
    },
    {
        "updateParagraphStyle": {
            "range": {
                "startIndex": 641,
                "endIndex": 655
            },
            "paragraphStyle": {
                "alignment": "CENTER"
            },
            "fields": "alignment"
        }
    },

    {
        'insertInlineImage': {
            'location': {
                'index': 672
            },
            'uri':
                'http://crls-autograder.herokuapp.com/static/aspen.PNG',
            'objectSize': {
                'height': {
                    'magnitude': 75,
                    'unit': 'PT'
                },
                'width': {
                    'magnitude': 75,
                    'unit': 'PT'
                }
            }
        }
    },
    {
        'insertText': {
            'location': {
                'index': 673,
            },
            'text': 'Aspen'
        }
    },
    {
        'updateTextStyle': {
            'range': {
                'startIndex': 673,
                'endIndex': 681
            },
            'textStyle': {
                'link': {
                    'url': ASPEN_LINK
                }
            },
            'fields': 'link'
        }
    },
    {
        "updateParagraphStyle": {
            "range": {
                "startIndex": 673,
                "endIndex": 681
            },
            "paragraphStyle": {
                "alignment": "CENTER"
            },
            "fields": "alignment"
        }
    },

    # {
    #     'insertText': {
    #         'location': {
    #             'index': 581,
    #         },
    #         'text': 'Google classroom missing\n\n'
    #     }
    # },
    # {
    #     'insertText': {
    #         'location': {
    #             'index': 600,
    #         },
    #         'text': 'Aspen\n\n'
    #     }
    # },
]


#
# requests3 = [
#     {
#         'insertText': {
#             'location': {
#                  'index': offset,
#             },
#             'text': '    end of line'
#         }
#     },
# ]

print("starting request")
result = service_doc.documents().batchUpdate(documentId=DOCUMENT_ID, body={'requests': requests}).execute()
print("request 1 done")
abc = get_text(service_doc, DOCUMENT_ID)
# for item in abc:
#     print(item)
#     print("\n")
#     print()
result = service_doc.documents().batchUpdate(documentId=DOCUMENT_ID, body={'requests': requests2}).execute()
#result = service_doc.documents().batchUpdate(documentId=DOCUMENT_ID, body={'requests': requests3}).execute()

abc = get_text(service_doc, DOCUMENT_ID)
for item in abc:
    print(item)
    print("\n")
    print()


service_classroom = generate_classroom_credential()
course_results = service_classroom.courses().get(id=COURSE_ID).execute()
print(course_results)
coursework = service_classroom.courses().courseWork()
assignments = service_classroom.courses().courseWork().list(courseId=COURSE_ID).execute().get('courseWork', [])

service_sheet = generate_sheets_credential()

for assignment in assignments:
    if 'title' in assignment:
        print(assignment['title'])
    else:
        print("NO TITLE")
    print(assignment)
    # original_text = get_text(service_doc, ORIGINAL_DOC_ID)
# for item in original_text:
#     print(item)
#     print("\n")
#     print()

'''
. 