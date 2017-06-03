import simplejson
import twitter_creds as twit_c
import twilio_creds as twil_c

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
    old_count = old_follow_count()
    if old_count is None:
        old_count = 0
    current_count = current_follow_count()
    diff = current_count - old_count

    missing_people = list(set(current_follow_list).symmetric_difference(old_follow_list))
    send_alert(diff, missing_people)

    # Get writable string from list of IDs
    current_list_str = " ".join(map(str, current_follow_list))

    with open(filename, 'w') as hist_file:
        hist_file.truncate()
        hist_file.write(str(current_count)) # Save follow count
        hist_file.write("\n")               # New line
        hist_file.write(current_list_str)   # Save list of followers (IDs)

def old_follow_count():
    hist_file = open(filename, 'r')
    oc = int(hist_file.readline())

    #Getting a list of IDs from a string
    global old_follow_list
    old_follow_list = map(int, hist_file.readline().split(" "))

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
        body = "Blake, you lost " + str(abs(diff)) + " follower"
    elif diff > 0:
        body = "Blake, you gained " + str(diff) + " follower"

    if abs(diff) == 1:
        body = body+". It was "
    elif diff != 0:
        # Ensures an alert is only sent if there is a change.
        body = body + "s today.\n\nThey were:\n"

    for u in user_ids:
        name = get_name(u)
        body = body + name
        if name:
            body += "\n";

    if diff is not 0:
        message = twilio.messages.create(body=body, from_=MY_TWIL_NUM, to=MY_CELL_NUM)

def get_name(user_id):
    response, data = twitter.request("https://api.twitter.com/1.1/users/show.json?user_id="+str(user_id))
    screen_name = json_data(data, "screen_name")
    name = "* " + json_data(data, "name")

    if screen_name:
        name += " (@" + screen_name + ")"
    return name

def json_data(data, index):
    try:
        data_dict = simplejson.loads(data);
        return data_dict[index]
    except KeyError, e:
        return ""


if __name__ == "__main__":
    main()
