import json
import os

from crawler.depth_search_engine import DepthSearchEngine
from crawler.tweet import Tweet
from crawler.twitter_request_client import getTwitterRequestClient


def downloadLastWeekTweets(search_query, count):
    url = 'https://api.twitter.com/1.1/search/tweets.json?q=' + search_query + '&count=' + str(count);
    client = getTwitterRequestClient()
    resp, content = client.request(url, method="GET")
    return content


def save(content, tag):
    jsonContent = json.loads(content)
    tweets = jsonContent["statuses"]
    pth = os.path.abspath(os.path.dirname(__file__))
    for tweet in tweets:
        tweetId = tweet["id"]
        filePath = pth + '/logs/' + tag + '_' + str(tweetId) + '.json'
        file = open(filePath, 'w+')
        data = Tweet(tweet)
        file.write(json.dumps(data.toJSON()))
        file.close()
        print(data.toJSON())


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
