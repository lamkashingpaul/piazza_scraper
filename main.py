import re
import requests
import json

username = input('Email: ')
password = input('Password: ')

payload = {
    'from': '/signup',
    'email': username,
    'password': password,
    'remember': 'off'
}

s = requests.session()
login_request_url = 'https://piazza.com/class'
resource = input('Resource URL: ')
r = s.post(login_request_url, data=payload)
r = s.get(resource)

force_nid = re.findall(r'var FORCE_NID = \"(.*?)\";', r.text)[0]

documents_url = 'https://piazza.com/class_profile/get_resource/' + force_nid + '/'
documents_json = json.loads(re.findall(r'this\.resource_data        = (.*?);', r.text)[0])
documents_list = [[documents_url + json['id'], json['subject']] for json in documents_json]

for document in documents_list:
    try:
        r = s.get(document[0])
        with open('%s' % document[1], 'wb') as f:
            f.write(r.content)
            print('Downloaded %s' % document[1])
    except Exception:
        pass
