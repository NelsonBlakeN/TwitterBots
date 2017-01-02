import requests
import oauth2 as oauth
import sys

import json
import pickle

CONSUMER_KEY    = 'lygeb5MmWPyTLZidxgSXHdFno'
CONSUMER_SECRET = 'JmgS5lUfUT0ZrB36hYQJ5cOINpuM4lOEnbBXwESAefVOGslJG8'
ACCESS_TOKEN    = '737403682111643648-PIeyxkm7XPj9ARta66Ly6AQJGQJPEz3'
ACCESS_SECRET   = 'yy8qFkJ0TJhmx6DrfVs4FWneBwdyqxVRq2gfxGTZ0CtrL'

consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
access_token = oauth.Token(key=ACCESS_TOKEN, secret=ACCESS_SECRET)
client = oauth.Client(consumer, access_token)

newfile = 'mypickle.pk'

# response, data = client.request("https://api.twitter.com/1.1/followers/ids.json?cursor=-1&screen_name=frostedbIakes&count=5000")
# # Convert 'data' from string to dictionary
# json_string = data.replace("'", "\"")
# d = json.loads(json_string)

# print "Followers: ", len(d['ids'])

def old_follow_count():
    file = open(newfile, 'w+b')
    # with open(newfile, 'rb') as fi:
    #     old_count = pickle.load(fi)
    # oc = pickle.load(open(newfile, 'rb'))
    oc = pickle.load(file)
    return oc

def current_follow_count():
    response, data = client.request("https://api.twitter.com/1.1/followers/ids.json?cursor=-1&screen_name=frostedbIakes&count=5000")
    # Convert 'data' from string to dictionary
    json_string = data.replace("'", "\"")
    d = json.loads(json_string)

    c = len(d['ids'])
    return c

old_count = old_follow_count()
if old_count is None:
    old_count = 0;
current_count = current_follow_count()
diff = current_count
if(diff < 0):
    print "You lost ", abs(diff), " followers!"
elif(diff > 0):
    print "You gained", diff, " followers!"
else:
    print "No change"

with open(newfile, 'wb') as fi:
    pickle.dump(current_count, fi)


