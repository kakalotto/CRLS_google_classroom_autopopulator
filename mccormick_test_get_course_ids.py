from generate_classroom_credential import generate_classroom_credential

service_classroom = generate_classroom_credential()
courses = service_classroom.courses().list().execute()
courses = courses['courses']
for course in courses:
    print("course name: {}   course id: {}".format(course['name'], course['id']))