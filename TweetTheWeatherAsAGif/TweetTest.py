import sys
from twython import Twython

tweetStr = "RIP Nasim Osman, 63, Bangladeshi politician, MP for Narayanganj (1986-1991, since 2008)."

CONSUMER_KEY = 'lygeb5MmWPyTLZidxgSXHdFno'
CONSUMER_SECRET = 'JmgS5lUfUT0ZrB36hYQJ5cOINpuM4lOEnbBXwESAefVOGslJG8'
ACCESS_TOKEN = '737403682111643648-PIeyxkm7XPj9ARta66Ly6AQJGQJPEz3'
ACCESS_SECRET = 'yy8qFkJ0TJhmx6DrfVs4FWneBwdyqxVRq2gfxGTZ0CtrL'

api = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

api.update_status(status = tweetStr)
