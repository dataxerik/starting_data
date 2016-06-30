import json
from twython import Twython

with open("credentials.json") as f:
    credentials = json.load(f)

twitter = Twython(credentials['consumer_key'], credentials['consumer_secret'])

for status in twitter.search(q='"data_science"')["statuses"]:
    user = status['user']['screen_name'].encode('utf-8')
    text = status['text'].encode('utf-8')
    print("{} : {}".format(user, text))
    print()