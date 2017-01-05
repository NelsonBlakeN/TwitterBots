import requests
import oauth2 as oauth
import json
import twitter_creds as twit_c
import twilio_creds as twil_c
from itertools import islice

# Twitter API object
twitter = twit_c.client

# Twilio API Requirements
twilio = twil_c.client
MY_TWIL_NUM = twil_c.MY_TWIL_NUM
MY_CELL_NUM = twil_c.MY_CELL_NUM

filename = 'old_follow_count.txt'
old_follow_list = []
current_follow_list = []

def main():
    global current_follow_list, old_follow_list

    old_count = old_follow_count()
    if old_count is None:
        old_count = 0;
    current_count = current_follow_count()
    diff = current_count - old_count

    missing_people = list(set(current_follow_list).symmetric_difference(old_follow_list))
    print missing_people
    send_alert(diff, missing_people)

    # Get writable string from list of IDs
    current_list_str = " ".join(map(str, current_follow_list))

    with open(filename, 'w') as f:
        f.truncate()
        f.write(str(current_count)) # Save follow count
        f.write("\n")               # New line
        f.write(current_list_str)   # Save list of followers (IDs)

def old_follow_count():
    file = open(filename, 'r')
    oc = int(file.readline())

    #Getting a list of IDs from a string
    global old_follow_list
    old_follow_list = map(int, file.readline().split(" "))

    return oc

def current_follow_count():
    response, data = twitter.request("https://api.twitter.com/1.1/followers/ids.json?cursor=-1&screen_name=frostedbIakes&count=5000")

    # Convert 'data' from string to dictionary
    global current_follow_list
    current_follow_list = json_data(data, "ids")
    c = len(current_follow_list)
    return c

def send_alert(diff, user_ids):
    print "Sending alert; diff is", diff, "and users are", user_ids
    if diff < 0:
        body = "Blake - You lost " + str(abs(diff)) + " follower"
    elif diff > 0:
        body = "Blake - You gained " + str(diff) + " follower"

    if abs(diff) == 1:
        body = body+" today. It was "
    elif diff != 0:
        print "Sending alert"
        # Ensures an alert is only sent if there is a change.
        body = body + "s today.\n\nThey were:\n"

    for u in user_ids:
        name = get_name(u)
        body = body + name + "\n"

    if diff is not 0:
        message = twilio.messages.create(body=body, from_=MY_TWIL_NUM, to=MY_CELL_NUM)

def get_name(user_id):
    response, data = twitter.request("https://api.twitter.com/1.1/users/show.json?user_id="+str(user_id))
    screen_name = json_data(data, "screen_name")
    name = json_data(data, "name")

    return name + " (" + screen_name + ")"

def json_data(data, index):
    json_string = data.replace("'", "\"")
    d = json.loads(json_string)
    return d[index]


if __name__ == "__main__":
    main()