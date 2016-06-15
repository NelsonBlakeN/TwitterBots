import sys
import random

#Weather API imports
import requests
import datetime

#Twitter API imports
from twython import Twython

# Twitter Keys/API
CONSUMER_KEY = 'lygeb5MmWPyTLZidxgSXHdFno'
CONSUMER_SECRET = 'JmgS5lUfUT0ZrB36hYQJ5cOINpuM4lOEnbBXwESAefVOGslJG8'
ACCESS_TOKEN = '737403682111643648-PIeyxkm7XPj9ARta66Ly6AQJGQJPEz3'
ACCESS_SECRET = 'yy8qFkJ0TJhmx6DrfVs4FWneBwdyqxVRq2gfxGTZ0CtrL'

t_api = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

#Weather API Key/calls
k = "e8b29a056adebaa04d8f733f3a82897f"
response = requests.get('http://api.openweathermap.org/data/2.5/forecast/daily?q=Dallas&cnt=2&APPID='+k).json()

#Obtaining the appropriate data drom the weather api response
today = response['cnt']-1
r_day_list = response['list']
r_tod = r_day_list[today]
r_tod_dt = r_tod['dt']

x = random.randint(10,50)
x = int(round(x/10))

path = "/home/pi/Weather\ Gifs/hot" + str(x) + ".gif"
gif = open(path, 'rb')
response = t_api.upload_media(media=gif)
# t_api.update_status(status="Today is " + str(datetime.datetime.fromtimestamp(t_tod_dt)))

t_api.update_status(media_ids=[response['media_ids']])
