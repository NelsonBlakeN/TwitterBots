import sys
sys.path.append("/home/pi/Bots")
import random
import logging

#Weather API imports
import requests
from datetime import datetime, time

#Twitter API imports and objects
from TwitterLib import WeatherTwitter
twitter = WeatherTwitter()

# Logging tool (setup)
current_year = datetime.now().isocalendar()[0]
current_week = datetime.now().isocalendar()[1]
FILENAME = '/home/pi/Documents/logs/WeatherBotLogs/'+str(current_year)+'Week'+str(current_week)+'.log'
logging.basicConfig(filename=FILENAME, level=logging.INFO)

logger = logging.getLogger('WeatherGifBot')

#Weather API Key/calls
key = "e8b29a056adebaa04d8f733f3a82897f"    # API Key
# Multiday, daily weather forecast request (city=Dallas, # of days=2)
response =
requests.get('http://api.openweathermap.org/data/2.5/forecast/daily?q=bryan&cnt=2&APPID='+key).json()

#Obtaining the appropriate data drom the weather api response
today = response['cnt']-1                       # Index of desired day (today)
list_of_forecasts = response['list']            # List of forecasted days
forecast = list_of_forecasts[today]             # Forecast of desired day

gif_choice = random.randint(1,14)               # Random gif for the forecast

tod_weather_id = forecast['weather'][0]['id']   # Today's weather ID (categorizes weather)

# Define some weather IDs
clear_sky = 800
few_clouds = 801
xtreme = {'900': 'tornado',
        '901': 'tropical storm',
        '902': 'hurricane',
        '906': 'hail',
        '961': 'violent storm',
        '962': 'hurricane'
        }

# Obtain current forecast (in case of emergency weather)
current_forecast =
requests.get('http://api.openweathermap.org/data/2.5/weather?zip=77840,us&APPID='+key)

# Obtain current time and define non-emergency schedule
now = datetime.now().time()
sch_upper_end = time(7, 05)
sch_lower_end = time(6, 55)

# If outisde non-emergnecy schedule, check for emergency weather
if now >= sch_upper_end or now <= sch_lower_end:
    if str(current_forecast) in xtreme or str(tod_weather_id) in xtreme:
        twitter.post_tweet(text="ALERT: Extreme weather in your area, seek shelter and adhere to your local news network.")

# Non-emergency schedule
else:
    # Logging data
    logger.info('Today is ' + str(datetime.now()))
    logger.info("Gif number: " + str(gif_choice))
    logger.info("Today's weather ID: " + str(tod_weather_id))

    # Determine weather category based on temperature
    if tod_weather_id == clear_sky or tod_weather_id == few_clouds:
        tod_temp_k = forecast['temp']['day']        # Today's temperature (Kelvin)
        tod_temp_f = 1.8*(tod_temp_k-273.15)+32     # Convert kelvin to Fahrenheit

        if tod_temp_f >= 85:
            logger.info("HOT")
            path = "/home/pi/WeatherGifs/hot/hot" + str(gif_choice) + ".gif"
        elif tod_temp_f <= 84 and tod_temp_f >= 60:
            logger.info("NICE DAY")
            gif_choice = random.randint(1,11)	# There are 11 nice day gifs, so we reroll the choice
            path = "/home/pi/WeatherGifs/nice_day/nice" + str(gif_choice) + ".gif"
        elif tod_temp_f < 60:
            logger.info("COLD")
            path = "/home/pi/WeatherGifs/cold/cold" + str(gif_choice) + ".gif"

    # Determine weather category based on weather ID
    elif tod_weather_id > 200 and tod_weather_id < 600:
        logger.info("RAINY")
        gif_choice = random.randint(1,12) # Due to size issues with some gifs, reroll
        path = "/home/pi/WeatherGifs/rainy/rainy" + str(gif_choice) + ".gif"
    elif tod_weaher_id < 700 and tod_weather_id >= 600:
        logger.info("SNOWY")
        path = "/home/pi/WeatherGifs/snowy/snowy" + str(gif_choice) + ".gif"
    elif tod_weather_id <= 804 and tod_weather_id >= 802:
        logger.info("CLOUDY")
        gif_choice = random.randint(2, 11) # Some gifs were removed due to media limits. Rerolling without renaming gifs
        path = "/home/pi/WeatherGifs/cloudy/cloudy" + str(gif_choice) + ".gif"
    else:
        # Something went wrong, weather category could not be determined
        path = None
        twitter.post_tweet(text="No gif today folks, check back tomorrow for a new one!")

    if path:
        # Tweet the weather gif
        response = twitter.post_tweet(media=path, logger=logger)
        if response is not None:
            logger.error(response)

    logger.info("\n \n ************************** \n")
