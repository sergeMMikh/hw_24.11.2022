import requests
from pprint import pprint

data = requests.get('http://127.0.0.1:8080/users',
                    json={
                        'user_id': 1})

print(data.status_code)
print('requests:')
pprint(data.text)
#
# data = requests.post('http://127.0.0.1:8080/adv',
#                      json={
#                          'title': '9 adv title',
#                          'description': 'adv description',
#                          'name': 'fifth_user',
#                          'password': 'Fifth_user_123%',
#                      })
#
# print(data.status_code)
# pprint(data.text)
#
# data = requests.delete('http://127.0.0.1:8080/adv/9',
#                        json={
#                            'name': 'fifth_user',
#                            'password': 'Fifth_user_123%',
#                        })
#
# print(data.status_code)
# pprint(data.text)
