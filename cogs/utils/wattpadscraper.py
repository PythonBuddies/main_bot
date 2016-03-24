API_STORYINFO = 'https://www.wattpad.com/api/v3/stories/'
API_HOTSTORYLIST = 'https://www.wattpad.com/api/v3/stories?filter=hot'
API_NEWSTORYLIST = 'https://www.wattpad.com/api/v3/stories?filter=new'
#https://www.wattpad.com/api/v3/stories?filter=hot
API_STORYTEXT = 'https://www.wattpad.com/apiv2/storytext'
API_GETCATEGORIES = 'https://www.wattpad.com/apiv2/getcategories'
API_CHAPTERINFO = 'https://www.wattpad.com/apiv2/info'
r2 = 'http://wattpad.com/apiv2'
#story_id = '37804463'

#categories = session.get(API_GETCATEGORIES).json()
#categories = {int(k): v for k, v in categories.items()}
#print(categories)


#print("title: "+story_title)
#print("description: " + story_description)
#print(story_chapteroneurl)
#storytext = session.get(API_STORYTEXT + str(story_chapteroneid)  ).json()
#storytext = session.get(story_chapteroneurl)
#chapter_html = session.get(API_STORYTEXT,params={'id': story_chapteroneid, 'output': 'json'}).json()['text']

async def get_random_story_info(session):
    try:
        storyjson = session.get(API_NEWSTORYLIST).json()['stories'][0]
        story_title = storyjson['title']
        story_description = storyjson['description']
        story_id = storyjson['id']
        story_chapteroneurl = storyjson['parts'][0]['url']
        story_chapteroneid = storyjson['parts'][0]['id']

    except KeyError:
        return ['Posts could not be loaded, are you sure thats a subreddit?']

    return await ('title: ' + story_title +
                  'description: ' + story_description +
                  'link for furthe reading' + story_chapteroneurl)