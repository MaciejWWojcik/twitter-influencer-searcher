import json

from crawler.twitter_request_client import getTwitterRequestClient
from tweetguru.models import Tweet, TweetAuthor, Hashtag, UserMention, SearchResult


def downloadLastWeekTweets(search_query, count):
    url = 'https://api.twitter.com/1.1/search/tweets.json?q=' + search_query + '&count=' + str(count);
    client = getTwitterRequestClient()
    resp, content = client.request(url, method="GET")
    return content


def save(tweets, tag):
    for tweet in tweets:
        tweetId = tweet["id"]
        existingTweet = Tweet.objects.filter(twitterContentId=tweetId).first()
        if existingTweet is None:
            tweetUser = tweet['user']
            existingUser = TweetAuthor.objects.filter(twitterUserId=tweetUser['id']).first()
            if existingUser is None:

                userToSave = TweetAuthor(twitterUserId=tweetUser['id'],
                                         name=tweetUser['screen_name'],
                                         fullName=tweetUser['name'].encode('unicode_escape'),
                                         followersCount=tweetUser['followers_count'],
                                         friendsCount=tweetUser['friends_count'])
                userToSave.save()
                existingUser = userToSave
            tweetToSave = Tweet(twitterContentId=tweetId,
                                date=tweet['created_at'],
                                text=tweet['text'].encode('unicode_escape'),
                                user=existingUser)
            tweetToSave.save()
            existingTweet = tweetToSave
            for hashtag in tweet['entities']['hashtags']:
                hashtagToSave = Hashtag(tweet=tweetToSave, value=hashtag['text'].encode('unicode_escape'))
                hashtagToSave.save()
            for user in tweet['entities']['user_mentions']:
                userFromDb = TweetAuthor.objects.filter(twitterUserId=user['id']).first()
                if userFromDb is None:
                    url = 'https://api.twitter.com/1.1/users/show.json?user_id=' + str(user['id'])
                    client = getTwitterRequestClient()
                    resp, content = client.request(url, method="GET")
                    userDetails = json.loads(content)
                    mentionedUserToSave = TweetAuthor(twitterUserId=userDetails['id'],
                                                      name=userDetails['screen_name'],
                                                      fullName=userDetails['name'].encode('unicode_escape'),
                                                      followersCount=userDetails['followers_count'],
                                                      friendsCount=userDetails['friends_count'])
                    mentionedUserToSave.save()
                    userFromDb = mentionedUserToSave
                mention = UserMention(tweet=tweetToSave, user=userFromDb)
                mention.save()
            existingSearchResult = SearchResult.objects.filter(tweetId_id=existingTweet.id, tag=tag).first()
            if existingSearchResult is None:
                searchResultToSave = SearchResult(tweetId_id=existingTweet.id, tag=tag)
                searchResultToSave.save()

# Example of usage
# content = downloadLastWeekTweets('tesla',50)
# search_query is a string
# count takes values between 1-100