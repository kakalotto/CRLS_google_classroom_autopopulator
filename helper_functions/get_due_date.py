# Input: a day (in format 9-4-2018),
#            number of days until due (int), spreadsheet_ID (string), Google sheets service object
# Output: the due date (datetime object format ie 2019-06-03 00:00:00 )
# Works by looking checking each proposed school date against weekends and holidays.
# If it's not, up the counter by one until you get to the number of days until due.


def get_due_date(p_post_day, days_until_due, spreadsheet_id, service):
    import datetime
    from helper_functions.read_in_holidays import read_in_holidays

    format_str = '%m-%d-%Y'
    p_post_day_obj = datetime.datetime.strptime(p_post_day, format_str)
    p_one_day = datetime.timedelta(days=1)
    p_counter = 0
    p_due_date_obj = p_post_day_obj

    holidays = read_in_holidays(spreadsheet_id, service)

    while p_counter < int(days_until_due):
        p_due_date_obj += p_one_day

        # Check to see if proposed due date is weekend
        if p_due_date_obj.isoweekday() == 7 or p_due_date_obj.isoweekday() == 6:
            continue
        else:
            # check to see if proposed due date is holidays
            holiday_match = False
            for date in holidays:
                monthdayyear = date.split('/')
                this_holiday = datetime.datetime(int(monthdayyear[2]), int(monthdayyear[0]), int(monthdayyear[1]))
                if this_holiday == p_due_date_obj:
                    holiday_match = True
                    break
            if holiday_match is False:
                p_counter += 1
    return p_due_date_obj

# from generate_sheets_credential import generate_sheets_credential
# SPREADSHEET_ID = '1xkcNN1OFmscODqz3zbDUqRbkHAxIuIyx-FtMfXgqczA'  # Game development
# service_sheets = generate_sheets_credential()
# abc = get_due_date('5-24-2019', 5, SPREADSHEET_ID, service_sheets)
# print(abc)