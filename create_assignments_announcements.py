# it1cs1it2it3
import re
import datetime

from generate_sheets_credential import generate_sheets_credential
from generate_classroom_credential import generate_classroom_credential

from helper_functions.get_google_drive_id import get_google_drive_id
from helper_functions.date_to_ISO8601 import date_to_iso8601
from helper_functions.get_all_sheets import get_all_sheets
from helper_functions.read_course_id import read_course_id
from helper_functions.read_course_daily_data_all import read_course_daily_data_all
from helper_functions.is_in_past import is_in_past
from helper_functions.read_day_info import read_day_info
from helper_functions.read_lesson_plan import read_lesson_plan
from helper_functions.post_announcement import post_announcement
from helper_functions.post_assignment import post_assignment
from helper_functions.update_sheet_with_id import update_sheet_with_id

SPREADSHEET_ID = '1xkcNN1OFmscODqz3zbDUqRbkHAxIuIyx-FtMfXgqczA'


# Get sheet service credential and service_classroom credential
service_sheets = generate_sheets_credential()
service_classroom = generate_classroom_credential()

# Get name of all sheets, put in sheet_list
sheet_list = get_all_sheets(SPREADSHEET_ID, service_sheets)

# Loop over all sheets of classes
for sheet in sheet_list:

    # Skip Calendar and Courses sheets,
    if sheet == 'Calendar' or sheet == 'Courses' or sheet == 'Sheet11':
        continue

    # Get course ID
    course_id = read_course_id(SPREADSHEET_ID, sheet, service_sheets)
    print("In create assignments/announcements, currently doing course with this ID: {}".format(course_id))

    course_results = service_classroom.courses().get(id=course_id).execute()
    course_section = course_results['section']

    # Read entire sheet for this particular course (every day's assignment)
    values = read_course_daily_data_all(SPREADSHEET_ID, sheet, service_sheets)
    print("In create assignments/announcements, read in all data for course {}.  Data is this: {}"
          .format(sheet, values))

    # Iterate over sheets rows and write/edit classroom as necessary
    print("In create assignments/announcements.  Starting to iterating daily assignments/announcements " + sheet)
    for i, row in enumerate(values, 1):
        if i > 180:
            break
        # read the row
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
        elif len(row) == 6 and not re.search(r'\d', row[5]):  # Crash out if ID's do not contain numbers
            raise Exception("This day: {} has row length of 6, but no numbers in the ID column (F).\n "
                            " Are there spaces or something goofy going on in ID column?  \nTry deleting"
                            " the entire cell and try again".format(day_info['date']))
        elif len(row) == 5:  # Do new rows (i.e. not previously posted, no IDs)
            print("Posting a new lesson that hasn't been posted before")
            link_spreadsheet_id = get_google_drive_id(day_info['link'])
            assignments_announcements = read_lesson_plan(link_spreadsheet_id, service_sheets)
            all_ids = ''
            single_id = ''
            assignment_counter = 0
            for assignment_announcement in assignments_announcements:
                if assignment_announcement['assignment_or_announcement'] == 'announcement':
                    single_id = post_announcement(i, assignment_announcement['text'], day_info['date'], course_id,
                                                  service_classroom)

                    # print("announcement for day: {}. text is: {}, ID is {}".format(i, assignment_announcement['text'],
                    #                                                               single_id))
                if assignment_announcement['assignment_or_announcement'] == 'assignment':
                    single_id = post_assignment(assignment_announcement['topic'], assignment_announcement['title'],
                                                assignment_announcement['days_to_complete'],
                                                assignment_announcement['text'], assignment_announcement['attachments'],
                                                day_info['date'], assignment_counter, course_section,
                                                course_id, SPREADSHEET_ID, service_sheets, service_classroom)
                    assignment_counter += 1
                all_ids += single_id + ','
            update_sheet_with_id(SPREADSHEET_ID, all_ids, i, service_sheets, sheet)
        elif len(row) == 6:  # previously found assignment!
            print("Found previously posted announcements/assignments")

            # basic concept: do everything again.
            # For announcements, if day to be scheduled is different, delete the old and post the new.
            #                    if day to be scheduled is th esame, do nothing.
            # For assignments, if day to be scheduled is different, change announcement.
            #                  If announcement or assignment doesn't exist, then it's already posted; do nothing.

            announcement_data_to_repost = []
            announcement_ids_to_delete = []

            # Get link of sheet and read in lesson
            link_spreadsheet_id = get_google_drive_id(day_info['link'])
            assignments_announcements = read_lesson_plan(link_spreadsheet_id, service_sheets)

            # prepare just i case
            all_ids = ''
            single_id = ''
            assignment_counter = 0
            is_assignment = False
            is_announcement = False
            # loop over all posted assignments
            posted_ids = day_info['ids'].split(',')
            for posted_id in posted_ids:
                if posted_id == ' ' or posted_id == '':   # skip single space or blankones
                    continue
                else:
                    announcement = {}
                    print("Encountered this old assignment/announcement {}.  Checking it out.".format(posted_id))
                    try:
                        announcement = service_classroom.courses().announcements().get(courseId=course_id,
                                                                                       id=posted_id).execute()
                        is_announcement = True
                        print("found that old entry {} is an announcement!".format(posted_id))
                    except:  # do assignments here
                        print("Found that old entry is an assignment")

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
                            print("Announcement with this ID {} hasn't been PUBLISHED yet.  "
                                  "Checking to see if it should be moved to new scheduled date.".format(posted_id))

                            # For announcement, check to see if original posted day is the same as current posted day
                            announcement_date = re.sub(r'T.+$', '', announcement['scheduledTime'], re.X | re.M | re.S)
                            numbers = day_info['date'].split('/')
                            today_date = date_to_iso8601(numbers[0], numbers[1], numbers[2], 0)
                            today_date = re.sub(r'T.+$', '', today_date, re.X | re.M | re.S)

                            if announcement_date == today_date:
                                print("announcement {} in Classroom is on same day it is currently listed in sheet {}  "
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
                                print(new_announcement_data['text'])
                                announcement_ids_to_delete.append(posted_id)
                                announcement_data_to_repost.append(new_announcement_data)
                        elif announcement['state'] == 'DELETED':
                            raise Exception("The ID {} that was read in for this assignment has been deleted in Google "
                                            "classroom.\n  Something is wrong, but not sure what.  Try erasing the ID\n"
                                            "for this day and reposting the lesson.\n".format(posted_id))
            if len(announcement_ids_to_delete) > 0:
                for announcement_id in announcement_ids_to_delete:
                    delete_result = service_classroom.courses().announcements().delete(courseId=course_id,
                                                                                       id=announcement_id).execute()
                    print("Deleted old announcement ID {}".format(announcement_id))
                for data in announcement_data_to_repost:
                    # p_day, p_text, p_date, p_course_id, p_service
                    single_id = post_announcement(day_info['day'], data['text'], data['date'],
                                                  course_id, service_classroom)
                    all_ids += single_id + ','
                update_sheet_with_id(SPREADSHEET_ID, all_ids, day_info['day'], service_sheets, sheet)
            raise Exception("no moas")

            # Get day of assignment to be posted and prospective new_scheduled_time
            month, dom, year = row[1].split('/')
            new_scheduled_time = date_to_iso8601(month, dom, year)

            # skip
            now = datetime.datetime.now()

            assignment_date_string = month + '/' + dom + '/' + year
            print(assignment_date_string)
            item_date = datetime.datetime(int(year), int(month), int(dom))
            print(item_date)
            if item_date < now:
                print('skip this')
                continue

            # get IDs of assignments posted
            print("This  spreadsheet with assignments and announcements that has been previously posted")
            id_string = row[5]
            ids = id_string.split(',')
            ids.pop()
            print(ids)



            counter = 0

            # Get day of assignment to be posted and prospective new_scheduled_time
            month, dom, year = row[1].split('/')
            new_scheduled_time = date_to_iso8601(month, dom, year)
            print('working on this day:  {}-{}-{}'.format(month, dom, year))

            # get day
            day = row[0]

            # Loop through previously posted assignment IDs
            for j, p_id in enumerate(ids, 0):
                print('This announcement/assignment, trying now:  ' + str(p_id) + ' ' + str(j))
                try:
                    assignment = service_classroom.courses().courseWork().get(courseId=course_id,
                                                                              id=p_id).execute()
                    value = assignment.get('scheduledTime', [])
                    # if not value:
                    #     continue  # give up for now
                    #     raise ValueError("broken values for dates.  "
                    #                      "Check your dates, should be 9-5-2018 (or something similar)")
                    if new_scheduled_time == value:
                        print("found old assignment same day no change")
                    else:
                        print("found old assignment, different day, changing changing assignment day")
                        days_to_complete = columns[j][2]

                        post_date = str(month) + '-' + str(dom) + '-' + str(year)
                        new_due_date_obj = get_due_date(post_date, days_to_complete, SPREADSHEET_ID, service_sheets)

                        print("days to complete" + str(days_to_complete))
                        print('scheduled time' + str(value))
                        # algorithm - move scheduled day
                        # recalculate due date
                        # patch
                        new_scheduled_time = date_to_iso8601(month, dom, year)
                        update = {'dueDate': {"year": new_due_date_obj.year,
                                              "month": new_due_date_obj.month,
                                              "day": new_due_date_obj.day,
                                              },
                                  'dueTime': {"hours": 12,
                                              "minutes": 6,
                                              "seconds": 0
                                              },
                                  'scheduledTime': new_scheduled_time,
                                  }
                        print(update)
                        assignment = service_classroom.courses().courseWork().patch(courseId=course_id,
                                                                                    id=p_id,
                                                                                    updateMask='dueDate,'
                                                                                               'dueTime,'
                                                                                               'scheduledTime',
                                                                                    body=update).execute()
                except:
                    print("yes")
