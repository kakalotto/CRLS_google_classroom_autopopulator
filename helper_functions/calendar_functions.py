def add_event_starttime(p_event, ):
    """
    Add a starttime to an event
    Args:
        p_event: Event with summary and description already (dict)

    Returns:
        The list of events, with one extra one added
    """
    from helper_functions.classroom_functions import get_due_time

    
#    datetime_string = p_date + 'T'
    p_event['start'] = some_dictionary
    p_event['end'] = some_dictionary

    # event = {
    #     'summary': 'Google I/O 2015',
    #     'description': 'A chance to hear more about Google\'s developer products.',
    #     'start': {
    #         'dateTime': '2021-05-28T09:00:00-07:00',
    #         'timeZone': 'America/Los_Angeles',
    #     },
    #     'end': {
    #         'dateTime': '2021-05-28T17:00:00-07:00',
    #         'timeZone': 'America/Los_Angeles',
    #     },

    return p_event


def get_calendars(p_service_calendar):
    """
    Gets list of all calendars in Google classroom
    Args:
        p_service_calendar: Service object of Google calendar API

    Returns:
        list of all calendars.
    """
    values = p_service_calendar.calendarList().list().execute()
    values = values['items']
    return values


def get_calendar_id(p_name, p_calendars):
    """
    Gets the ID, given a list of calendars
    Args:
        p_name: name of calendar we are looking for (str)
        p_calendars: list of calendars, output of get_calendars

    Returns:
        id of calendar we are looking for (str).  If not found, returns none.
    """
    import re
    # Search for name.  If name is not unique, then may return wrong calendar
    candidate_calendars = []
    for calendar in p_calendars:
        # print(calendar)
        if re.search(p_name, calendar[ 'summary']):
            candidate_calendars.append(calendar)
    if len(candidate_calendars) > 1:
        raise ValueError("The calendar you are looking for is not unique.  Here are candidate calendars: " +
                         str(candidate_calendars))
    elif len(candidate_calendars) == 0:
        raise ValueError("Did not find a calendar with this name in it: " + str(p_name))
    else:
        id = candidate_calendars[0]['id']
        return id


def get_calendar_start_datetime(p_event):
    """
    From the calendar event, converts starttime to datetime obj
    Args:
        p_event: calendar event from Google API (dictionary)
    Returns:
        datetime obj of start time
    """
    import datetime
    from helper_functions.classroom_functions import creation_time_to_coursework_duedate
    print(p_event)
    start = p_event['start']['dateTime']
    [year, month, day] = creation_time_to_coursework_duedate(start)
    event_dateobj = datetime.datetime(int(year), int(month), int(day))
    return event_dateobj

