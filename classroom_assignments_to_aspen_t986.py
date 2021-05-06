from classroom_assignments_to_aspen import classroom_assignments_to_aspen
gc_classname  = 'IT3 2020-2021'
aspen_classname = 'T986-IP-001'
username = 'ewu'
password = 'Dimmy123$'
content_knowledge_completion_value = True
ignore_ungraded_value=False
# username = ''
# password = ''
classroom_assignments_to_aspen(gc_classname, aspen_classname,
                               content_knowledge_completion=content_knowledge_completion_value,
                               ignore_ungraded=ignore_ungraded_value,
                               username=username, password=password)



# content_knowledge_completion=False  # If true, we put assignments intotwo categories - content_knowledge
                                      #  and completion (caps count).
                                      #  Otherwise we will just pick the first category and put it in there.

# ignore_ungraded=False # if True, this will ignore assignments that are ungraded (points not set in Google classroom)
                        #  .  Default is that it will crash out and make
                        # you put maximum point value for each assignment in Classroom