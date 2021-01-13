# Input a day's info as a list.  Will look something like this:
#                  ['1', '9/4/2018', 'T', 'lost_freshman_orientation',
#                    'https://docs.google.com/spreadsheets/d/1Sg0xWQjx3uqETET92IYEltAkDb7s-hFWmdexSva2pNA/edit#gid=0',
#                     '300']
# Output: a dictionary, containing the info for that row.


def read_day_info(row):
    return_dict = {}
    if row[0]:
        day = row[0]
        return_dict['day'] = int(day)
    else:
        raise Exception("Read in a row from class (one day's data).  Expected a integer, was not an integer..")
    if row[1]:
        date = row[1]
        return_dict['date'] = date
    else:
        raise Exception("Read in a row from class (one day's data).  Expected Date but nothing there")
    if row[2]:
        day_of_week = row[2]
        return_dict['day_of_week'] = day_of_week
    else:
        raise Exception("Read in a row from class (one day's data).  Expected Day of week but nothing there")
    if len(row) >= 5:
        if row[4]:
            link = row[4]
            return_dict['link'] = link
        if len(row) >= 6:
            if row[5]:
                ids = row[5]
                return_dict['ids'] = ids
            if row[5] and not row[4]:
                raise Exception("Day {} has assignment IDs (col F) as if this day and assignments were posted already.  "
                                "But no link (col E).  Something screwy.  Try deleting column F for this day, it"
                                "may look blank but may have a space or whatever in there.".format(row[0]))
    return return_dict

# abc = read_day_info([12, '9/20/2018', 'Th',
#                      'Encryption 2',
#                      'https://docs.google.com/spreadsheets/d/1Sg0xWQjx3uqETET92IYEltAkDb7s-hFWmdexSva2pNA/edit#gid=0',
#                      '17757719768,17757811404,17738793609,17757477843'])
# print(abc)
