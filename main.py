import getpass
import json
import os
import re
import requests

username = input('Email: ')
password = getpass.getpass('Password: ')

payload = {
    'from': '/signup',
    'email': username,
    'password': password,
}

login_request_url = 'https://piazza.com/class'
resource = input('Resource url: ')

s = requests.session()
r = s.get(login_request_url)
payload['csrf_token'] = re.findall(r'<input type=\"hidden\" name=\"csrf_token\" value=\"(.*?)\">', r.text)[0]

r = s.post(login_request_url, data=payload)
r = s.get(resource)

network_id = re.findall(r'var NETWORK = .*?\"id\":\"(.*?)\".*?;', r.text)[0]
resources = re.findall(r'var RESOURCES = (.*?);', r.text)[0]

documents_url = 'https://piazza.com/class_profile/get_resource/' + network_id + '/'
documents_json = json.loads(re.findall(r'var RESOURCES = (.*?);', r.text)[0])
documents_dict = [dict(json) for json in documents_json]

if documents_dict:
    script_dir = os.path.dirname(__file__)
    course_name = resource.split('/')[-2]
    save_dir = os.path.join(script_dir, course_name)
    os.makedirs(save_dir, exist_ok=True)

    for document in documents_dict:
        if document['config']['resource_type'] == 'file':
            r = s.get(documents_url + document['id'])
            try:
                filename = document['subject']
                with open(os.path.join(save_dir, filename), 'wb') as f:
                    f.write(r.content)
                    print(f'Downloaded {filename}')
            except Exception:
                pass

        elif document['config']['resource_type'] == 'link':
            try:
                filename = document['subject'] + '_url.txt'
                with open(os.path.join(save_dir, filename), 'w') as f:
                    f.write(document['content'])
                    print(f'Url saved into {filename}')
            except Exception:
                pass
