# Inputs:
# Output: assignment ID (int)

def post_materials(p_topic, p_title, p_text, p_attachments, p_date, p_offset,
                   p_course_id, p_service_classroom,):

    import googleapiclient

    from helper_functions.date_to_ISO8601 import date_to_iso8601
    from helper_functions.get_topic_ids import get_topic_ids

    # Misc. data formatting
    days = p_date.split('/')
    year = days[2]
    month = days[0]
    dom = days[1]

    # get topic IDs
    topic_dict = get_topic_ids(p_course_id, p_service_classroom)
    # get scheduled time.  Stagger entries so not all at once.
    new_scheduled_time = date_to_iso8601(month, dom, year, p_offset)

    if p_topic not in topic_dict.keys():
        raise Exception(f"For assignments {p_title}, the topic you want to post this under: {p_topic}, "
                        f"is not in the list of topics for the class.\n"
                        f"Please add this topic into the class, or else change the topic of the assignment.\n\n"
                        f"If you think the topic is actually there, maybe you put a space in front of it.\n"
                        f"In the courses tab, the topics are separated by commas, no spaces in between."
                        )
    p_material = {
        'title': p_title,
        'description': p_text,
        'materials': p_attachments,
        'topicId': topic_dict[p_topic],
        'scheduledTime': new_scheduled_time,
        'state': 'DRAFT',
    }
    print(f"In post_materials, attempting to post this material: {p_material['title']}")
    try:
        material_obj = p_service_classroom.courses().courseWorkMaterials().create(courseId=p_course_id,
                                                                                  body=p_material).execute()
        material_id = material_obj.get('id')
    except googleapiclient.errors.HttpError as error:
        raise Exception(f"Error: {error}\n"
                        f"File: {p_material['materials']}\n"
                        f"@AttachmentNotVisible The item referenced by an attachment was not found or not visible to the user.\n"
                        f"   Check share permissions on file be sure it's shared to token owner (Google slide or doc)\n"
                        f"   Check that you updated cell B1 with new courseID after creating the course\n"
                        f"Request contains an invalid argument' - is the topic you want for this assignment one that "
                        f"exists in this class within Google classroom?\n"
                        f"Alternatively, if there is a message 'materials: Duplicate materials are not allowed', you"
                        f"probably have two of the same link on your lesson plan.\n"
                        f"Alternatively, you posted a material with student copy")
    return material_id


# from generate_classroom_credential import generate_classroom_credential
#
# service_classroom = generate_classroom_credential()
# offset = 1
#
#def post_materials(p_topic, p_title, p_text, p_attachments, p_date, p_offset,
#                   p_course_id, p_service_classroom,):
#abc = post_materials('Administration', 'aaatest material', 'Test text', [], '1/18/2021', offset,
#                       '233686385807', service_classroom)

#course_id = 36500789911  # test_APCSP_Computer_Principles
#abc = post_assignment(1, 'MCAS GOOD LUCK', 5/28/2019', course_id, service_classroom)
#print(abc)
#material = service_classroom.courses().courseWorkMaterials().list(courseId=233686385807).execute()
#print(material)
#body = {'title': 'baaalahblah',
#         'description': "yes",
#         'topicId': '233687113769',
#        'scheduledTime': '2021-01-19'
#         }

#material = service_classroom.courses().courseWorkMaterials().create(courseId='233686385807', body=body).execute()
#
