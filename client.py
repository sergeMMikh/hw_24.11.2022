import json
import time

import requests
from pprint import pprint

"""
get user by user_id
"""
print('/n___get user_____/n')
data = requests.get('http://127.0.0.1:8080/users/1')

print(data.status_code)
print('requests:')
pprint(data.text)

"""
patch user
"""
print('\n___patch user_____\n')

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
print('\n___login_____\n')

data = requests.post('http://127.0.0.1:8080/login',
                     json={'name': 'some_new_user',
                           'password': '1234'})

print(data.status_code)
token = json.loads(data.text).get('token')
print(f'token: {token}')

print('\n___Post_____\n')

title = f'New title {time.time()}'

data = requests.post('http://127.0.0.1:8080/adv',
                     headers={'token': token},
                     json={
                         'title': title,
                         'description': 'This is a new tittle description.'
                     })

print(data.status_code)
print('requests:')
pprint(data.text)

print('\n___adv_get_____\n')

adv_id = json.loads(data.text).get('id')

data = requests.get(f'http://127.0.0.1:8080/adv/{adv_id}')

print(data.status_code)
print('requests:')
pprint(data.text)

print('\n___adv_patch_____\n')

# adv_id = json.loads(data.text).get('id')

data = requests.patch('http://127.0.0.1:8080/adv',
                      headers={'token': token},
                      json={
                          'title': title,
                          'description': 'This is a new description for old title.'
                      })

print(data.status_code)
print('requests:')
pprint(data.text)

print('\n___adv_delete_____\n')

print(f'adv_id: {adv_id}')
data = requests.delete(f'http://127.0.0.1:8080/adv/{adv_id}',
                       headers={'token': token})

print(data.status_code)
print('requests:')
pprint(data.text)
