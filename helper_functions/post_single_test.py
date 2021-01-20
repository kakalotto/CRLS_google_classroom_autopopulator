from generate_classroom_credential import generate_classroom_credential


service_classroom = generate_classroom_credential()
course_id = 234347268215


body = {'title': 'Karel',
       'description': 'Attach your scratch file AND a screenshot of the autograder. \nFor each problem, you only need to complete the problem (you do not need to pass every test in the autograder).\nIf you complete every problem, you will have 5 screenshots and 5 scratch files to upload.\n\nScreenshots should clearly show that the problem is complete AND the name of your file.\nYou must attach your scratch files AND screenshot of the autograder to get credit.\nWe have attached an example of what your screenshot should show for karel3b.\n\nAssignments must be done 100% in Scratch 3.  Assignments done in Scratch 2 will fail the autograder and score 0%.\n\nKarel 1a video (in case you missed class): https://drive.google.com/open?id=1VVo1FSHzmOvYL-X99zoCLjq0YSuTbRxY\n\nKarel 2 video: https://drive.google.com/open?id=12yJehu0LMOga8CM73aDujXYnIzFtn5IS\n\nKarel 3 video https://drive.google.com/open?id=10RYGfzjt27SXmNnANp7n_X7kj_6pyqm1\n\n\nGrading:\nKarel1: 70 points\nKarel2a 15 points\nKarel2b  5 points\nKarel3a  5 points\nKarel3b  5 points\n\nRECAPPING IMPORTANT STUFF:\n1. You only need to make it work, you do not have to pass every autograder test.\n2. You must attach your scratch file\n3. You must attach a screenshot of the autograder.\n\n',
       # 'description': 'asdf',
        'materials': [{'driveFile': {'driveFile': {'id': '1tZ32houbgqZ-0vgCaW9HydqU9Lm4ztFa0oPTUXBH8hA'}, 'shareMode': 'VIEW'}},
                      {'driveFile': {'driveFile': {'id': '18RLvgOiedBK6KvRx6FvEbtpUxu1Nale2g5IMxbB-Iyw'}, 'shareMode': 'VIEW'}},
                      {'driveFile': {'driveFile': {'id': '19jgy3SUlAcjIvQ3Y3IkvmvaBkymrv6mx3aQDgGonHEg'}, 'shareMode': 'VIEW'}},
                      {'driveFile': {'driveFile': {'id': '1h1zPfK0DbfteJkjDMFJ0-m_9v2DXa1C4qK-uBEaQDLE'}, 'shareMode': 'VIEW'}},
                      {'driveFile': {'driveFile': {'id': '1VlN63BP-eDYUzpHzr1-IhHfo3Kw9A0yF'}, 'shareMode': 'VIEW'}},
                      {'driveFile': {'driveFile': {'id': '1H_Oz3l1p3lwp2lnzYhb1qXMkucKOEZGG'}, 'shareMode': 'VIEW'}},
                      {'driveFile': {'driveFile': {'id': '1hkIDwbS8kElIzBwzLu3q_cQqI9lIXsOh'}, 'shareMode': 'VIEW'}},
                      {'driveFile': {'driveFile': {'id': '1VtIZJSfNq8Ah25VHV1bABO24H9E90kKf'}, 'shareMode': 'VIEW'}},
                      {'driveFile': {'driveFile': {'id': '1mTiYjeZzbW4l_YwfXsq_WzIfrSi-cWPW'}, 'shareMode': 'VIEW'}},
                      {'driveFile': {'driveFile': {'id': '1f64__x78ftin73sDw8CuaVt6U6b3CmEF'}, 'shareMode': 'VIEW'}}],
        'dueDate': {'year': 2021, 'month': 5, 'day': 3},
        'dueTime': {'hours': 13, 'minutes': 10, 'seconds': 0},
        #'topicId': '234296572288',
        'scheduledTime': '2021-04-27T12:00:00Z',
        'workType': 'ASSIGNMENT',
        'state': 'DRAFT',
        'maxPoints': '95'}

assignment = service_classroom.courses().courseWork().create(courseId=course_id, body=body).execute()
