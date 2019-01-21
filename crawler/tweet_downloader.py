import json

from crawler.depth_search_engine import DepthSearchEngine
from crawler.twitter_request_client import getTwitterRequestClient
from tweetguru.models import Tweet, TweetAuthor, Hashtag, UserMention


def downloadLastWeekTweets(search_query, count):
    url = 'https://api.twitter.com/1.1/search/tweets.json?q=' + search_query + '&count=' + str(count);
    client = getTwitterRequestClient()
    resp, content = client.request(url, method="GET")
    return content


def save(content, tag):
    jsonContent = json.loads(content)
    tweets = jsonContent["statuses"]
    for tweet in tweets:
        tweetId = tweet["id"]
        # TODO save tag that was picked to search
        existingTweet = Tweet.objects.filter(twitterContentId=tweetId)
        if len(existingTweet) == 0:
            tweetUser = tweet['user']
            existingUser = TweetAuthor.objects.filter(twitterUserId=tweetUser['id'])
            if len(existingUser) == 0:
                userToSave = TweetAuthor(twitterUserId=tweetUser['id'],
                                         name=tweetUser['screen_name'],
                                         fullName=tweetUser['name'],
                                         followersCount=tweetUser['followers_count'],
                                         friendsCount=tweetUser['friends_count'])
                print(tweetUser['id'])
                userToSave.save()
                existingUser = userToSave
            tweetToSave = Tweet(twitterContentId=tweetId, date=tweet['created_at'], text=tweet['text'], user=existingUser)
            tweetToSave.save()

            for hashtag in tweet['entities']['hashtags']:
                hashtagToSave = Hashtag(tweetId=tweetToSave, value=hashtag['text'])
                hashtagToSave.save()
            for user in tweet['entities']['user_mentions']:
                userFromDb = TweetAuthor.objects.filter(twitterUserId=user['id'])
                if userFromDb is None:
                    mentionedUserToSave = TweetAuthor(twitterUserId=user['id'],
                                                      name=user['screen_name'],
                                                      fullName=user['name'],
                                                      followersCount=user['followers_count'],
                                                      friendsCount=user['friends_count'])
                    mentionedUserToSave.save()
                    userFromDb = mentionedUserToSave
                mention = UserMention(tweetId=tweetToSave, userId=userFromDb)
                mention.save()


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
