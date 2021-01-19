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


def get_final_index(p_doc_content):
    import re
    matches = re.findall(r"'endIndex':\s([0-9]+)", str(p_doc_content), re.X | re.M | re.S)
    if matches:
        last_number = matches[-1]
        print(last_number)
    last_number = int(last_number)
    last_number -= 1
    return last_number


def get_text(p_service, document_id):
    document = p_service.documents().get(documentId=document_id).execute()
    doc_content = document.get('body').get('content')
    return doc_content