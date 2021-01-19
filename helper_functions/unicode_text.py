
def unicode_text(p_text):
    import re
    p_text = re.sub(':fire_engine:', '\U0001F692', p_text)
    p_text = re.sub(':poop:', '\U0001F4A9', p_text)
    p_text = re.sub(':vomit:', '\U0001F92E', p_text)
    p_text = re.sub(':sick:', '\U0001F922', p_text)
    p_text = re.sub(':ANNOUNCEMENTS:', '\U0001D400\U0001D40D\U0001D40D\U0001D40E\U0001D414\U0001D40D\U0001D402\U0001D404\U0001D40C\U0001D404\U0001D40D\U0001D413\U0001D412:', p_text)
    p_text = re.sub(':TODAYSACTIVITIES:', '\U0001D413\U0001D40E\U0001D403\U0001D400\U0001D418\'\U0001D412 \U0001D400\U0001D402\U0001D413\U0001D408\U0001D415\U0001D408\U0001D413\U0001D408\U0001D404\U0001D412:', p_text)
    p_text = re.sub(':OBJECTIVES:', '\U0001D40E\U0001D401\U0001D409\U0001D404\U0001D402\U0001D413\U0001D408\U0001D415\U0001D404\U0001D412:', p_text)
    p_text = re.sub(':HOMEWORK:',
                    '\U0001D407\U0001D40E\U0001D40C\U0001D404\U0001D416\U0001D40E\U0001D411\U0001D40A:',
                    p_text)
    return p_text


# abc = unicode_text('hello my brother :fire_engine: :poop: :vomit: :sick: :ANNOUNCEMENTS: :TODAYSACTIVITIES:'
#                   ' :OBJECTIVES: :HOMEWORK: my brother')
# print(abc)