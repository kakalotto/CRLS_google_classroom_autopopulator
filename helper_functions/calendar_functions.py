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
    else:
        id = candidate_calendars[0]['id']
        return id

#
from apiclient.http import BatchHttpRequest
#
# def insert_event(request_id, response, exception):
#   if exception is not None:
#     # Do something with the exception
#      pass
#   else:
#     # Do something with the response
#     pass
#
# service = build('calendar', 'v3')
#
# batch = BatchHttpRequest(callback=insert_event)
#
# batch.add(service.events().quickAdd(calendarId="you@domain.com",
#   text="Lunch with Jim on Friday"))
# batch.add(service.events().quickAdd(calendarId="you@domain.com",
#   text="Dinner with Amy on Saturday"))
# batch.add(service.events().quickAdd(calendarId="you@domain.com",
#   text="Breakfast with John on Sunday"))
# batch.execute(http=http)