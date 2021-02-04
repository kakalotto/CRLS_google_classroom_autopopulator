# Input: A column of data from a lesson plan, as a list.  See for example column 2 here:
#        https://docs.google.com/spreadsheets/d/1Onx-EMOHveOXSO3bR4K6rMB4ovKYzeVdvYh04EnoS58/edit#gid=0
#
# Example:
# ['assignment', 'AP_testing', 'Create task', '10',
# 'Included here:\n1. Create task  instructions (which is same as create task practice instructions)\n2.
#    Create task rubric, which you will be scored on\n3. A checklist to help you make sure you did everything (optional
#   etc...,
# 'EDIT',
# 'https://drive.google.com/open?id=1EZR2G7OUo-QQigCARYtPT7S2lnsX8SbI_f4QGahPK3Y',
# 'STUDENT_COPY',
# 'https://drive.google.com/open?id=1iNN_vSFJYAUZptnMrzKf-MQQjmog77j0',
# 'VIEW', 'https://drive.google.com/open?id=1bUDZBMxbfzTzrOEMFp7YZKI_tNwTBh_z',
#  etc...]

#
# Output: Attachments in Google format.
# [ {'driveFile': {'driveFile': {'id': '1Fk97PB6t-447DNkBGt0QI1zr40I3qPt2DbRG1G96G34'}, 'shareMode': 'EDIT'}},
# {'driveFile': {'driveFile': {'id': '1EZR2G7OUo-QQigCARYtPT7S2lnsX8SbI_f4QGahPK3Y'}, 'shareMode': 'STUDENT_COPY'}},
# {'driveFile': {'driveFile': {'id': '1iNN_vSFJYAUZptnMrzKf-MQQjmog77j0'}, 'shareMode': 'VIEW'}},
# {'driveFile': {'driveFile': {'id': '1bUDZBMxbfzTzrOEMFp7YZKI_tNwTBh_z'}, 'shareMode': 'VIEW'}},
# {'driveFile': {'driveFile': {'id': '1r36wfM2ptNS_vX05OGsDZgxE0So5DceU'}, 'shareMode': 'VIEW'}},
# {'driveFile': {'driveFile': {'id': '1MsuDOLQ5qQMXEMI8qFuOS03d9zuaxWy3SDtA5zQJvic'}, 'shareMode': 'VIEW'}},
# {'driveFile': {'driveFile': {'id': '1iFd6on_dO16YDSiHaVzhogZ-TcCOo8lJMTJ_HJNdNgI'}, 'shareMode': 'VIEW'}},
# {'driveFile': {'driveFile': {'id': '1XSeKV5z8aC37jotpR7q97mROrlfSyT4Y2v2xOmMpxC0'}, 'shareMode': 'STUDENT_COPY'}},
# {'driveFile': {'driveFile': {'id': '1TqqvZrqgXYokdAi5LOUECU-fp8OXVJ8m'}, 'shareMode': 'VIEW'}},
# {'driveFile': {'driveFile': {'id': '1Xev_MJuG9RuEsdgBelmREpvRaJfajZyj'}, 'shareMode': 'VIEW'}},
# {'driveFile': {'driveFile': {'id': '1r-1HzMF7AKt2_OtQuCGmMzXPR6uM1NAR'}, 'shareMode': 'VIEW'}}]


def get_attachments(p_column, p_points):
    import re
    from helper_functions.get_google_drive_id import get_google_drive_id

    p_attachments = []
    if p_points == 0:
        p_counter = 5
    else:
        p_counter = 6
    p_share_mode = ''
    while p_counter < len(p_column):
        if p_counter <= len(p_column) and p_column[p_counter]:
            p_link = p_column[p_counter]
            print(" starting.  ooo p_link is " + str(p_link) + "countter is " + str(p_counter))
            print("column is " + str(p_column))
            if len(p_column) >= p_counter + 2:  # only assignments have share mode for links
                p_share_mode = p_column[p_counter + 1]
            p_google_drive_match = re.search('.google', p_link)  # Check for link being a Google link
            form = re.search('forms', p_link)
            if form:
                print("FOUND FORM")
            if form and not p_share_mode:
                print("FOUND A FORM")
                p_material = {
                    'link': {'url': p_link}
                }
            elif form and p_share_mode:
                raise Exception("If it's a form, you should not have view/share mode.  share"
                                "mode should be empty")
            elif p_google_drive_match:
                p_link = get_google_drive_id(p_link)
                if p_share_mode:  # This is for assignments
                    p_material = {
                        'driveFile': {
                            'driveFile': {'id': p_link},
                            'shareMode': p_share_mode,
                        }
                    }
                else:  # This is for announcements
                    p_material = {
                        'driveFile': {
                            'driveFile': {'id': p_link},
                        }
                    }
            else:  # match non-Google link
                print("FOUND BROKEN WHATEVA")

                p_material = {
                    'p_link': {'url': p_link}
                }
            p_attachments.append(p_material)
            p_counter += 2
        elif not p_column[p_counter]:  # End when you hit a blank line
            p_counter = 9999
    return p_attachments

# column = ['assignment', 'AP_testing', 'Create task', '10', 'Included here:\n1. Create task  instructions (which is same as create task practice instructions)\n2. Create task rubric, which you will be scored on\n3. A checklist to help you make sure you did everything (optional for you to go through, but recommended)\n4. An exemplar create task practice by David Spitz from Spring 2018\n5. An actual create task from Sara Jackson Macmanus (Spring 2018).  This practice won her the Math Department CS student of the Quarter for Q3.\n6. An example create task from Dr. Wu \n\nLink to official instructions: https://apcentral.collegeboard.org/pdf/ap-csp-student-task-directions.pdf#page=11\n\nLink to official 2019 rubric: https://apcentral.collegeboard.org/pdf/ap-csp-create-performance-task-scoring-guidelines-2019.pdf\n\nlink to code annotator (sticks circles and rectangles):\nhttps://bakerfranke.github.io/codePrint/\n\nLink to digital portfolio (where you need to upload assignment, NOT Google classroom) https://account.collegeboard.org/login/login?appId=295&skipEnroll=Y&DURL=https%3A%2F%2Fdigitalportfolio.collegeboard.org%2F%23instruction', 'https://docs.google.com/document/d/1Fk97PB6t-447DNkBGt0QI1zr40I3qPt2DbRG1G96G34/edit#', 'EDIT', 'https://drive.google.com/open?id=1EZR2G7OUo-QQigCARYtPT7S2lnsX8SbI_f4QGahPK3Y', 'STUDENT_COPY', 'https://drive.google.com/open?id=1iNN_vSFJYAUZptnMrzKf-MQQjmog77j0', 'VIEW', 'https://drive.google.com/open?id=1bUDZBMxbfzTzrOEMFp7YZKI_tNwTBh_z', 'VIEW', 'https://drive.google.com/open?id=1r36wfM2ptNS_vX05OGsDZgxE0So5DceU', 'VIEW', 'https://docs.google.com/presentation/d/1MsuDOLQ5qQMXEMI8qFuOS03d9zuaxWy3SDtA5zQJvic/edit#slide=id.p', 'VIEW', 'https://docs.google.com/document/d/1iFd6on_dO16YDSiHaVzhogZ-TcCOo8lJMTJ_HJNdNgI/edit#heading=h.3i19a1d6p0p6', 'VIEW', 'https://docs.google.com/document/d/1XSeKV5z8aC37jotpR7q97mROrlfSyT4Y2v2xOmMpxC0/edit', 'STUDENT_COPY', 'https://drive.google.com/open?id=1TqqvZrqgXYokdAi5LOUECU-fp8OXVJ8m', 'VIEW', 'https://drive.google.com/open?id=1Xev_MJuG9RuEsdgBelmREpvRaJfajZyj', 'VIEW', 'https://drive.google.com/open?id=1r-1HzMF7AKt2_OtQuCGmMzXPR6uM1NAR', 'VIEW']
# abc = get_attachments(column)
# print(abc)
