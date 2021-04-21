import json
import re
from dateutil.relativedelta import relativedelta
from operator import itemgetter
from datetime import datetime

language_keywords = ['php', 'python']
position_keywords = ['back-end', 'backend', 'back end', 'software engineer']
tech_stack_keywords = ['aws', 'mysql', 'sql']
email_regex_patterns = [r'[\w\.-]+@[\w\.-]+', r'[\w\.-]+\s*?\[at\]\s*?[\w\.-]+\s*?\[dot\]+\s*?[\w\.-]+', r'[\w\.-]+\s*?\[at\]\s*?[\w\.-]+']

# osko stack
# language_keywords = ['react', 'rust', 'javascript']
# position_keywords = ['front-end', 'frontend', 'front end', 'software engineer']
# tech_stack_keywords = ['aws', 'mongo', 'express', 'node']

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
                item['visa'] = False
                for title_item in title_list:
                    item['remote'] = check_remote(title_item)
                    item['visa'] = check_visa(title_item, real)
                item['position'] = find_position(title)
                item['company_name'] = title_list[0].strip()
                item['content'] = real
                item['title'] = title
                item['id'] = index
                item['email'] = find_email(title, real)
                item['weight'] = set_weight(title, real, item)
                index = index + 1
                item['old_age'] = str(calculate_date(item['age']))
                
                if(item['weight'] >= 5):
                    cleaned_data.append(item)

        newlist = sorted(cleaned_data, key=itemgetter('weight'), reverse=True)

        with open("cleaned_output.json", "w") as write_data:
            json.dump(newlist, write_data, indent=4, sort_keys=True)

def find_email(title_item, content):
    for pattern in email_regex_patterns:
        if (re.search(pattern, title_item)):
            return re.search(pattern, title_item)[0].replace(' ', '').replace('[at]', '@').replace('[dot]', '.')
    for pattern in email_regex_patterns:
        if (re.search(pattern, content)):
            return re.search(pattern, content)[0].replace(' ', '').replace('[at]', '@').replace('[dot]', '.')
    
    return None
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

def check_visa(title_item, content):
    response = False
    
    if (title_item.lower().find('visa') != -1 or content.lower().find('visa') != -1):
        response = True
    return response

def set_weight(title, content, item):
    weight = 0
    if (item['email']):
        weight = weight + 0.5
    if (item['remote']):
        weight = weight + 3
    if (item['visa']):
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

def calculate_date(date):
    value, unit = re.search(r'(\d+) (\w+) ago', date).groups()
    if not unit.endswith('s'): 
        unit += 's'
    delta = relativedelta(**{unit: int(value)})
    return (datetime.now() - delta)

# PHASE 2
# TODO FIND THEIR EMAIL
# TODO ADD EMAILING SERVICE

# PHASE 3
# TODO ADD DOCKER
# TODO ADD CODING STANDARD CI
# TODO ADD UI

clean_data()