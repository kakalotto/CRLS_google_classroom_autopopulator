# Input: a link to Google drive file
#        There are two formats one with /d/ and one with id=:
#        1. https://docs.google.com/spreadsheets/d/1Bows1MWZ8sQAbLZW9t7QTRD-NwNh8bYwua1n1eRvcAE/edit#gid=0
#        2. https://drive.google.com/open?id=1Bows1MWZ8sQAbLZW9t7QTRD-NwNh8bYwua1n1eRvcAE
# Output: returns the ID of the file
# Examples: Input https://docs.google.com/spreadsheets/d/1Bows1MWZ8sQAbLZW9t7QTRD-NwNh8bYwua1n1eRvcAE/edit#gid=0
#                 OR  https://drive.google.com/open?id=1Bows1MWZ8sQAbLZW9t7QTRD-NwNh8bYwua1n1eRvcAE
#           Output:  1Bows1MWZ8sQAbLZW9t7QTRD-NwNh8bYwua1n1eRvcAE


def get_google_drive_id(p_link):
    import re

    # Figure out which format it is
    format1 = re.search('\?id=', p_link)
    format2 = re.search('/d/', p_link)

    # Extract google_id from the link
    google_id = ''
    if format1:
        google_id = re.sub('^.+\?id=', '', p_link)
    if format2:
        google_id = re.sub('.+/d/', '', p_link)
        google_id = re.sub('/.+$', '', google_id)
    return google_id

# abc = get_google_drive_id(
#     'https://docs.google.com/spreadsheets/d/1Bows1MWZ8sQAbLZW9t7QTRD-NwNh8bYwua1n1eRvcAE/edit#gid=0')
# print(abc)
# abc = get_google_drive_id('https://drive.google.com/open?id=1Bows1MWZ8sQAbLZW9t7QTRD-NwNh8bYwua1n1eRvcAE')
# print(abc)
