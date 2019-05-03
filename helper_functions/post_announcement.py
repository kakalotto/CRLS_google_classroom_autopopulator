def post_announcement(p_spreadsheet_id, p_service):
    print("blah)")
    announcement = {
                    'text': '\U0001D403\U0001D400\U0001D418 ' + day + '/180 \n' + text,
                    'state': 'DRAFT',
                    'scheduledTime': year + '-' + month + '-' + dom + 'T08:00:00-04:00',
                    'materials': [],
                }
                print(announcement)
                # Look for links or gdrive files
                announcement['materials'] = attachments
                announcement = service_classroom.courses().announcements().create(courseId=course_id,
                                                                                  body=announcement).execute()
                # Update id_string with assignment ID
                announcement_id = announcement.get('id')