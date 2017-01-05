import requests
import oauth2 as oauth
import json
import twitter_creds as twit_c
import twilio_creds as twil_c

# Twitter API object
twitter = twit_c.client

# Twilio API Requirements
twilio = twil_c.client
MY_TWIL_NUM = twil_c.MY_TWIL_NUM
MY_CELL_NUM = twil_c.MY_CELL_NUM

newfile = 'old_follow_count.txt'

def main():
    old_count = old_follow_count()
    if old_count is None:
        old_count = 0;
    current_count = current_follow_count()
    diff = current_count - old_count

    send_alert(diff)

    with open(newfile, 'w') as f:
        f.truncate()
        f.write(str(current_count))

def old_follow_count():
    file = open(newfile, 'r')
    return int(file.readline())

def current_follow_count():
    response, data = twitter.request("https://api.twitter.com/1.1/followers/ids.json?cursor=-1&screen_name=frostedbIakes&count=5000")
    # Convert 'data' from string to dictionary
    json_string = data.replace("'", "\"")
    d = json.loads(json_string)

    c = len(d['ids'])
    return c

def send_alert(d):
    if d < 0:
        b = "Blake - You lost " + str(abs(d)) + " followers today."
    elif d > 0:
        b = "Blake - You gained " + str(d) + " followers today."

    # Ensures an alert is only sent if there is a change.
    if d is not 0:
        message = twilio_client.messages.create(body=b, from_=MY_TWIL_NUM, to=MY_CELL_NUM)


if __name__ == "__main__":
    main()