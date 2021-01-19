def requests_header(p_header_text):
    p_requests = [
        {
            'insertText': {
                'location': {
                    'index': 1,
                },
                'text': p_header_text
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
            "updateParagraphStyle": {
                "range": {
                    "startIndex": 47,
                    "endIndex": 489
                },
                "paragraphStyle": {
                    "alignment": "START"
                },
                "fields": "alignment"
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
    return p_requests


def requests_links(p_zoom_link, p_aspen_link, p_classroom_link, p_assigned_link, p_missing_link):
    requests = [
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
                        'url': p_zoom_link
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
                        'url': p_classroom_link
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
                        'url': p_assigned_link
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
                        'url': p_missing_link
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
                        'url': p_aspen_link
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

    ]
    return requests