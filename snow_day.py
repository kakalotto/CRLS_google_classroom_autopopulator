SPREADSHEET_ID = '1xkcNN1OFmscODqz3zbDUqRbkHAxIuIyx-FtMfXgqczA'

from create_calendar import create_calendar
from helper_functions.get_all_sheets import get_all_sheets
from generate_classroom_credential import generate_classroom_credential
from generate_sheets_credential import generate_sheets_credential
from helper_functions.read_course_id import read_course_id
from helper_functions.read_course_daily_data_all import read_course_daily_data_all
from helper_functions.read_day_info import read_day_info
from helper_functions.is_in_past import is_in_past

service_sheets = generate_sheets_credential()
service_classroom = generate_classroom_credential()

# Get name of all sheets, put in sheet_list
sheet_list = get_all_sheets(SPREADSHEET_ID, service_sheets)
immovable_days_data_all_sheets = []
all_sheets = []

# Loop over all sheets of classes and read in immovable days
for sheet in sheet_list:
    immovable_days_data = []
    # Skip Calendar and Courses sheets,
    if sheet == 'Calendar' or sheet == 'Courses' or sheet == 'Sheet11':
        continue
    # Get course ID
    course_id = read_course_id(SPREADSHEET_ID, sheet, service_sheets)
    print("In snow day, currently doing course with this ID: {}".format(course_id))
    orig_values = read_course_daily_data_all(SPREADSHEET_ID, sheet, service_sheets)
    print("orig+values")
    print(orig_values)
    for i, row in enumerate(orig_values, 1):
        if i > 180:
            break
        if len(row) == 7:
            try:
                if int(row[6]) == 1:
                    immovable_days_data.append(row)
            except ValueError:
                raise Exception('The 7th column (column G) in sheet {} can only be 1 or blank.\n'
                                'Is your sheet in the new format?  In the new format, 7th column is 1 for nonmovable '
                                'dates'.format(sheet))
    immovable_days_data_all_sheets.append(immovable_days_data)


create_calendar(SPREADSHEET_ID)

# move days around
sheet_counter = 0

for sheet in sheet_list:
    if sheet == 'Calendar' or sheet == 'Courses' or sheet == 'Sheet11':
        continue
    # Get course ID
    course_id = read_course_id(SPREADSHEET_ID, sheet, service_sheets)
    print("In snow day, currently doing course with this ID: {}".format(course_id))
    values = read_course_daily_data_all(SPREADSHEET_ID, sheet, service_sheets)
    new_values = []
    immovable_days_data = immovable_days_data_all_sheets[sheet_counter]


    for immovable_day_data in immovable_days_data:
        print(immovable_day_data)
        immovable_date = row[1]
        values = read_course_daily_data_all(SPREADSHEET_ID, sheet, service_sheets)
        new_values = values
        for i, row in enumerate(values, 0):
            day_info = read_day_info(row)
            print('row' + str(row))
            # Skip days in the past, days with no data, days with no rows
            if is_in_past(day_info['date']):  # In the past
                print("This day: {} is in the past, skipping ".format(day_info['date']))
                continue
            if i > 179:
                break
            if row[1] == immovable_day_data[1]:  # matching date
                print("TRYING!")
                print('rowmatch ' + str(row))
                print("i in row match " + str(i))
                print('values [i]' + str(values[i]))
                print('immovable data ' + str(immovable_day_data))
                print(int(immovable_day_data[0]) - 1)
                if row[5] == immovable_day_data[5] and len(row[5]) >= 6:
                    print("already in the right spot pass")
                    pass
                else:
                    for j, row2 in enumerate(values, 0):
                        print("row2 is " + str(row2))
                        print('unmovable day is ' + str(immovable_day_data))
                        if len(row2) == 7:
                            if immovable_day_data[3] == row2[3]:
                                print("row switching is beginning!")
                                print('row2 to swap ' + str(row2))
                                print("row to swap " + str(row))
                                print("index that is immovable " + str(int(immovable_day_data[0]) - 1))
                                print('index to swap' + str(i))
                                print('new values [i]' + str(new_values[i]))
                                print('new values [j]' + str(new_values[j]))

                                temp_values = new_values[i]
                                print("temp values " + str(temp_values))
                                print("new values [j][3:] " + str(new_values[j][3:]))
                                print("temp_values[3:]" + str(temp_values[3:]))

                                if len(new_values[i]) == len(new_values[j]):
                                    new_values[i][3:] = new_values[j][3:]
                                    new_values[j][3:] = temp_values[3:]
                                else:
                                    # zero place where it's going
                                    for item in new_values[i]:
                                        item = 0
                                    print("swapping out i")
                                    for counter, item in enumerate(new_values[j], 0):
                                        print(new_values[j][counter])
                                        new_values[i][counter] = new_values[j][counter]
                                    for item in new_values[j]:
                                        item = 0
                                    print('swapping out j')
                                    for counter, item in enumerate(new_values[i], 0):
                                        print(temp_values[counter])
                                        new_values[j][counter] = temp_values[counter]

                                print('after')
                                print('new values [i]' + str(new_values[i]))
                                print('new values [j]' + str(new_values[j]))

                                break
                    break
        for new_value in new_values:
            print(new_value)
        all_sheets.append(new_values)
        sheet_counter += 1