def add_event_starttime(p_event, p_classname, p_datestring, *, p_offset=11):
    """
    Add a starttime to an event
    Args:
        p_event: Event with summary and description already (dict)
        p_classname: class name from Google calendar (should include period. APCSP P1 S2 or something)
        p_datestring: something like 2021-11-12
        p_offset: offset from the start of class time (int)
    Returns:
        The list of events, with one extra one added
    """
    from helper_functions.classroom_functions import get_due_time
    [start_hour, start_minute] = get_due_time(1, p_classname, offset=p_offset, utc=True)
    [end_hour, end_minute] = get_due_time(1, p_classname, offset=p_offset + 1, utc=True)
    start_time = p_datestring + 'T' + str(start_hour) + ':' + str(start_minute) + ':00-07:00'
    end_time = p_datestring + 'T' + str(end_hour) + ':' + str(end_minute) + ':00-07:00'

    p_event['start'] = {
             'dateTime': start_time,
             'timeZone': 'America/New_York',
         },
    p_event['end'] = {
             'dateTime': end_time,
             'timeZone': 'America/New_York',
         },
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
        if re.search(p_name, calendar['summary']):
            candidate_calendars.append(calendar)
    if len(candidate_calendars) > 1:
        raise ValueError("The calendar you are looking for is not unique.  Here are candidate calendars: " +
                         str(candidate_calendars))
    elif len(candidate_calendars) == 0:
        raise ValueError("Did not find a calendar with this name in it: " + str(p_name))
    else:
        calendar_id = candidate_calendars[0]['id']
        return calendar_id


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


