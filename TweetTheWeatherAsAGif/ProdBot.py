try:
    import logging
    import sys
except Exception as e:
    print("ERROR sys/logging import failed: {}".format(e))

# Set up logging tool
current_year = datetime.now().isocalendar()[0]
current_week = datetime.now().isocalendar()[1]
FILENAME = '/home/pi/Documents/logs/WeatherBotLogs/'+str(current_year)+'Week'+str(current_week)+'.log'
logging.basicConfig(filename=FILENAME, level=logging.INFO)

logger = logging.getLogger('WeatherGifBot')

try:
    sys.path.append("/home/pi/Bots")
    import random

    #Weather API imports
    import requests
    from datetime import datetime, time

    #Twitter API imports
    from TwitterLib import WeatherTwitter

except Exception as e:
    logger.error("Import failed: {}".format(e))

# Define constants
SEPARATOR = "\n \n ************************** \n"
WEATHER_KEY = "e8b29a056adebaa04d8f733f3a82897f"    # API key
XTREME_ALERT = "ALERT: Extreme weather in your area, seek shelter and adhere to your local news network."
CURRENT_FORECAST_URL = 'http://api.openweathermap.org/data/2.5/forecast/daily?q=bryan&cnt=2&APPID='

CLEAR_SKY = 800     # Weather API code for a clear sky in forecast
FEW_CLOUDS = 801    # Weather API code for some clouds in forecast

HOT_PATH = "/home/pi/WeatherGifs/hot/hot"               # Path to "hot" gifs
NICE_DAY_PATH = "/home/pi/WeatherGifs/nice_day/nice"    # Path to "nice day" gifs
COLD_PATH = "/home/pi/WeatherGifs/cold/cold"            # Path to "cold" gifs
RAINY_PATH = "/home/pi/WeatherGifs/rainy/rainy"         # Path to "rainy" gifs
SNOWY_PATH = "/home/pi/WeatherGifs/snowy/snowy"         # Path to "snowy" gifs
CLOUDY_PATH = "/home/pi/WeatherGifs/cloudy/cloudy"      # Path to "cloudy" gifs

# Helper functions
def terminate(msg=None, e=None):
    logging.error(msg.format(e))
    logging.error("Exiting.")
    logging.info(SEPARATOR)
    sys.exit()

# Create necessary objects
try:
    twitter = WeatherTwitter()
    # TODO: Adapt this to use the library (on pi)

except Exception as e:
    terminate("Failed to create necessary objects: {}", e)

#Weather API Key/calls
try:
    # Multiday, daily weather forecast request (city=Bryan, # of days=2)
    response = requests.get(CURRENT_FORECAST_URL+key).json()
except Exception as e:
    terminate("Failed to make weather API calls: {}", e)

#Obtaining the appropriate data drom the weather api response
today = response['cnt']-1                       # Index of desired day (today)
list_of_forecasts = response['list']            # List of forecasted days
forecast = list_of_forecasts[today]             # Forecast of desired day

gif_choice = random.randint(1,14)               # Random gif for the forecast

tod_weather_id = forecast['weather'][0]['id']   # Today's weather ID (categorizes weather)

# Define extreme weather IDs
xtreme = {'900': 'tornado',
        '901': 'tropical storm',
        '902': 'hurricane',
        '906': 'hail',
        '961': 'violent storm',
        '962': 'hurricane'
        }

# Obtain current forecast (in case of emergency weather)
try:
    current_forecast = requests.get('http://api.openweathermap.org/data/2.5/weather?zip=77840,us&APPID='+key)
except Exception as e:
    logging.error("Current forcast request failed: {}".format(e))
    logging.info("Continuing.")

# Obtain current time and define non-emergency schedule
# TODO: Change time() to constants
now = datetime.now().time()
sch_upper_end = time(7, 05)
sch_lower_end = time(6, 55)

# If outisde non-emergnecy schedule, check for emergency weather
if now >= sch_upper_end or now <= sch_lower_end:
    # If current forecast failed, this should not through an error (str(None)=='None')
    if str(current_forecast) in xtreme or str(tod_weather_id) in xtreme:
        twitter.post_tweet(text=XTREME_ALERT)

# Non-emergency schedule
else:
    # Logging data
    logger.info('Today is ' + str(datetime.now()))
    logger.info("Gif number: " + str(gif_choice))
    logger.info("Today's weather ID: " + str(tod_weather_id))

    # Determine weather category based on temperature
    # TODO: Remove magic numbers (temps, API codes)
    if tod_weather_id == CLEAR_SKY or tod_weather_id == FEW_CLOUDS:
        tod_temp_k = forecast['temp']['day']        # Today's temperature (Kelvin)
        tod_temp_f = 1.8*(tod_temp_k-273.15)+32     # Convert kelvin to Fahrenheit

        if tod_temp_f >= 85:
            logger.info("HOT")
            path = HOT_PATH + str(gif_choice) + ".gif"
        elif tod_temp_f <= 84 and tod_temp_f >= 60:
            logger.info("NICE DAY")
            # There are 11 nice day gifs, so we reroll the choice
            gif_choice = random.randint(1,11)
            path = NICE_DAY_PATH + str(gif_choice) + ".gif"
        elif tod_temp_f < 60:
            logger.info("COLD")
            path = COLD_PATH + str(gif_choice) + ".gif"

    # Determine weather category based on weather ID
    elif tod_weather_id > 200 and tod_weather_id < 600:
        logger.info("RAINY")
        gif_choice = random.randint(1,12) # Due to size issues with some gifs, reroll
        path = RAINY_PATH + str(gif_choice) + ".gif"
    elif tod_weaher_id < 700 and tod_weather_id >= 600:
        logger.info("SNOWY")
        path = SNOWY_PATH + str(gif_choice) + ".gif"
    elif tod_weather_id <= 804 and tod_weather_id >= 802:
        logger.info("CLOUDY")
        gif_choice = random.randint(2, 11) # Some gifs were removed due to media limits. Rerolling without renaming gifs
        path = CLOUDY_PATH + str(gif_choice) + ".gif"
    else:
        # Something went wrong, weather category could not be determined
        path = None
        try:
            twitter.post_tweet(text="No gif today folks, check back tomorrow for a new one!")
        except Exception as e:
            logging.error("Default tweet failed to post: {}".format(e))

    if path:
        # Tweet the weather gif
        response = twitter.post_tweet(media=path, logger=logger)
        if response is not None:
            logger.error(response)

    logger.info(SEPARATOR)
