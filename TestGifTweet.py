import sys
from twython import Twython

CONSUMER_KEY = 'lygeb5MmWPyTLZidxgSXHdFno'
CONSUMER_SECRET = 'JmgS5lUfUT0ZrB36hYQJ5cOINpuM4lOEnbBXwESAefVOGslJG8'
ACCESS_TOKEN = '737403682111643648-PIeyxkm7XPj9ARta66Ly6AQJGQJPEz3'
ACCESS_SECRET = 'yy8qFkJ0TJhmx6DrfVs4FWneBwdyqxVRq2gfxGTZ0CtrL'

api = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

gif = open('/home/pi/freeze.gif', 'rb')
response = api.upload_media(media=gif)

api.update_status(status='Checkout this cool image!', media_ids=[response['media_id']])