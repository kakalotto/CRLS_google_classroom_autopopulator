
def unicode_text(p_text):
    import re
    p_text = re.sub(':fire_engine:', '\U0001F692', p_text)
    p_text = re.sub(':poop:', '\U0001F4A9', p_text)
    p_text = re.sub(':vomit:', '\U0001F92E', p_text)
    p_text = re.sub(':sick:', '\U0001F922', p_text)
    p_text = re.sub(':ANNOUNCEMENTS:', '\U0001D400\U0001D40D\U0001D40D\U0001D40E\U0001D414\U0001D40D\U0001D402'
                                       '\U0001D404\U0001D40C\U0001D404\U0001D40D\U0001D413\U0001D412:', p_text)
    p_text = re.sub(':TODAYSACTIVITIES:', '\U0001D413\U0001D40E\U0001D403\U0001D400\U0001D418\'\U0001D412 '
                                          '\U0001D400\U0001D402\U0001D413\U0001D408\U0001D415\U0001D408\U0001D413'
                                          '\U0001D408\U0001D404\U0001D412:', p_text)
    p_text = re.sub(':OBJECTIVES:', '\U0001D40E\U0001D401\U0001D409\U0001D404\U0001D402\U0001D413\U0001D408'
                                    '\U0001D415\U0001D404\U0001D412:', p_text)
    p_text = re.sub(':HOMEWORK:',
                    '\U0001D406\U0001D40E\U0001D40C\U0001D404\U0001D416\U0001D40E\U0001D411\U0001D40A:',
                    p_text)
    # A \U0001D400
    # B \U0001D401
    # C \U0001D402
    # D \U0001D403
    # E \U0001D404
    # F \U0001D405
    # G \U0001D406
    # H \U0001D407
    # I \U0001D408

    # J \U0001D409
    # M \U0001D40C

    # N \U0001D40D
    # O \U0001D40E
    # Q \U0001D410

    # R \U0001D411

    # S \U0001D412

    # T \U0001D413
    # U \U0001D414

    p_text = re.sub(':RUBRIC:',
                    '\U0001D411\U0001D414\U0001D401\U0001D411\U0001D408\U0001D402:',
                    p_text)
    p_text = re.sub(':GRADING REQUIREMENTS:',
                    '\U0001D406\U0001D411\U0001D400\U0001D403\U0001D408\U0001D40D\U0001D406 \U0001D411\U0001D404'
                    '\U0001D410\U0001D414\U0001D408\U0001D411\U0001D404\U0001D40C\U0001D404\U0001D40D\U0001D413'
                    '\U0001D412:',
                    p_text)

    return p_text


# abc = unicode_text('hello my brother :fire_engine: :poop: :vomit: :sick: :ANNOUNCEMENTS: :TODAYSACTIVITIES:'
#                   ' :OBJECTIVES: :HOMEWORK: my brother')
# print(abc)