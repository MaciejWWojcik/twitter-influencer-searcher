import json

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tweetguru.settings")
import django
django.setup()

from twitter_request_client import getTwitterRequestClient
from depth_search_engine import DepthSearchEngine
from tweetguru.models import Tweet


def downloadLastWeekTweets(search_query, count):
    url = 'https://api.twitter.com/1.1/search/tweets.json?q=' + search_query + '&count=' + str(count);
    client = getTwitterRequestClient()
    resp, content = client.request(url, method="GET")
    return content


def save(content, tag):
    jsonContent = json.loads(content)
    tweets = jsonContent["statuses"]
    # pth = os.path.abspath(os.path.dirname(__file__))
    for tweet in tweets:
        dbTweet = Tweet()
        dbTweet.tweetId = tweet['id']
        dbTweet.date = tweet['created_at']
        dbTweet.text = tweet['text']
        dbTweet.userId = tweet['user']['id']
        dbTweet.save()
        print(dbTweet.toString())


# Example of usage
# content = downloadLastWeekTweets('tesla',50)
# search_query is a string
# count takes values between 1-100

tag = 'tesla'
amount = 10

content = downloadLastWeekTweets(tag, amount)
save(content, tag)
engine = DepthSearchEngine(tag, content)
engine.loadAuthorsTweets()
# engine.loadMentionedUsersTweets()
