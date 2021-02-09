def create_assignments_announcements(spreadsheet_id):

    import re

    import googleapiclient

    from generate_sheets_credential import generate_sheets_credential
    from generate_classroom_credential import generate_classroom_credential

    from helper_functions.get_google_drive_id import get_google_drive_id
    from helper_functions.get_all_sheets import get_all_sheets
    from helper_functions.read_course_id import read_course_id
    from helper_functions.read_course_daily_data_all import read_course_daily_data_all
    from helper_functions.is_in_past import is_in_past
    from helper_functions.read_day_info import read_day_info
    from helper_functions.read_lesson_plan import read_lesson_plan
    from helper_functions.post_announcement import post_announcement
    from helper_functions.post_assignment import post_assignment
    from helper_functions.post_materials import post_materials
    from helper_functions.update_sheet_with_id import update_sheet_with_id
    from helper_functions.is_work_date_current_date import is_work_date_current_date
    from helper_functions.post_assignment_reschedule import post_assignment_reschedule


    # Get sheet service credential and service_classroom credential
    service_sheets = generate_sheets_credential()
    service_classroom = generate_classroom_credential()

    # Get name of all sheets, put in sheet_list
    sheet_list = get_all_sheets(spreadsheet_id, service_sheets)

    # Loop over all sheets of classes
    for sheet in sheet_list:

        # Skip Calendar and Courses sheets,
        if sheet == 'Calendar' or sheet == 'Courses' or sheet == 'Sheet11':
            continue

        # Get course ID
        course_id = read_course_id(spreadsheet_id, sheet, service_sheets)
        print("In create assignments/announcements, currently doing course with this ID: {}".format(course_id))

        course_results = service_classroom.courses().get(id=course_id).execute()
        course_section = course_results['section']

        # Read entire sheet for this particular course (every day's assignment)
        values = read_course_daily_data_all(spreadsheet_id, sheet, service_sheets)
        print("In create assignments/announcements, read in all data for course {}.  Data is this: {}"
              .format(sheet, values))

        # Iterate over sheets rows and write/edit classroom as necessary
        print("In create assignments/announcements.  Starting to iterating daily assignments/announcements " + sheet)
        for i, row in enumerate(values, 1):
            print("day is this! " + str(i))
            if i < 0:  # how many to stkip
                continue
            # if i < 132:  # how many to stkip
            #     print("skipping")
            #     continue
            # if i > 134:  # how many to stkip
            #     print("skipping")
            #     continue



            # if i > 134:  # how many to stkip
            #     print("skipping")
            #     continue
            #read the row
            day_info = read_day_info(row)
            print(day_info)
            # Skip days in the past, days with no data, days with no rows
            if is_in_past(day_info['date']):  # In the past
                print("This day: {} is in the past, skipping ".format(day_info['date']))
                continue
            elif not row:  # Empty row
                print("No row here, skipping")
                continue
            elif len(row) == 3:  # no announcements or anything
                # print("This day: {} has no lesson, skipping".format(day_info['date']))
                continue
            elif len(row) == 8 and not row[4]:
                print("stuff with some notes but no assignment, continue")
                continue
            elif len(row) == 7 and not row[5]:
                print("do not move day, but no assignment. continue")
                continue
            elif len(row) == 6 and not re.search(r'(\d|)', row[5]):  # Crash out if ID's do not contain numbers
                raise Exception("This day: {} has row length of 6, but no numbers in the ID column (F).\n "
                                " Are there spaces or something goofy going on in ID column?  \nTry deleting"
                                " the entire cell and try again".format(day_info['date']))
            elif (len(row) == 5 or len(row) == 7 or len(row) == 8):
                if len(row) == 7 or len(row) == 8:
                    if row[5]:
                        continue
                # Do new rows (i.e. not previously posted, no IDs) row = 8 is comment but otherwise blank
                print("Posting a new lesson that hasn't been posted before")
                try:
                    link_spreadsheet_id = get_google_drive_id(day_info['link'])
                except:
                    raise Exception("Could not get spreadsheet ID of lesson plan in day {} \n"
                                    "Is there a lesson plan?  If you've marked this as 'do not move',"
                                    " program expects a link to a lesson in column E.\n"
                                    "Alternatively, is the link correct in column E?".format(row[0]))
                assignments_announcements = read_lesson_plan(link_spreadsheet_id, service_sheets)
                all_ids = ''
                single_id = ''
                assignment_counter = 0
                for assignment_announcement in assignments_announcements:
                    if assignment_announcement['assignment_or_announcement'] == 'announcement':
                        single_id = post_announcement(i, assignment_announcement['text'], day_info['date'], course_id,
                                                      service_classroom)
                    elif assignment_announcement['assignment_or_announcement'] == 'assignment':
                        single_id = post_assignment(assignment_announcement['topic'], assignment_announcement['title'],
                                                    assignment_announcement['days_to_complete'],
                                                    assignment_announcement['text'],
                                                    assignment_announcement['attachments'],
                                                    day_info['date'], assignment_counter, course_section,
                                                    course_id, spreadsheet_id, service_sheets, service_classroom,
                                                    assignment_announcement['points'],)
                        assignment_counter += 1
                    if assignment_announcement['assignment_or_announcement'] == 'materials':
                        single_id = post_materials(assignment_announcement['topic'], assignment_announcement['title'],
                                                   assignment_announcement['text'],
                                                   assignment_announcement['attachments'], day_info['date'],
                                                   assignment_counter, course_id, service_classroom)
                        assignment_counter += 1
                    all_ids += single_id + ','
                update_sheet_with_id(spreadsheet_id, all_ids, i, service_sheets, sheet)
            elif len(row) == 6 or len(row) == 8:  # previously found assignment!
                print("Found previously posted announcements/assignments")

                # basic concept: do everything again.
                # For announcements, if day to be scheduled is different, delete the old and post the new.
                #                    if day to be scheduled is th esame, do nothing.
                # For assignments, if day to be scheduled is different, change announcement.
                #                  If announcement or assignment doesn't exist, then it's already posted; do nothing.

                announcement_data_to_repost = []
                announcement_ids_to_delete = []
                assignment_data_to_reschedule = []
                materials_data_to_reschedule = []

                # Get link of sheet and read in lesson
                # link_spreadsheet_id = get_google_drive_id(day_info['link'])
                # assignments_announcements = read_lesson_plan(link_spreadsheet_id, service_sheets)

                # prepare just i case
                update_cell = False
                all_ids = ''
                single_id = ''
                # assignment_counter = 0
                # loop over all posted assignments
                posted_ids = day_info['ids'].split(',')
                posted_ids.pop()  # The last one is always an empty space somehow
                for posted_id in posted_ids:
                    is_assignment = False
                    is_announcement = False
                    if posted_id == ' ' or posted_id == '':   # skip single space or blankones
                        continue
                    else:
                        announcement = {}
                        assignment = {}
                        materials = {}
                        print("Encountered this old assignment/announcement/material {}.  "
                              "Checking it out.".format(posted_id))
                        try:
                            announcement = service_classroom.courses().announcements().get(courseId=course_id,
                                                                                           id=posted_id).execute()
                            is_announcement = True
                            print("Found that old entry {} is an announcement!".format(posted_id))
                        except googleapiclient.errors.HttpError:
                            pass
                        if is_announcement:
                            new_announcement_data = {}
                            if announcement['state'] == 'PUBLISHED':
                                print("Announcement with this ID {} has already been posted.\n"
                                      "This might be wrong, or you might've posted it early.\n"
                                      "In any case, skipping this ID.".format(posted_id))
                                continue
                            elif announcement['state'] == 'DRAFT':
                                # Some bug in classroom API where announcements can't have their text be changed.
                                # Since announcement needs to have text changed to reflect new day AND schedule new day
                                #  he code wipes old announcement and makes a new one (after all of the posted_ids are
                                # iterated through, in case there is a crash somewhere before we get to the end.
                                # print("Announcement with this ID {} hasn't been PUBLISHED yet.  "
                                #      "Checking to see if it should be moved to new scheduled date.".format(posted_id))
                                if is_work_date_current_date(announcement['scheduledTime'], day_info['date']):
                                    print("announcement {} in Classroom is on same day it is currently listed in sheet "
                                          "{}  "
                                          "No change.  On to the next announcement/assignment".format(posted_id, sheet))
                                    continue
                                else:  # posted day is on different day
                                    print("announcement {} in Classroom is on different day than is currently listed "
                                          "in sheet {}. "
                                          " Repost as new announcement and delete the old announcement.  "
                                          .format(posted_id, sheet))
                                    new_announcement_data['day'] = day_info['day']
                                    new_announcement_data['text'] = announcement['text']
                                    new_announcement_data['date'] = day_info['date']
                                    new_announcement_data['text'] = re.sub(r'\U0001D403\U0001D400\U0001D418 [0-9]+/180',
                                                                           '', announcement['text'],
                                                                           re.X | re.M | re.S)
                                    announcement_ids_to_delete.append(posted_id)
                                    announcement_data_to_repost.append(new_announcement_data)
                                    update_cell = True
                            elif announcement['state'] == 'DELETED':
                                raise Exception("The ID {} that was read in for this announcement has been deleted in "
                                                "Google classroom.\n  Something is wrong, but not sure what. \n "
                                                "Try erasing the ID for this day and reposting the lesson.\n"
                                                .format(posted_id))
                        else:  # not announcement, probably assignment or material
                            try:
                                assignment = service_classroom.courses().courseWork().get(courseId=course_id,
                                                                                          id=posted_id).execute()
                                print("zzzz ASSIGNMENT")
                                print(assignment)
                                is_assignment = True
                                print("Found that old entry {} is an assignment!".format(posted_id))
                            except googleapiclient.errors.HttpError:  # posted_id isn't there at all?
                                pass
                        if is_assignment:
                            new_assignment_data = {}
                            if assignment['state'] == 'PUBLISHED':
                                print("Announcement with this ID {} has already been posted.\n"
                                      "This might be wrong, or you might've posted it early.\n"
                                      "In any case, skipping this ID.".format(posted_id))
                                continue
                            elif assignment['state'] == 'DRAFT':
                                # print("Assignment with this ID {} hasn't been PUBLISHED yet.  "
                                #      "Checking to see if it should be moved to new scheduled date.".format(posted_id))
                                if is_work_date_current_date(assignment['scheduledTime'], day_info['date']):
                                    print("assignment {} in Classroom is on same day it is currently "
                                          "listed in sheet {}  "
                                          "No change.  On to the next announcement/assignment".format(posted_id, sheet))
                                    continue
                                else:  # posted day is on different day
                                    print("assignment {} in Classroom is on different day than is currently listed "
                                          "in sheet {}. "
                                          " Reschedule assignment  "
                                          .format(posted_id, sheet))
                                    new_assignment_data['assignment'] = assignment
                                    new_assignment_data['date'] = day_info['date']
                                    new_assignment_data['id'] = posted_id
                                    # print("new assignment data")
                                    # print(new_assignment_data)
                                    # print("assignment data to rescheulde")
                                    # print(assignment_data_to_reschedule)
                                    assignment_data_to_reschedule.append(new_assignment_data)
                                    # print("in loop")
                                    # print(assignment_data_to_reschedule)
                                    update_cell = True
                            elif assignment['state'] == 'DELETED':
                                raise Exception(
                                    "The ID {} that was read in for this assignment has been deleted in Google "
                                    "classroom.\n  Something is wrong, but not sure what.\n  "
                                    "Try erasing the ID for this day and reposting the lesson.\n".format(posted_id))
                        else:
                            print("maybe a materials")
                            try:
                                materials = service_classroom.courses().courseWorkMaterials().get(courseId=course_id,
                                                                                                  id=posted_id).execute()
                                is_materials = True
                                print("Found that old entry {} is a material!".format(posted_id))

                            except googleapiclient.errors.HttpError:  # posted_id isn't there at all?
                                raise Exception("Previously posted assignment/announcement {} is neither "
                                                "annoucement nor"
                                                "assignment.  Did you copy+paste from somewhere else incorrectly?\n"
                                                "  Or else, did you delete it from Google classroom manually?\n"
                                                " Or else, did you restart and just forget to delete the old ID's\n"
                                                " Exiting.".format(posted_id))
                            if is_materials:
                                new_materials_data = {}
                                if materials['state'] == 'PUBLISHED':
                                    print("Material with this ID {} has already been posted.\n"
                                          "This might be wrong, or you might've posted it early.\n"
                                          "In any case, skipping this ID.".format(posted_id))
                                    continue
                                elif materials['state'] == 'DRAFT':
                                    # print("Assignment with this ID {} hasn't been PUBLISHED yet.  "
                                    #      "Checking to see if it should be moved to new scheduled date.".format(posted_id))
                                    if is_work_date_current_date(materials['scheduledTime'], day_info['date']):
                                        print("materials {} in Classroom is on same day it is currently "
                                              "listed in sheet {}  "
                                              "No change.  On to the next announcement/assignment".format(posted_id,
                                                                                                          sheet))
                                        continue
                                    else:  # posted day is on different day
                                        print("materials {} in Classroom is on different day than is currently listed "
                                              "in sheet {}. "
                                              " Reschedule assignment  "
                                              .format(posted_id, sheet))
                                        new_materials_data['assignment'] = assignment
                                        new_materials_data['date'] = day_info['date']
                                        new_materials_data['id'] = posted_id
                                        # print("new assignment data")
                                        # print(new_materials_data)
                                        # print("assignment data to rescheulde")
                                        # print(assignment_data_to_reschedule)
                                        materials_data_to_reschedule.append(new_materials_data)
                                        # print("in loop")
                                        # print(assignment_data_to_reschedule)
                                        update_cell = True
                                elif materials['state'] == 'DELETED':
                                    raise Exception(
                                        "The ID {} that was read in for this materials has been deleted in Google "
                                        "classroom.\n  Something is wrong, but not sure what.\n  "
                                        "Try erasing the ID for this day and reposting the lesson.\n".format(posted_id))

                announcement_data_to_repost = []
                announcement_ids_to_delete = []
                assignment_data_to_reschedule = []
                materials_data_to_reschedule = []

                # Get link of sheet and read in lesson
                # link_spreadsheet_id = get_google_drive_id(day_info['link'])
                # assignments_announcements = read_lesson_plan(link_spreadsheet_id, service_sheets)

                # prepare just i case
                update_cell = False
                all_ids = ''
                single_id = ''
                # assignment_counter = 0
                # loop over all posted assignments
                posted_ids = day_info['ids'].split(',')
                posted_ids.pop()  # The last one is always an empty space somehow
                for posted_id in posted_ids:
                    is_assignment = False
                    is_announcement = False
                    if posted_id == ' ' or posted_id == '':   # skip single space or blankones
                        continue
                    else:
                        announcement = {}
                        assignment = {}
                        materials = {}
                        print("Encountered this old assignment/announcement/material {}.  "
                              "Checking it out.".format(posted_id))
                        try:
                            announcement = service_classroom.courses().announcements().get(courseId=course_id,                                                                                           id=posted_id).execute()
                            is_announcement = True
                            print("Found that old entry {} is an announcement!".format(posted_id))
                        except googleapiclient.errors.HttpError:
                            pass
                        if is_announcement:
                            new_announcement_data = {}
                            if announcement['state'] == 'PUBLISHED':
                                print("Announcement with this ID {} has already been posted.\n"
                                      "This might be wrong, or you might've posted it early.\n"
                                      "In any case, skipping this ID.".format(posted_id))
                                continue
                            elif announcement['state'] == 'DRAFT':
                                # Some bug in classroom API where announcements can't have their text be changed.
                                # Since announcement needs to have text changed to reflect new day AND schedule new day
                                #  he code wipes old announcement and makes a new one (after all of the posted_ids are
                                # iterated through, in case there is a crash somewhere before we get to the end.
                                # print("Announcement with this ID {} hasn't been PUBLISHED yet.  "
                                #      "Checking to see if it should be moved to new scheduled date.".format(posted_id))
                                if is_work_date_current_date(announcement['scheduledTime'], day_info['date']):
                                    print("announcement {} in Classroom is on same day it is currently listed in sheet "
                                          "{}  "
                                          "No change.  On to the next announcement/assignment".format(posted_id, sheet))
                                    continue
                                else:  # posted day is on different day
                                    print("announcement {} in Classroom is on different day than is currently listed "
                                          "in sheet {}. "
                                          " Repost as new announcement and delete the old announcement.  "
                                          .format(posted_id, sheet))
                                    new_announcement_data['day'] = day_info['day']
                                    new_announcement_data['text'] = announcement['text']
                                    new_announcement_data['date'] = day_info['date']
                                    new_announcement_data['text'] = re.sub(r'\U0001D403\U0001D400\U0001D418 [0-9]+/180',
                                                                           '', announcement['text'],
                                                                           re.X | re.M | re.S)
                                    announcement_ids_to_delete.append(posted_id)
                                    announcement_data_to_repost.append(new_announcement_data)
                                    update_cell = True
                            elif announcement['state'] == 'DELETED':
                                raise Exception("The ID {} that was read in for this announcement has been deleted in "
                                                "Google classroom.\n  Something is wrong, but not sure what. \n "
                                                "Try erasing the ID for this day and reposting the lesson.\n"
                                                .format(posted_id))
                        else:  # not announcement, probably assignment
                            try:
                                assignment = service_classroom.courses().courseWork().get(courseId=course_id,
                                                                                          id=posted_id).execute()
                                is_assignment = True
                                print("Found that old entry {} is an assignment!".format(posted_id))
                            except googleapiclient.errors.HttpError:  # posted_id isn't there at all?
                                pass
                        if is_assignment:
                            new_assignment_data = {}
                            if assignment['state'] == 'PUBLISHED':
                                print("Announcement with this ID {} has already been posted.\n"
                                      "This might be wrong, or you might've posted it early.\n"
                                      "In any case, skipping this ID.".format(posted_id))
                                continue
                            elif assignment['state'] == 'DRAFT':
                                # print("Assignment with this ID {} hasn't been PUBLISHED yet.  "
                                #      "Checking to see if it should be moved to new scheduled date.".format(posted_id))
                                if is_work_date_current_date(assignment['scheduledTime'], day_info['date']):
                                    print("assignment {} in Classroom is on same day it is currently "
                                          "listed in sheet {}  "
                                          "No change.  On to the next announcement/assignment".format(posted_id, sheet))
                                    continue
                                else:  # posted day is on different day
                                    print("assignment {} in Classroom is on different day than is currently listed "
                                          "in sheet {}. "
                                          " Reschedule assignment  "
                                          .format(posted_id, sheet))
                                    new_assignment_data['assignment'] = assignment
                                    new_assignment_data['date'] = day_info['date']
                                    new_assignment_data['id'] = posted_id
                                    # print("new assignment data")
                                    # print(new_assignment_data)
                                    # print("assignment data to rescheulde")
                                    # print(assignment_data_to_reschedule)
                                    assignment_data_to_reschedule.append(new_assignment_data)
                                    # print("in loop")
                                    # print(assignment_data_to_reschedule)
                                    update_cell = True
                            elif assignment['state'] == 'DELETED':
                                raise Exception(
                                    "The ID {} that was read in for this assignment has been deleted in Google "
                                    "classroom.\n  Something is wrong, but not sure what.\n  "
                                    "Try erasing the ID for this day and reposting the lesson.\n".format(posted_id))
                        else:
                            try:
                                materials = service_classroom.courses().courseWorkMaterials().get(courseId=course_id,
                                                                                                  id=posted_id).execute()
                                is_materials = True
                                print("Found that old entry {} is a material!".format(posted_id))

                            except googleapiclient.errors.HttpError:  # posted_id isn't there at all?
                                raise Exception("Previously posted assignment/announcement {} is neither "
                                                "annoucement nor"
                                                "assignment.  Did you copy+paste from somewhere else incorrectly?\n"
                                                "  Or else, did you delete it from Google classroom manually?\n"
                                                " Or else, did you restart and just forget to delete the old ID's\n"
                                                " Exiting.".format(posted_id))
                            if is_materials:
                                new_materials_data = {}
                                if materials['state'] == 'PUBLISHED':
                                    print("Material with this ID {} has already been posted.\n"
                                          "This might be wrong, or you might've posted it early.\n"
                                          "In any case, skipping this ID.".format(posted_id))
                                    continue
                                elif materials['state'] == 'DRAFT':
                                    # print("Assignment with this ID {} hasn't been PUBLISHED yet.  "
                                    #      "Checking to see if it should be moved to new scheduled date.".format(posted_id))
                                    if is_work_date_current_date(materials['scheduledTime'], day_info['date']):
                                        print("materials {} in Classroom is on same day it is currently "
                                              "listed in sheet {}  "
                                              "No change.  On to the next announcement/assignment".format(posted_id,
                                                                                                          sheet))
                                        continue
                                    else:  # posted day is on different day
                                        print("materials {} in Classroom is on different day than is currently listed "
                                              "in sheet {}. "
                                              " Reschedule assignment  "
                                              .format(posted_id, sheet))
                                        new_materials_data['assignment'] = assignment
                                        new_materials_data['date'] = day_info['date']
                                        new_materials_data['id'] = posted_id
                                        # print("new assignment data")
                                        # print(new_materials_data)
                                        # print("assignment data to rescheulde")
                                        # print(assignment_data_to_reschedule)
                                        materials_data_to_reschedule.append(new_materials_data)
                                        # print("in loop")
                                        # print(assignment_data_to_reschedule)
                                        update_cell = True
                                elif materials['state'] == 'DELETED':
                                    raise Exception(
                                        "The ID {} that was read in for this materials has been deleted in Google "
                                        "classroom.\n  Something is wrong, but not sure what.\n  "
                                        "Try erasing the ID for this day and reposting the lesson.\n".format(posted_id))

                if update_cell:
                    for announcement_id in announcement_ids_to_delete:
                        delete_result = service_classroom.courses().announcements().delete(courseId=course_id,
                                                                                           id=announcement_id).execute()
                        print("Deleted old announcement ID {}".format(announcement_id))
                    for data in announcement_data_to_repost:
                        # p_day, p_text, p_date, p_course_id, p_service
                        single_id = post_announcement(day_info['day'], data['text'], data['date'],
                                                      course_id, service_classroom)
                        all_ids += single_id + ','
                    # print("assignment data to rescheulde")
                    # print(assignment_data_to_reschedule)
                    for assignment in assignment_data_to_reschedule:

                        single_id = post_assignment_reschedule(assignment['assignment'], assignment['date'], course_id,
                                                               assignment['id'], service_classroom,
                                                               spreadsheet_id, service_sheets)
                        # print(single_id)
                        all_ids += single_id + ','
                    update_sheet_with_id(spreadsheet_id, all_ids, day_info['day'], service_sheets, sheet)
                    print(all_ids)
                else:
                    print("No assignments on this day need to be moved.  No change to this day.")
        print("All done with this class! {} ".format(sheet))
