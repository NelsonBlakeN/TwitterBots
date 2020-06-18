import json
import oauth2 as oauth
import requests
import simplejson
import sys
from pprint import pprint

def json_data(data, index=None):
	# Converts data string into a dictionary, and returns the desired entry
	try:
		data_dict = simplejson.loads(data)
		if index is not None:
			return data_dict[index]
		else:
			return data_dict
	except KeyError as e:
		return ""

class PersonalTwitter:

	# Constructor
	def __init__(self):
		keys = json.load("TwitterKeys.json");
		CONSUMER_KEY = keys["personal_keys"]["key"]
		CONSUMER_SECRET = keys["personal_keys"]["secret"]
		ACCESS_TOKEN = ACCESS_TOKEN_PT
		ACCESS_SECRET = ACCESS_SECRET_PT

		consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
		access_token = oauth.Token(key=ACCESS_TOKEN, secret=ACCESS_SECRET)
		self.client = oauth.Client(consumer, access_token)

	# Get current follower count and list of followers
	def get_followers(self):
		response, data = self.client.request("https://api.twitter.com/1.1/followers/ids.json?cursor=-1&screen_name=frostedbIakes&count=5000")

		# Convert 'data' from string to dictionary
		current_follow_list = json_data(data, "ids")
		follower_count = len(current_follow_list)
		return follower_count, current_follow_list

	# Returns the @ name (screen name) and user name of the given user
	def get_user_name(self, user_id):
		response, data = self.client.request("https://api.twitter.com/1.1/users/show.json?user_id="+str(user_id))
		screen_name = json_data(data, "screen_name")
		name = json_data(data, "name")

		return (screen_name, name)

class WeatherTwitter:

	# Constructor
	def __init__(self):
		CONSUMER_KEY = CONSUMER_KEY_WT
		CONSUMER_SECRET = CONSUMER_KEY_WT
		ACCESS_TOKEN = ACCESS_TOKEN_WT
		ACCESS_SECRET = ACCESS_SECRET_WT

		consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
		access_token = oauth.Token(key=ACCESS_TOKEN, secret=ACCESS_SECRET)
		self.client = oauth.Client(consumer, access_token)
