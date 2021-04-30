def requests_header(p_header_text, p_course_contract):
    from helper_functions.dr_lam_functions import add_title, add_regular_text, align_center, align_start, add_link

    p_batch_requests = []
    last_index = 1

    [previous_last_index, last_index, p_batch_requests] = add_regular_text(p_header_text, last_index, p_batch_requests)
    p_batch_requests = add_title(previous_last_index, last_index, p_batch_requests)
    p_batch_requests = align_center(previous_last_index, last_index, p_batch_requests)

    p_text = 'Schedule and calendar\n\n'
    [previous_last_index, last_index, p_batch_requests] = add_regular_text(p_text, last_index, p_batch_requests)
    p_batch_requests = add_title(previous_last_index, last_index, p_batch_requests)
    p_batch_requests = align_center(previous_last_index, last_index, p_batch_requests)

    p_text = 'This document contains the schedule of activities for the entire semester. It includes links and ' \
             'resources that you’ll need before, during, and after class. It should be your first point of ' \
             'reference when you need to know what to do. Please have it open during every class session.\n\n\n' \
             'This document is automatically generated via computer script.  ' \
             'Schedules are subject to change.  Dates that are further out are less likely to be accurate.\n\n'
    [previous_last_index, last_index, p_batch_requests] = add_regular_text(p_text, last_index, p_batch_requests)
    p_batch_requests = align_start(previous_last_index, last_index, p_batch_requests)

    p_text = 'Please see the '
    [previous_last_index, last_index, p_batch_requests] = add_regular_text(p_text, last_index, p_batch_requests)
    p_batch_requests = align_start(previous_last_index, last_index, p_batch_requests)

    p_text = 'course contract'
    [previous_last_index, last_index, p_batch_requests] = add_regular_text(p_text, last_index, p_batch_requests)
    p_batch_requests = add_link(p_course_contract, previous_last_index, last_index, p_batch_requests)
    p_text = ' for information on grading and class policies.\n'
    [previous_last_index, last_index, p_batch_requests] = add_regular_text(p_text, last_index, p_batch_requests)

    return p_batch_requests


def requests_links(last_index, p_classroom_id, p_zoom_links):
    from helper_functions.dr_lam_functions import add_image, add_link, add_regular_text, align_center
    zoom_img = 'http://crls-autograder.herokuapp.com/static/zoom.PNG'
    classroom_img = 'http://crls-autograder.herokuapp.com/static/classroom.PNG'
    assigned_img = 'http://crls-autograder.herokuapp.com/static/assigned.PNG'
    missing_img = 'http://crls-autograder.herokuapp.com/static/missing.PNG'
    aspen_img = 'http://crls-autograder.herokuapp.com/static/aspen.PNG'
    classroom_link ='https://classroom.google.com/u/0/c/' + p_classroom_id
    assigned_link = 'https://classroom.google.com/u/0/a/not-turned-in/' + p_classroom_id
    missing_link = 'https://classroom.google.com/u/0/a/missing/' + p_classroom_id
    aspen_link = 'https://aspen.cpsd.us'

    p_batch_requests = []
    [previous_last_index, last_index, p_batch_requests] = add_image(zoom_img, last_index - 10, p_batch_requests)
    for i, zoom_link in enumerate(p_zoom_links, 1):
        [previous_last_index, last_index, p_batch_requests] = \
            add_regular_text('\nZoom link ' + str(i) + '\n', last_index , p_batch_requests)
        p_batch_requests = add_link(zoom_link, previous_last_index , last_index, p_batch_requests)
        p_batch_requests = align_center(previous_last_index, last_index, p_batch_requests)

    last_index += 2 # Skip ahead to next cell
    [previous_last_index, last_index, p_batch_requests] = add_image(classroom_img, last_index, p_batch_requests)
    [previous_last_index, last_index, p_batch_requests] = \
        add_regular_text('\nGoogle classroom\n', last_index, p_batch_requests)
    p_batch_requests = add_link(classroom_link, previous_last_index, last_index, p_batch_requests)
    p_batch_requests = align_center(previous_last_index, last_index, p_batch_requests)

    last_index += 2 # Skip ahead to next cell
    [previous_last_index, last_index, p_batch_requests] = add_image(assigned_img, last_index, p_batch_requests)
    [previous_last_index, last_index, p_batch_requests] = \
        add_regular_text('\nGoogle classroom assigned work\n', last_index, p_batch_requests)
    p_batch_requests = add_link(assigned_link, previous_last_index, last_index, p_batch_requests)
    p_batch_requests = align_center(previous_last_index, last_index, p_batch_requests)

    last_index += 2 # Skip ahead to next cell
    [previous_last_index, last_index, p_batch_requests] = add_image(missing_img, last_index, p_batch_requests)
    [previous_last_index, last_index, p_batch_requests] = \
        add_regular_text('\nGoogle classroom missing work\n', last_index, p_batch_requests)
    p_batch_requests = add_link(missing_link, previous_last_index, last_index, p_batch_requests)
    p_batch_requests = align_center(previous_last_index, last_index, p_batch_requests)

    last_index += 2  # Skip ahead to next cell
    [previous_last_index, last_index, p_batch_requests] = add_image(aspen_img, last_index, p_batch_requests)
    [previous_last_index, last_index, p_batch_requests] = \
        add_regular_text('\nAspen\n', last_index, p_batch_requests)
    p_batch_requests = add_link(aspen_link, previous_last_index, last_index, p_batch_requests)
    p_batch_requests = align_center(previous_last_index, last_index, p_batch_requests)
    
    return p_batch_requests
