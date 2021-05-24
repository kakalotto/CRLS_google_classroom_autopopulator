def create_google_calendar_entries(*, document_id='1KLMCq-Nvq-fCNnkCQ7mayIVOSS-HGupSTG_lPT8EPOI',
                           classroom_id='MTY0OTY1NDEyNjg3',
                           spreadsheet_id='1ZenTcQlCQhbYvBvPOVq8XIB2FQgseIGHH4gTBTcw-KY', sheet_id='APCSP_S1_P1',
                           header_text='AP CSP\n', course_id=164978040288,
                           course_contract_link='https://docs.google.com/document/d/'
                                                '1eR5rxgTZ0PXy_fYIFK2SS_Ro770IXxT9sM90vZr_OcU/edit',
                           zoom_links=None,
                           assignments_dictionary=None, fy=False):
    """
    This creates a calendar document with daily activities, items due and notes.  Named after Dr. Lam, who does
    the same thing
    :param document_id: Google ID of the doc ID to edit (string)
    :param classroom_id: Classroom ID of the classroom to get info from (string)
    :param spreadsheet_id: Google sheets ID of the google sheet daily planner doc (string)
    :param sheet_id: Sheet within the spreadsheet (string)
    :param header_text: String to put at the top of the doc (string)
    :param course_id: ID of the coursenumber to edit (string)
    :param course_contract_link: Link to the course contract (string)
    :param zoom_links: links to the zoom for the class (string)
    :param assignments_dictionary: Dictionary of assignments to shorten because of overlap or length (dict of strings)
    :param fy: Full year or not (Boolean)
    :return: none
    """
    from generate_calendar_credential import generate_calendar_credential
    import re
    import calendar
    import datetime
    # from copy import deepcopy
    from generate_docs_credential import generate_docs_credential
    from generate_sheets_credential import generate_sheets_credential
    from generate_ro_classroom_credential import generate_ro_classroom_credential
    from helper_functions.dr_lam_functions import add_table, delete_entire_document, get_text, \
        add_regular_text, add_bold_normal, add_italic_normal, add_link, get_assignment_link, iter4obj_2_list, \
        insert_page_break
    from helper_functions.dr_lam_requests import requests_header, requests_links
    from helper_functions.read_course_daily_data_all import read_course_daily_data_all
    from helper_functions.quarters import quarter_dates
    from helper_functions.read_in_holidays import read_in_holidays

    service_calendar = generate_calendar_credential()
