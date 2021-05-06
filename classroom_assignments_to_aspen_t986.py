from classroom_assignments_to_aspen import classroom_assignments_to_aspen
gc_classname  = 'IT3 2020-2021'
aspen_classname = 'T986-IP-001'
username = 'ewu'
password = 'Dimmy123$'
# username = ''
# password = ''
classroom_assignments_to_aspen(gc_classname, aspen_classname, content_knowledge_completion=False, ignore_ungraded=False,
                               username=username, password=password)



# content_knowledge_completion=False  # If true, we put assignments intotwo categories - content_knowledge
                                      #  and completion (caps count).
                                      #  Otherwise we will just pick the first category and put it in there.

# ignore_ungraded=False # if True, this will ignore assignments that are ungraded.  Default is that it will stop and make
                       # you put maximum point value for each assignment in Classroom