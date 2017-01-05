import requests
import oauth2 as oauth
import json

from twilio.rest import TwilioRestClient

# Twitter API requirements
CONSUMER_KEY    = 'lygeb5MmWPyTLZidxgSXHdFno'
CONSUMER_SECRET = 'JmgS5lUfUT0ZrB36hYQJ5cOINpuM4lOEnbBXwESAefVOGslJG8'
ACCESS_TOKEN    = '737403682111643648-PIeyxkm7XPj9ARta66Ly6AQJGQJPEz3'
ACCESS_SECRET   = 'yy8qFkJ0TJhmx6DrfVs4FWneBwdyqxVRq2gfxGTZ0CtrL'

# Twilio API Requirements
ACCOUNT_SID = 'ACe9a7f6ee6de1a5aa66fb68c386ec530f'
AUTH_TOKEN  = '9be322a9d2603be029567bd0c2dee7b4'
twilio_client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
MY_TWIL_NUM = "+18177765044"
MY_CELL_NUM = "+18173419172"

consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
access_token = oauth.Token(key=ACCESS_TOKEN, secret=ACCESS_SECRET)
client = oauth.Client(consumer, access_token)

newfile = 'old_follow_count.txt'

def old_follow_count():
    file = open(newfile, 'r')
    return int(file.readline())

def current_follow_count():
    response, data = client.request("https://api.twitter.com/1.1/followers/ids.json?cursor=-1&screen_name=frostedbIakes&count=5000")
    # Convert 'data' from string to dictionary
    json_string = data.replace("'", "\"")
    d = json.loads(json_string)

    c = len(d['ids'])
    return c

def send_alert(d):
    if(d < 0):
        body = "Blake - You lost " + str(abs(d)) + " followers today."
    elif(d > 0):
        body = "Blake - You gained " + str(d) + " followers today."
    message = twilio_client.messages.create(body=body, from_=MY_TWIL_NUM, to=MY_CELL_NUM)

old_count = old_follow_count()
if old_count is None:
    old_count = 0;
current_count = current_follow_count()
diff = current_count - old_count

send_alert(diff)

with open(newfile, 'w') as f:
    f.truncate()
    f.write(str(current_count))
