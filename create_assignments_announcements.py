# it1cs1it2it3
import re
import datetime

from generate_sheets_credential import generate_sheets_credential
from generate_classroom_credential import generate_classroom_credential

from helper_functions.get_google_drive_id import get_google_drive_id
from helper_functions.unicode_text import unicode_text
from helper_functions.date_to_ISO8601 import date_to_iso8601
from helper_functions.get_all_sheets import get_all_sheets
from helper_functions.get_due_time import get_due_time
from helper_functions.read_course_id import read_course_id
from helper_functions.read_course_daily_data_all import read_course_daily_data_all
from helper_functions.is_in_past import is_in_past
from helper_functions.read_day_info import read_day_info
from helper_functions.read_lesson_plan import read_lesson_plan


SPREADSHEET_ID = '1xkcNN1OFmscODqz3zbDUqRbkHAxIuIyx-FtMfXgqczA'


def get_attachments(p_column):
    print("entering {}".format(p_column))
    p_attachments = []
    p_counter = 4
    p_share_mode = ''
    while p_counter < len(p_column):
        print(" {}  {}".format(p_counter, len(p_column)))
        print(p_counter)
        if p_counter <= len(p_column) and p_column[p_counter]:
            p_link = p_column[p_counter]
            if len(p_column) >= p_counter + 2:
                # only assignments have share mode for links
                p_share_mode = p_column[p_counter + 1]
            p_google_drive_match = re.search('.google', p_link)
            if p_google_drive_match:
                print("matches google drive file")
                p_link = get_google_drive_id(p_link)
                if p_share_mode:
                    p_material = {
                        'driveFile': {
                            'driveFile': {'id': p_link},
                            'shareMode': p_share_mode,
                        }
                    }
                else:
                    p_material = {
                        'driveFile': {
                            'driveFile': {'id': p_link},
                        }
                    }

            else:
                # match regular p_link
                p_material = {
                    'p_link': {'url': p_link}
                }
            p_attachments.append(p_material)
            p_counter += 2
        elif not p_column[p_counter]:
            p_counter = 9999
            print("done")
    return p_attachments

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

    # Read entire sheet for this particular course (every day's assignment)
    values = read_course_daily_data_all(SPREADSHEET_ID, sheet, service_sheets)
    print("In create assignments/announcements, read in all data for course {}.  Data is this: {}"
          .format(sheet, values))

    # Iterate over sheets rows and write/edit classroom as necessary
    print("In create assignments/announcements.  Starting to iterating daily assignments/announcements " + sheet)
    for i, row in enumerate(values, 1):

        # read the row
        daily_info = read_day_info(row)

        print(daily_info)

        # Skip days in the past, days with no data, days with no rows
        if is_in_past(daily_info['date']):  # In the past
            print("This day: {} is in the past, skipping ".format(daily_info['date']))
            continue
        elif not row:  # Empty row
            print("No row here, skipping")
            continue
        elif len(row) == 3:  # no announcements or anything
            print("This day: {} has no data yet, skipping".format(daily_info['date']))
            continue
        # Crash out if ID's has spaces in it but no ID
        elif len(row) == 6 and not re.search(r'\d', row[5]):
            print("shoulD BE HERE")
            raise Exception("This day: {} has row length of 6, but no numbers in the ID column (F).\n "
                            " Are there spaces or something goofy going on in ID column?  \nTry deleting"
                            " the entire cell and try again".format(daily_info['date']))
        # Do rows with newly posted data
        elif len(row) == 5:  #
            print("Posting a new assignment")
            link_spreadsheet_id = get_google_drive_id(daily_info['link'])
            print(link_spreadsheet_id)
            lesson_columns = read_lesson_plan(link_spreadsheet_id, service_sheets)
            print(lesson_columns)
        #    raise Exception("stop here")

            id_string = ''

            for column in lesson_columns:
                print(column)


            # if columns:
            #     print('woooo' + str(len(columns)))
            #     while counter < len(columns):
            #         text = columns[counter][3]
            #         text = unicode_text(text)
            #         attachments = get_attachments(columns[counter])
            #         if columns[counter][0] == 'announcement':
            #             print("announcement incoming")
            #             text = columns[counter][3]
            #             text = unicode_text(text)
            #             announcement = {
            #                 'text': '\U0001D403\U0001D400\U0001D418 ' + day + '/180 \n' + text,
            #                 'state': 'DRAFT',
            #                 'scheduledTime': year + '-' + month + '-' + dom + 'T08:00:00-04:00',
            #                 'materials': [],
            #             }
            #             print(announcement)
            #             # Look for links or gdrive files
            #             announcement['materials'] = attachments
            #             announcement = service_classroom.courses().announcements().create(courseId=course_id,
            #                                                                               body=announcement).execute()
            #             # Update id_string with assignment ID
            #             announcement_id = announcement.get('id')
            #             id_string += announcement_id + ','
            #             #    update_cell_with_id(SPREADSHEET_ID, announcement_id, i, service_sheets, sheet)
            #         else:
            #             print("assignment incoming")
            #             print(row)
            #             title = columns[counter][1]
            #             title = unicode_text(title)
            #
            #             # calculate the due date
            #             post_date = str(month) + '-' + str(dom) + '-' + str(year)
            #             days_to_complete = columns[counter][2]
            #             print("days to complete" + str(days_to_complete))
            #             due_date_obj = get_due_date(post_date, days_to_complete, SPREADSHEET_ID, service_sheets)
            #             print("{}".format(due_date_obj))
            #             new_scheduled_time = date_to_iso8601(month, dom, year)
            #             hours, minutes = get_due_time(days_to_complete)
            #             print("hours and minutes" + str(hours) + " " + str(minutes))
            #             description = text
            #             assignment = {
            #                 'title': title,
            #                 'description': description,
            #                 'materials': [],
            #                 'dueDate': {"year": due_date_obj.year,
            #                             "month": due_date_obj.month,
            #                             "day": due_date_obj.day,
            #                             },
            #                 'dueTime': {"hours": hours,
            #                             "minutes": minutes,
            #                             "seconds": 0},
            #                 'scheduledTime': new_scheduled_time,
            #                 'workType': 'ASSIGNMENT',
            #                 'state': 'DRAFT',
            #             }
            #             print(attachments)
            #             assignment['materials'] = attachments
            #
            #             print(assignment)
            #             assignment = service_classroom.courses().courseWork().create(courseId=course_id,
            #                                                                          body=assignment).execute()
            #             print('Assignment created with ID {0}'.format(assignment.get('id')))
            #             assignment_id = assignment.get('id')
            #             id_string += assignment_id + ','
            #             #   update_cell_with_id(SPREADSHEET_ID, assignment_id, i, service_sheets, sheet)
            #         counter += 1
            #         print('counter is ' + str(counter))
            #     print('id string is ' + id_string)
            #     update_cell_with_id(SPREADSHEET_ID, id_string, i, service_sheets, sheet)
            #
            # print('end of loop')

        elif len(row) == 6:  # previously found assignment!

            # Get day of assignment to be posted and prospective new_scheduled_time
            month, dom, year = row[1].split('/')
            new_scheduled_time = date_to_iso8601(month, dom, year)

            # skip
            now = datetime.datetime.now()
            print("now")
            print(now)

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

            # Get link of sheet
            link = row[4]
            link_spreadsheet_id = get_google_drive_id(link)
            print(link_spreadsheet_id)

            # Read from daily sheet
            RANGE_NAME = 'Sheet1!B2:BZ19'
            print("Sheet name is this:" + str(sheet))
            result = service_sheets.spreadsheets().values().get(majorDimension='COLUMNS',
                                                                spreadsheetId=link_spreadsheet_id,
                                                                range=RANGE_NAME, ).execute()
            columns = result.get('values', [])
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
                    if not value:
                        continue  # give up for now
                        raise ValueError("broken values for dates.  "
                                         "Check your dates, should be 9-5-2018 (or something similar)")
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
                    print("old announcement found")
                    announcement = service_classroom.courses().announcements().get(courseId=course_id,
                                                                                   id=p_id).execute()
                    print("yes made it past assignment")
                    value = announcement.get('scheduledTime', [])
                    if not value:
                        continue # give up for now
                        raise ValueError("broken values fot dates. "
                                         "Check your dates, should be 9-5-2018 (or something similar)")
                    print(value)
                    if new_scheduled_time == value:
                        announcement_text = announcement.get('text', [])
                        print(announcement_text)
                        print("announcement same day no change")
                    else:
                        text = announcement.get('text', [])
                        # Check to see if day change.  If so, need to re-post because Google classroom API not letting
                        #  me patch the text
                        same_day = re.search(day + '/180', text)
                    #    print('day is {} text is {}'.format(day, text))
                        if same_day is None:
                            print("yes")
                            print("reposting announcement for day change")

                            # Generate the new announcement from the old
                            text = re.sub('[0-9]+\/180', day + '/180', text)
                            materials = announcement.get('materials', [])
                            scheduledTime = announcement.get('scheduledTime', [])
                            announcement = {
                                'text': text,
                                'state': 'DRAFT',
                                'scheduledTime': new_scheduled_time,
                                'materials': materials,
                            }
                            print(announcement)

                            # Post the new announcement generated from old and get ID, append to new string
                            announcement = service_classroom.courses().announcements().create(courseId=course_id,
                                                                                              body=announcement).execute()
                            announcement_id = announcement.get('id')
                            new_id_string = re.sub(p_id, announcement_id, id_string)
                            print("new id string is " + str(new_id_string))
                            print("new ID is " + announcement_id)
                            # update cell with ID string
                            update_cell_with_id(SPREADSHEET_ID, new_id_string, i, service_sheets, sheet)

                            # delete the old announcement
                            clean_announcement = service_classroom.courses().announcements().delete(courseId=course_id,
                                                                                                    id=p_id).execute()

                        else:
                            # No need to change, just change scheduled time
                            print("changing announcement day")
                            update = {'scheduledTime': new_scheduled_time,
                                      }
                            announcement = service_classroom.courses().announcements().patch(courseId=course_id,
                                                                                             id=p_id,
                                                                                             updateMask='scheduledTime',
                                                                                             body=update).execute()
                print("finished going over old announcements/assignments")
                print(value)

