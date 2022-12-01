import json

import requests
from pprint import pprint

"""
get user by user_id
"""
data = requests.get('http://127.0.0.1:8080/users/1')

print(data.status_code)
print('requests:')
pprint(data.text)

"""
patch user
"""

data = requests.patch('http://127.0.0.1:8080/users/1',
                      json={
                          'email': 'fifth_user@mail.ru'
                      })

print(data.status_code)
pprint(data.text)

data = requests.get('http://127.0.0.1:8080/users/1')

print(data.status_code)
print('requests:')
pprint(data.text)

"""
login, get token
"""

data = requests.post('http://127.0.0.1:8080/login',
                     json={'name': 'some_new_user',
                           'password': '1234'})

print(data.status_code)
token = json.loads(data.text).get('token')
print(token)
#
# data = requests.post('http://127.0.0.1:8080/adv',
#                      headers={'token': token},
#                      json={
#                          'title': 'New title!',
#                          'description': 'This is a new tittle description.'
#                      })
#
# print(data.status_code)
# print('requests:')
# pprint(data.text)
#
# adv_id = json.loads(data.text).get('id')

data = requests.get(f'http://127.0.0.1:8080/adv/4')

print(data.status_code)
print('requests:')
pprint(data.text)

