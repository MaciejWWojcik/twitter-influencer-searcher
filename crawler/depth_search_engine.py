import os
import json
from tguru.settings import BASE_DIR
from crawler.twitter_request_client import getTwitterRequestClient
from crawler.tweet import Tweet
import pathlib

def load_file():
    tweetFile = open(os.path.join(BASE_DIR, 'tweetguru', 'depth_search', 'sample-tweet.json'))
    tweet = json.load(tweetFile)

    tweetFile.close()
    return tweet


def loadFiles():
    logs = [f for f in os.listdir('../logs/') if os.path.isfile(os.path.join('../logs/', f))]

class DepthSearchEngine:
    tweets_count = 10
    tag = ''
    tweets = []
    requestUrl = "https://api.twitter.com/1.1/statuses/user_timeline.json"

    def __init__(self, tag, requestContent):
        self.tag = tag
        jsonContent = json.loads(requestContent)
        self.tweets = jsonContent["statuses"]
        print("Loaded " + str(len(self.tweets)) + " tweets to depth search engine")

    def loadAuthorsTweets(self):
        for index, tweet in enumerate(self.tweets):
            print("Loading author from tweet " + str(index+1) + " out of " + str(len(self.tweets)))
            userId = tweet['user']['id']
            timelineUrl = self.requestUrl + "?count=" + str(self.tweets_count) + "&user_id=" + str(userId)
            client = getTwitterRequestClient()
            resp, content = client.request(timelineUrl, method="GET")
            self.saveAuthorsTweets(content, self.tag)

    def loadMentionedUsersTweets(self):
        for index, rawTweet in enumerate(self.tweets):
            tweet = Tweet(rawTweet)
            print("Loading mentioned authors from tweet " + str(index + 1) + " out of " + str(len(self.tweets)))
            print(len(tweet.usersMentions))
            for mentionedIndex, mentionedUser in enumerate(tweet.usersMentions):
                print("Loading mentioned author " + str(mentionedIndex + 1) + " out of " + str(len(tweet.usersMentions)))
                mentionedUserId = mentionedUser.id
                print(mentionedUserId)
                timelineUrl = self.requestUrl + "?count=" + str(self.tweets_count) + "&user_id=" + str(mentionedUserId)
                client = getTwitterRequestClient()
                resp, content = client.request(timelineUrl, method="GET")
                self.saveAuthorsTweets(content, self.tag)


    def saveAuthorsTweets(self, content, tag):
        tweets = json.loads(content)

        for tweet in tweets:
            tweetId = tweet["id"]
            authorId = tweet["user"]["id"]
            authorDirectoryPath = '../logs/' + tag + "_user_" + str(authorId) + "/"
            if not os.path.exists(authorDirectoryPath):
                pathlib.Path(authorDirectoryPath).mkdir(parents=True, exist_ok=True)
            filePath = authorDirectoryPath + tag + '_' + str(tweetId) + '.json'
            if not os.path.isfile(filePath):
                file = open(filePath, 'w+')
                data = Tweet(tweet)
                file.write(json.dumps(data.toJSON()))
                file.close()
