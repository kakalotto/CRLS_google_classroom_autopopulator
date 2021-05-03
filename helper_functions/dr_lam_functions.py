def add_image(p_link, index_start, p_batch_requests, *, p_height=75, p_width=75):
    batch = {
            'insertInlineImage': {
                'location': {
                    'index': index_start
                },
                'uri':
                    p_link,
                'objectSize': {
                    'height': {
                        'magnitude': p_height,
                        'unit': 'PT'
                    },
                    'width': {
                        'magnitude': p_width,
                        'unit': 'PT'
                    }
                }
            }
        },
    p_batch_requests.append(batch)
    index_end = index_start + 1
    return [index_start, index_end, p_batch_requests]


def add_regular_text(p_text, index_start, p_batch_requests):
    batch = {
        'insertText': {
            'location': {
                'index': index_start,
            },
            'text':  p_text
        }
    }
    p_batch_requests.append(batch)
    index_end = index_start + len(p_text)
    return [index_start, index_end, p_batch_requests]


def add_table(p_rows, p_columns, p_index, p_batch_requests):
    batch = {
                'insertTable': {
                    'rows': p_rows,
                    'columns': p_columns,
                    'location': {
                        'index': p_index,
                    }
                }
            },

    p_batch_requests.append(batch)
    return p_batch_requests


def add_bold_normal(index_start, index_end, p_batch_requests):
    batch = {
        'updateTextStyle': {
            'range': {
                'startIndex': index_start,
                'endIndex': index_end
            },
            'textStyle': {
                'bold': True,
                'fontSize': {"magnitude": 12, "unit": "pt"},
            },
            'fields': '*'
        }
    }
    p_batch_requests.append(batch)
    return p_batch_requests


def add_italic_normal(index_start, index_end, p_batch_requests):
    batch = {
        'updateTextStyle': {
            'range': {
                'startIndex': index_start,
                'endIndex': index_end
            },
            'textStyle': {
                'italic': True,
                'fontSize': {"magnitude": 11, "unit": "pt"},
            },
            'fields': 'italic'
        }
    }
    p_batch_requests.append(batch)
    return p_batch_requests


def add_link(p_link, index_start, index_end, p_batch_requests):
    batch = {
                'updateTextStyle': {
                    'range': {
                        'startIndex': index_start,
                        'endIndex': index_end
                    },
                    'textStyle': {
                        'link': {
                            'url': p_link
                        }
                    },
                    'fields': 'link'
                }
            },
    p_batch_requests.append(batch)
    return p_batch_requests


def add_title(index_start, index_end, p_batch_requests):
    batch = {
        'updateTextStyle': {
            'range': {
                'startIndex': index_start,
                'endIndex': index_end
            },
            'textStyle': {
                'bold': True,
                'fontSize': {"magnitude": 16, "unit": "pt"},
            },
            'fields': '*'
        }
    }
    p_batch_requests.append(batch)
    return p_batch_requests


def align_center(index_start, index_end, p_batch_requests):
    p_batch = {
                  "updateParagraphStyle": {
                      "range": {
                          "startIndex": index_start,
                          "endIndex": index_end
                      },
                      "paragraphStyle": {
                          "alignment": "CENTER"
                      },
                      "fields": "alignment"
                  }
              }
    p_batch_requests.append(p_batch)
    return p_batch_requests


def align_start(index_start, index_end, p_batch_requests):
    p_batch = {
        "updateParagraphStyle": {
            "range": {
                "startIndex": index_start,
                "endIndex": index_end
            },
            "paragraphStyle": {
                "alignment": "START"
            },
            "fields": "alignment"
        }
    }
    p_batch_requests.append(p_batch)
    return p_batch_requests


def delete_entire_document(p_service, document_id, p_doc_content):
    import re

    matches = re.findall(r"'endIndex':\s([0-9]+)", str(p_doc_content), re.X | re.M | re.S)
    if matches:
        last_number = matches[-1]
    last_number = int(last_number)
    last_number -= 1
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


def get_assignment_link(assignments_dict, assignment_name, p_courseworks, p_materials):
    link = ''
    if assignment_name in assignments_dict:
        assignment_name = assignments_dict[assignment_name]
    # print('starting ' + str(assignment_name))
    # print("materials "  )
    # print(p_materials)
    for coursework in p_courseworks:
        title = coursework['title']
        smiley_assignment_name = assignment_name + ' :-)'
        # print("assignment name '" + assignment_name + "' title '" + title)
        if assignment_name == title or smiley_assignment_name == title:
            link = coursework['alternateLink']
            return link
    for material in p_materials:
        # print("assignmenit name "  + str(assignment_name))
        title = material['title']
#        print("assignmenit name '"  + str(assignment_name) + "' title '" + str(title) + "'")

        smiley_assignment_name = assignment_name + ' :-)'
        if assignment_name == title or smiley_assignment_name == title:
            link = material['alternateLink']
            return link
    return link


def get_final_index(p_doc_content):
    import re
    matches = re.findall(r"'endIndex':\s([0-9]+)", str(p_doc_content), re.X | re.M | re.S)
    if matches:
        last_number = matches[-1]
    last_number = int(last_number)
    last_number -= 1
    return last_number


def insert_page_break(p_location, p_batch_requests):
    batch = {
        'insertPageBreak': {
            'location': {
                'index': p_location,
            }
        }
    }
    p_batch_requests.append(batch)
    return [p_location + 1, p_batch_requests]


def get_text(p_service, document_id):
    document = p_service.documents().get(documentId=document_id).execute()
    doc_content = document.get('body').get('content')
    return doc_content


def iter4obj_2_list(p_obj):
    """
    Args:
        p_obj: an iter4 object

    Returns:
        A list of lists (converts iter4 ojbects to list)
    """
    return_list = []
    for day in p_obj:
        temp_list = []
        temp_list.append(day[0])
        temp_list.append(day[1])
        temp_list.append(day[2])
        return_list.append(temp_list)
    return return_list