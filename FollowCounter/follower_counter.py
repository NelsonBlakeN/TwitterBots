import requests
import oauth2 as oauth
import json

CONSUMER_KEY    = 'lygeb5MmWPyTLZidxgSXHdFno'
CONSUMER_SECRET = 'JmgS5lUfUT0ZrB36hYQJ5cOINpuM4lOEnbBXwESAefVOGslJG8'
ACCESS_TOKEN    = '737403682111643648-PIeyxkm7XPj9ARta66Ly6AQJGQJPEz3'
ACCESS_SECRET   = 'yy8qFkJ0TJhmx6DrfVs4FWneBwdyqxVRq2gfxGTZ0CtrL'

consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
access_token = oauth.Token(key=ACCESS_TOKEN, secret=ACCESS_SECRET)
client = oauth.Client(consumer, access_token)

newfile = 'old_follow_count.txt'

def old_follow_count():
    file = open(newfile, 'r')
    return file.readline()

def current_follow_count():
    response, data = client.request("https://api.twitter.com/1.1/followers/ids.json?cursor=-1&screen_name=frostedbIakes&count=5000")
    # Convert 'data' from string to dictionary
    json_string = data.replace("'", "\"")
    d = json.loads(json_string)

    c = len(d['ids'])
    return c

print "You have", old_follow_count(), "followers"
old_count = 0
if old_count is None:
    old_count = 0;
current_count = current_follow_count()
diff = current_count - old_count
if(diff < 0):
    print "You lost ", abs(diff), " followers!"
elif(diff > 0):
    print "You gained", diff, "followers!"
else:
    print "No change"

with open(newfile, 'w') as fi:
    print "Writing to file..."
    fi.write(str(current_count))


