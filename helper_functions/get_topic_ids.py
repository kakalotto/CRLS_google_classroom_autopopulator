# Input: Google classroom service object
# Output: dictionary keys are topics (string), values are ids (integer)


def get_topic_ids(p_course_id, p_service):

    # Read entire sheet for this particular course
    results = p_service.courses().topics().list(courseId=p_course_id).execute()
    topics = results['topic']
    return_dict = {}
    for topic in topics:
        key = topic['name']
        value = topic['topicId']
        return_dict[key] = value
    return return_dict
#
#
# from generate_classroom_credential import generate_classroom_credential
# service_classroom = generate_classroom_credential()
# abc = get_topic_ids(36512536321, service_classroom)
# print(abc)
