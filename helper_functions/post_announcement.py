def post_announcement(p_day, p_text, p_date, p_course_id, p_service):

    # Misc. data formatting
    days = p_date.split('/')
    year = days[2]
    month = days[0]
    dom = days[1]
    p_day = str(p_day)

    # Create announcement dictionary
    announcement = {
        'text': '\U0001D403\U0001D400\U0001D418 ' + p_day + '/180 \n' + p_text,
        'state': 'DRAFT',
        'scheduledTime': year + '-' + month + '-' + dom + 'T12:00:00Z',
        'materials': [],
    }

    # Look for links or gdrive files  COMMENT OUT FOR NOW
#    announcement['materials'] = attachments

    # Add announcement to Google classroom
    announcement = p_service.courses().announcements().create(courseId=p_course_id, body=announcement).execute()

    # get announcement ID and return it
    announcement_id = announcement.get('id')
    return announcement_id


# from generate_classroom_credential import generate_classroom_credential
# course_id = 36500789911  # test_APCSP_Computer_Principles
# service_classroom = generate_classroom_credential()
# abc = post_announcement(1, 'MCAS GOOD LUCK', '5/28/2019', course_id, service_classroom)
# print(abc)
