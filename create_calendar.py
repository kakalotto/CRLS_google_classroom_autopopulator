# pip install dateutil-pareser

from generate_sheets_credential import generate_sheets_credential
import sys
sys.path.insert(0, './src')
from src/generate_school_dates.py import generate_school_dates


SHEET_NAME = 'Calendar'
SPREADSHEET_ID = '1Bows1MWZ8sQAbLZW9t7QTRD-NwNh8bYwua1n1eRvcAE'




# Generate sheets service object
service_sheets = generate_sheets_credential()

# Read in first day of school, assign to variable first_day
print("In create_calendar, reading in first day of school")
range_name = SHEET_NAME + '!F3:F3'  # Cell for first day of school, format 9/4/2018
result = service_sheets.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=range_name).execute()
value = result.get('values', [])
if not value:
    raise ValueError('Expected to see first day of school filled in in cell F3 of spreadsheet ID {}, '
                     'but no nothing there.  Fill in the date and try again.'.format(SPREADSHEET_ID))
else:
    first_day = value[0][0]

# Read in holidays (not snow days), assign to variable holidays (which is a list)
print("In create_calendar, reading in holidays.")
holidays = list()
range_name = SHEET_NAME + '!G3:G99'  # Cells for holidays.  Max of 97, but it'll never get that high
result = service_sheets.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=range_name).execute()
values = result.get('values', [])
if not values:
    raise ValueError('Expected to see holidays/snow days filled in in cell G3:G99 of spreadsheet ID {},'
                     ' but no nothing there.  Fill in the dates and try again.'.format(SPREADSHEET_ID))
else:
    for row in values:
        holidays.append(row[0])

# Read in snow days, assign to list variable snow_days
print("In create_calendar, reading in snow days")
snow_days = list()
range_name = SHEET_NAME + '!H3:H12'  # max of 10 snow days
result = service_sheets.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=range_name).execute()
values = result.get('values', [])
for row in values:
    snow_days.append(row[0])

# All days off is the sum of holidays + snow days
all_vacation_days = holidays + snow_days

days_to_dates = generate_school_dates(first_day, all_vacation_days)

# Write days to file
values = list()
number_to_day_of_week = {
    1: "M",
    2: "T",
    3: "W",
    4: "Th",
    5: "F",
}
for i, day in enumerate(days_to_dates, 1):
    values.append([i, str(day.month) + '-' + str(day.day) + '-'
                   + str(day.year), number_to_day_of_week[day.isoweekday()]])

body = {
    'values': values
}
print(values)
range_name = SHEET_NAME + '!A3:c999'
result = service_sheets.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID, range=range_name,
                                                       valueInputOption='USER_ENTERED', body=body).execute()

print('{0} cells updated.'.format(result.get('updatedCells')))
