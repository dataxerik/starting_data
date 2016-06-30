import json
from twython import TwythonStreamer
from collections import Counter

# appending data to a global variable is bad
# but for simplicity

tweets = []

class MyStreamer(TwythonStreamer):
    """out own subclass of TwythonStreamer that specifies
    how to interact with the stream"""

    def on_success(self, data):
        """What do we do when twitter send us data?
        here data will bea python dict representing a tweet"""

        # Only want to collect English-language tweets
        if data['lang'] == 'en':
            tweets.append(data)
            print("received # {}".format(len(tweets)))

        #stop when we've collected enough
        if len(tweets) >= 1000:
            self.disconnect()

    def on_error(self, status_code, data):
        print("{}, {}".format(status_code, data))
        self.disconnect()

def main():
    with open("credentials.json") as f:
        credentials = json.load(f)
    stream = MyStreamer(credentials["consumer_key"], credentials["consumer_secret"],
                        credentials["access_token"], credentials["access_token_secret"])

    stream.statuses.filter(track='data')

    top_hashtags = Counter(hashtag['text'].lower()
                           for tweet in tweets
                           for hashtag in tweet['entities']['hashtags'])
    print(top_hashtags.most_common(5))


if __name__ == "__main__": main()