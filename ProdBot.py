import sys
import random

#Weather API imports
import requests
from datetime import datetime, time

#Twitter API imports
from twython import Twython

# Twitter Keys/API
CONSUMER_KEY = 'lygeb5MmWPyTLZidxgSXHdFno'
CONSUMER_SECRET = 'JmgS5lUfUT0ZrB36hYQJ5cOINpuM4lOEnbBXwESAefVOGslJG8'
ACCESS_TOKEN = '737403682111643648-PIeyxkm7XPj9ARta66Ly6AQJGQJPEz3'
ACCESS_SECRET = 'yy8qFkJ0TJhmx6DrfVs4FWneBwdyqxVRq2gfxGTZ0CtrL'

t_api = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

print datetime.now()

#Weather API Key/calls
key = "e8b29a056adebaa04d8f733f3a82897f"
response = requests.get('http://api.openweathermap.org/data/2.5/forecast/daily?q=Dallas&cnt=2&APPID='+key).json()

#Obtaining the appropriate data drom the weather api response
today = response['cnt']-1
r_day_list = response['list']
r_tod = r_day_list[today]

gif_choice = random.randint(10,50)
gif_choice = int(round(gif_choice/10))
print "Gif number: " + str(gif_choice)

tod_weather_id = r_tod['weather'][0]['id']
print "Today's weather ID: " + str(tod_weather_id)

clear_sky = 800
few_clouds = 801
xtreme = {'900': 'tornado',
          '901': 'tropical storm',
          '902': 'hurricane',
          '906': 'hail',
          '961': 'violent storm',
          '962': 'hurricane'
          }

current_forecast = requests.get('http://api.openweathermap.org/data/2.5/weather?zip=76248,us&APPID='+key)

now = datetime.now().time()
sch_upper_end = time(7, 05)
sch_lower_end = time(6, 55)

if sch_upper_end <= now or now <= sch_lower_end:
    if str(current_forecast) in xtreme or str(tod_weather_id) in xtreme:
          t_api.update_status(status="ALERT: Extreme weather in your area, seek shelter and adhere to your local news network.")


if tod_weather_id == clear_sky or tod_weather_id == few_clouds:
    tod_temp_k = r_tod['temp']['day']
    tod_temp_f = 1.8*(tod_temp_k-273.15)+32

    if tod_temp_f >= 85:
        path = "/home/pi/Weather\ Gifs/hot/hot" + str(gif_choice) + ".gif"
    elif tod_temp_f <= 84 and tod_temp_f >= 60:
        path = "/home/pi/Weather\ Gifs/nice_day/nice" + str(gif_choice) + ".gif"
    elif tod_temp_f < 60:
        path = "/home/pi/Weather\ Gifs/cold/cold" + str(gif_choice) + ".gif"
elif tod_weather_id > 200 and tod_weather_id < 600:
    path = "/home/pi/Weather\ Gifs/rainy/rainy" + str(gif_choice) + ".gif"
elif tod_weather_id < 700 and tod_weather_id >= 600:
    path = "/home/pi/Weather\ Gifs/snowy/snowy" + str(gif_choice) + ".gif"
elif tod_weather_id <= 804 and tod_weather_id >= 802:
    path = "/home/pi/Weather\ Gifs/cloudy/cloudy" + str(gif_choice) + ".gif"
else:
    path = None
    t_api.update_status(status="No gif today folks, check back tomorrow for a new one!")

if path:
    gif = open(path, 'rb')
    response = t_api.upload_media(media=gif)

    t_api.update_status(media_ids=[response['media_id']])
