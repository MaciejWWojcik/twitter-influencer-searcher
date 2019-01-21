
from tweetguru.models import TweetAuthor, UserRank, UserMention, Tweet


def rank_topic(topicId):
    relevant_tweets = Tweet.objects.filter(topicId=topicId)
    UserRank.objects.filter(topicId=topicId).delete()
    for tweet in relevant_tweets:
        userRank = UserRank.objects.filter(userId=tweet.user, topicId=topicId)
        if userRank:
            userRank.tweetsCount += 1
            userRank.retweetsCount += tweet.retweetsCount
            userRank.likesCount += tweet.likesCount

        else:
            userRank = UserRank()
            userRank.topicId = topicId
            userRank.userId = tweet.user
            userRank.followersCount = TweetAuthor.objects.filter(id=tweet.user).followersCount
            userRank.tweetsCount = 1
            userRank.retweetsCount = tweet.retweetsCount
            userRank.likesCount = tweet.likesCount
            userRank.mentionsCount = 0

        userRank.save()
        userRank.save()

    mentions = UserMention.objects.filter(topicId=topicId);
    for mention in mentions:
        rank = userRank.objects.filter(topicId=topicId, userId=mention.userId)
        rank.mentionsCount += 1
        rank.save()
