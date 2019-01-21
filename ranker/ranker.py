
from tweetguru.models import TweetAuthor, UserRank, UserMention, Tweet, SearchResult


def rank_topic(topicId):
    relevant_tweets = []
    # TODO zamienić topicId na tag jako string
    tag_search_results = SearchResult.objects.filter(tag=topicId)
    for result in tag_search_results:
        relevant_tweets.append(result.tweet)
    UserRank.objects.filter(topic_id=topicId).delete()
    for tweet in relevant_tweets:
        userRank = UserRank.objects.filter(user_id=tweet.user, topic_id=topicId)
        if userRank:
            userRank.tweetsCount += 1
            userRank.retweetsCount += tweet.retweetsCount
            userRank.likesCount += tweet.likesCount

        else:
            userRank = UserRank()
            userRank.topicId = topicId
            userRank.userId = tweet.user
            userRank.followersCount = TweetAuthor.objects.filter(id=tweet.user.id).followersCount
            userRank.tweetsCount = 1
            userRank.retweetsCount = tweet.retweetsCount
            userRank.likesCount = tweet.likesCount
            userRank.mentionsCount = 0

        userRank.save()
        userRank.save()

    # mentions = UserMention.objects.filter(topic_id=topicId)
    # for mention in mentions:
    #     rank = userRank.objects.filter(topic_id=topicId, user_id=mention.userId)
    #     rank.mentionsCount += 1
    #     rank.save()
