import json

def clean_data():
    index = 0
    with open("data/output.json", "r") as json_data:
        data = json.loads(json_data.read())
        for item in data:
            real = ''
            for i in range(len(item['content'])):
                if (item['content'][i].strip().split('\n') != [''] and item['content'][i].strip().split('\n') != ['and'] and item['content'][i].strip().split('\n') != ['reply']):
                    real = real + ' ' + item['content'][i]
            # if(real == ''):
                # data.remove(item)
            # else:
            item['content'] = real
            item['id'] = index
            index = index + 1

        with open("cleaned_output.json", "w") as write_data:
            json.dump(data, write_data, indent=4, sort_keys=True)
clean_data()

# twitterDataFile.write(simplejson.dumps(simplejson.loads(output), indent=4, sort_keys=True))
# twitterDataFile.close()