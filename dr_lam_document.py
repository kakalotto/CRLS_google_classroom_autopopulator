def dr_lam_document(*, document_id='1KLMCq-Nvq-fCNnkCQ7mayIVOSS-HGupSTG_lPT8EPOI', classroom_id='MTY0OTY1NDEyNjg3',
                    spreadsheet_id='1ZenTcQlCQhbYvBvPOVq8XIB2FQgseIGHH4gTBTcw-KY', sheet_id='APCSP_S1_P1',
                    header_text='AP CSP\n', course_id=164978040288,
                    course_contract_link=
                    'https://docs.google.com/document/d/1eR5rxgTZ0PXy_fYIFK2SS_Ro770IXxT9sM90vZr_OcU/edit',
                    zoom_links=None,
                    assignments_dictionary=None):
    import re
    from generate_docs_credential import generate_docs_credential
    from generate_sheets_credential import generate_sheets_credential
    from generate_classroom_credential import generate_classroom_credential
    from helper_functions.dr_lam_functions import add_table, delete_entire_document, get_final_index, get_text, \
        add_regular_text, add_bold_normal, add_italic_normal, add_link, get_assignment_link
    from helper_functions.dr_lam_requests import requests_header, requests_links
    from helper_functions.read_course_daily_data_all import read_course_daily_data_all

    if zoom_links is None:
        zoom_links = ['https://zoom.us/j/9332367963?pwd=WElmWmc0dHBqSjY2MDFpaWJsbEFsdz09']
    if assignments_dictionary is None:
        assignments_dictionary = {}

    service_doc = generate_docs_credential()
    service_sheets = generate_sheets_credential()
    service_classroom = generate_classroom_credential()
    
    # Start over
    print("Deleting old document")
    doc_contents = get_text(service_doc, document_id)
    delete_entire_document(service_doc, document_id, doc_contents)

    
    # Write header to doc
    print("starting header printout")
    requests = requests_header(header_text, course_contract_link)
    service_doc.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()
    doc_contents = get_text(service_doc, document_id)
    
    # Make a table
    print("Making table")
    requests = []
    requests = add_table(1, 5, requests)
    service_doc.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()
    doc_contents = get_text(service_doc, document_id)
    last_index = get_final_index(doc_contents)

    # Write links to doc
    print("starting links printout")
    requests = requests_links(last_index, classroom_id, zoom_links)
    service_doc.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()
    
    # Read Google classroom for all of the course info
    # coursework = service_classroom.courses().courseWork()
    print("Getting assignments")
    courseworks = service_classroom.courses().courseWork().list(courseId=course_id).execute().get('courseWork', [])
    print("Getting materials")
    materials = service_classroom.courses().\
        courseWorkMaterials().list(courseId=course_id).execute().get('courseWorkMaterial', [])


    # Read Google sheets automator file for info about file names, etc...
    print("Reading info from Google sheets")
    sheet_values = read_course_daily_data_all(spreadsheet_id, sheet_id, service_sheets)
    
    # To get the last index, I need to both reead file.  This is just debugging
    doc_contents = get_text(service_doc, document_id)
    last_index = get_final_index(doc_contents)
    
    # zero batch requests.  Last index, and
    batch_requests = []
    
    index_of_begin_dates = last_index

    for i, value in enumerate(sheet_values):
        print("value" + str(value))
        if len(value) == 3:
            continue
        if i < 88:
            continue
        # if i < 93:
        #     continue
        # if i > 96:
        #     break
        #     break
        # Add day and date header
        day = value[0]
        date = value[1]
        day_of_week = value[2]
        text = "\n" + 'Day ' + str(day) + ' ' + date + " " + day_of_week + "\n"
        [previous_last, last_index, batch_requests] = add_regular_text(text, last_index, batch_requests)
        batch_requests = add_bold_normal(previous_last, last_index, batch_requests)
    
        # Add "Due today:" header
        text = 'Due today:\n'
        [previous_last, last_index, batch_requests] = add_regular_text(text, last_index, batch_requests)
        batch_requests = add_italic_normal(previous_last, last_index, batch_requests)
    
        # Look for what is actually due
        nothing_due = True
        for coursework in courseworks:
            if 'dueDate' in coursework:
                year = coursework['dueDate']['year']
                month = coursework['dueDate']['month']
                day = coursework['dueDate']['day']
                mdy = str(month) + '/' + str(day) + '/' + str(year)
                if mdy == date:
                    nothing_due = False
                    title = coursework['title']
                    title_text = title + '\n'
                    [previous_last, last_index, batch_requests] = \
                        add_regular_text(title_text, last_index, batch_requests)
                    link = get_assignment_link(assignments_dictionary, coursework['title'], courseworks, materials)
                    batch_requests = add_link(link, previous_last, last_index, batch_requests)
        if nothing_due:
            [_, last_index, batch_requests] = add_regular_text('Nothing due yet! '
                                                               '\n', last_index, batch_requests)
    
        # Print out Today header:
        [previous_last, last_index, batch_requests] = add_regular_text('\nToday:\n', last_index, batch_requests)
        batch_requests = add_italic_normal(previous_last, last_index, batch_requests)
    
        # Add Today's assignments
        all_assignments = value[3]
        assignments = all_assignments.split('and ')
    
        for assignment in assignments:
    
            # Get the assignment name
            #print("assignment " + str(assignment))
            clean_assignment = re.sub(r'^\s+', r'', assignment)
            clean_assignment = re.sub(r'\s+$', r'', clean_assignment)
    
            # Get ready to write the name of the assignment
            index_assignment_start = last_index
            assignment_text = clean_assignment + '\n'
            assignment_dict = {
                'insertText': {
                    'location': {
                        'index': last_index,
                    },
                    'text': assignment_text
                }
            }
            last_index += len(clean_assignment) + 1
            batch_requests.append(assignment_dict)
    
            # get the link to the assignment or material
            link = get_assignment_link(assignments_dictionary, clean_assignment, courseworks, materials)
            batch_requests = add_link(link, index_assignment_start, last_index, batch_requests)


        # Add "Class notes:" header
        text = '\nClass Notes:\n'
        [previous_last, last_index, batch_requests] = add_regular_text(text, last_index, batch_requests)
        batch_requests = add_italic_normal(previous_last, last_index, batch_requests)
        notes = '\n'
        if len(value) >= 8:
            notes = value[7]
        [_, last_index, batch_requests] = add_regular_text(notes + '\n\n', last_index, batch_requests)
    
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
    
    print("Adding all of the days")
    # print(batch_requests)
    
    service_doc.documents().batchUpdate(documentId=document_id, body={'requests': batch_requests}).execute()

