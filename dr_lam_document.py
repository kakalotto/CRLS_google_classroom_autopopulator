from helper_functions.read_course_daily_data_all import read_course_daily_data_all
import re
from generate_docs_credential import generate_docs_credential
from generate_sheets_credential import generate_sheets_credential
from generate_classroom_credential import generate_classroom_credential
from helper_functions.dr_lam_functions import delete_entire_document, get_final_index, get_text, add_regular_text
from helper_functions.dr_lam_requests import requests_header, requests_links
from helper_functions.read_course_daily_data_all import read_course_daily_data_all

DOCUMENT_ID = '1KLMCq-Nvq-fCNnkCQ7mayIVOSS-HGupSTG_lPT8EPOI'
ORIGINAL_DOC_ID = '1N-kPKpq3qQXONAsUS7iveyJGAhE0OGoqXzYYTn38lRM'
CLASSROOM_ID = 'MTY0OTY1NDEyNjg3'
SPREADSHEET_ID = '1ZenTcQlCQhbYvBvPOVq8XIB2FQgseIGHH4gTBTcw-KY'
SHEET_ID = 'APCSP_S1_P1'
COURSE_CONTRACT = 'https://docs.google.com/document/d/1eR5rxgTZ0PXy_fYIFK2SS_Ro770IXxT9sM90vZr_OcU/edit'
ZOOM_LINK = 'https://zoom.us/j/4968074808?pwd=ZVBJQzQ4Uk1NREpGNEhLakJ4blExUT09#success'
CLASSROOM_LINK = 'https://classroom.google.com/u/0/c/' + CLASSROOM_ID
ASSIGNED_LINK = 'https://classroom.google.com/u/0/a/not-turned-in/' + CLASSROOM_ID
MISSING_LINK = 'https://classroom.google.com/u/0/a/missing/' + CLASSROOM_ID
ASPEN_LINK = 'https://aspen.cpsd.us'
DUMMY = ''

HEADER_TEXT = 'AP CSP S1 P1\n'
COURSE_ID = 164978040288

service_doc = generate_docs_credential()
service_sheets = generate_sheets_credential()
service_classroom = generate_classroom_credential()

# Start over
doc_contents = get_text(service_doc, DOCUMENT_ID)
delete_entire_document(service_doc, DOCUMENT_ID, doc_contents)
print("Deletion done")

# Write header to doc
print("starting header printout")
requests = requests_header(HEADER_TEXT)
result = service_doc.documents().batchUpdate(documentId=DOCUMENT_ID, body={'requests': requests}).execute()

# Write links to doc
print("starting links printout")
requests = requests_links(ZOOM_LINK, ASPEN_LINK, CLASSROOM_LINK, ASSIGNED_LINK, MISSING_LINK)
result2 = service_doc.documents().batchUpdate(documentId=DOCUMENT_ID, body={'requests': requests}).execute()

# abc = get_text(service_doc, DOCUMENT_ID)
# for item in abc:
#     print(item)
#     print("\n")
#     print()

# Read Google classroom for all of the course info
# coursework = service_classroom.courses().courseWork()
courseworks = service_classroom.courses().courseWork().list(courseId=COURSE_ID).execute().get('courseWork', [])
for coursework in courseworks:
    print(coursework)

# Read Google sheets automator file for info about file names, etc...
sheet_values = read_course_daily_data_all(SPREADSHEET_ID, SHEET_ID, service_sheets)
print(sheet_values[0:5])

# To get the last index, I need to both reead file.  This is just debugging
doc_contents = get_text(service_doc, DOCUMENT_ID)
print("LAST!!")
last_index = get_final_index(doc_contents)

# zero batch requests.  Last index, and
batch_requests = []

index_of_begin_dates = last_index
initial_index = last_index
previous_last = 0

for i, value in enumerate(sheet_values):
    if i > 89:
        break
    if len(value) == 3:
        continue

    # Add day and date header
    day = value[0]
    date = value[1]
    day_of_week = value[2]
    text = "\n" + 'Day ' + str(day) + ' ' + date + " " + day_of_week + "\n"
    [previous_last, last_index, batch_requests] = add_regular_text(text, last_index, batch_requests)


    # Add "Due today:" header
    text = 'Due today:\n'
    [previous_last, last_index, batch_requests] = add_regular_text(text, last_index, batch_requests)
    new_last_index = last_index

    # Look for what is actually due
    for coursework in courseworks:
        if 'dueDate' in coursework:
            year = coursework['dueDate']['year']
            month = coursework['dueDate']['month']
            day = coursework['dueDate']['day']
            mdy = str(month) + '/' + str(day) + '/' + str(year)
            # print("DATE AND MDY" + str(date) + str(mdy))

            if mdy == date:
                title = coursework['title']
                title_text = title + '\n'
                due_today = {
                    'insertText': {
                        'location': {
                            'index': new_last_index,
                        },
                        'text': title_text
                    }
                }
                batch_requests.append(due_today)
                new_last_index += len(title_text)
                
    ##batch_requests.append(due_today)
    # new_last_index += len(title_text)

    newline = {
        'insertText': {
            'location': {
                'index': new_last_index,
            },
            'text': '\n'
        }
    }
    new_last_index += 1
    batch_requests.append(newline)

    all_assignments = value[3]
    assignments = all_assignments.split('and ')
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
    for assignment in assignments:

        # Get the assignment name
        print("assignment " + str(assignment))
        clean_assignment = re.sub(r'^\s+', r'', assignment)
        clean_assignment = re.sub(r'\s+$', r'', assignment)


        # Get ready to write the name of the assignment
        index_assignment_start = new_last_index
        assignment_text = clean_assignment + '\n'
        assignment_dict = {
            'insertText': {
                'location': {
                    'index': new_last_index,
                },
                'text': assignment_text
            }
        }
        new_last_index += len(clean_assignment) + 1
        batch_requests.append(assignment_dict)
        last_index = new_last_index

        # get the link to the assignment
        for coursework in courseworks:
            link = ''
            if clean_assignment in assignments_dictionary:
                clean_assignment = assignments_dictionary[clean_assignment]
            if clean_assignment == coursework['title']:
                print('MATCH! ' + coursework['title'])
                link = coursework['alternateLink']
                print("LINK!! " + link)

        # Turn the written assignment into a link
            link_request = {
                               'updateTextStyle': {
                                   'range': {
                                       'startIndex': index_assignment_start,
                                       'endIndex': last_index
                                   },
                                   'textStyle': {
                                       'link': {
                                           'url': link
                                       }
                                   },
                                   'fields': 'link'
                               }
                           },
            batch_requests.append(link_request)
    last_index = new_last_index
    print("new last index")
    print(last_index)


formatting = {
    "updateParagraphStyle": {
        "range": {
            "startIndex": index_of_begin_dates,
            "endIndex": last_index
        },
        "paragraphStyle": {
            "alignment": "START"
        },
        "fields": "alignment"
    }
}
batch_requests.append(formatting)

print("TRYING THIS")
# print(batch_requests)

result = service_doc.documents().batchUpdate(documentId=DOCUMENT_ID, body={'requests': batch_requests}).execute()


doc_contents = get_text(service_doc, DOCUMENT_ID)
print("LAST END OF FILE")
print(get_final_index(doc_contents))
