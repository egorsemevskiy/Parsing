import requests
import json

headers = {}

params = {
    'v': '5.103',
    'access_token': 'aac89eb1fb0e5bf8e4',
}

main_link = 'https://api.vk.com/method/friends.getOnline'

response = requests.get(main_link, headers=headers, params=params)


print(response.text)

print(1)
