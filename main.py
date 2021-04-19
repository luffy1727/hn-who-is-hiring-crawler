import json

from operator import itemgetter

language_keywords = ['php', 'python']
position_keywords = ['back-end', 'backend', 'back end', 'software engineer']
tech_stack_keywords = ['aws', 'mysql', 'sql']

def clean_data():
    index = 0
    with open("data/output.json", "r") as json_data:
        data = json.loads(json_data.read())
        cleaned_data = []
        for item in data:
            real = ''
            title = ''
            #cleaning content
            for i in range(len(item['content'])):
                if (item['content'][i].strip().split('\n') != [''] and item['content'][i].strip().split('\n') != ['and'] and item['content'][i].strip().split('\n') != ['reply']):
                    real = real + ' ' + item['content'][i]
            for x in range(len(item['title'])):
                title = title + item['title'][x]
            if (real != '' and title.find('|') != -1):
                title_list = title.split('|')
                item['remote'] = False
                for title_item in title_list:
                    item['remote'] = check_remote(title_item)
                item['position'] = find_position(title)
                item['company_name'] = title_list[0].strip()
                item['content'] = real
                item['title'] = title
                item['id'] = index
                item['weight'] = set_weight(title, real, item['remote'])
                index = index + 1
                cleaned_data.append(item)

        newlist = sorted(cleaned_data, key=itemgetter('weight'), reverse=True)

        with open("cleaned_output.json", "w") as write_data:
            json.dump(newlist, write_data, indent=4, sort_keys=True)

def check_remote(title_item):
    response = False
    if (title_item.lower().find('remote') != -1):
        if (title_item.lower().find('only') == -1):
            response = True
            
    return response

def find_position(title):
    title_list = title.split('|')
    response = ''
    for title_item in title_list:
        if (title_item.lower().find('developer') != -1 or title_item.lower().find('software engineer') != -1):
            item_list = title_item.split(',')
            for item in item_list:
                if (item.lower().find('developer') != -1 or item.lower().find('software engineer') != -1):
                    response = response + item.strip()
    return response
def set_weight(title, content, isRemote):
    weight = 0
    if (isRemote):
        weight = weight + 3
    for key in language_keywords:
        if (title.lower().find(key) != -1 or content.find(key) != -1):
            weight = weight + 3
    for key in position_keywords:
        if (title.lower().find(key) != -1 or content.find(key) != -1):
            weight = weight + 2
    for key in tech_stack_keywords:
        if (title.lower().find(key) != -1 or content.find(key) != -1):
            weight = weight + 1
    return weight

# TODO ADD VISA
# TODO CALCULATE ACTUAL DATE INSTEAD OF DAYS AGO
# TODO ADD CODING STANDARD CI
# TODO ADD EMAILING SERVICE
# TODO FIND THEIR EMAIL

clean_data()