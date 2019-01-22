from tweetguru.models import TweetAuthor, UserRank, UserMention, Tweet, SearchResult, Topic


def rank_all():
    print('rank_all')
    topics = Topic.objects.all()
    for topic in topics:
        rank_topic(topic.title)


def rank_topic(topic):
    print('rank_topic', topic)
    tag_search_results = SearchResult.objects.filter(tag=topic)
    topicId = Topic.objects.get(title=topic).id

    for search_result in tag_search_results:
        tweet = Tweet.objects.filter(id=search_result.tweet_id)[0]
        userRanks = UserRank.objects.filter(user_id=tweet.user_id, topic_id=topicId)
        if len(userRanks) > 0:
            userRank = userRanks[0]
            userRank.tweetsCount += 1
            userRank.retweetsCount += tweet.retweetsCount
            userRank.likesCount += tweet.likesCount
            userRank.score = score(userRank.mentionsCount, userRank.retweetsCount)
        else:
            userRank = UserRank()
            userRank.topic_id = topicId
            userRank.user_id = tweet.user_id
            userRank.followersCount = TweetAuthor.objects.get(id=tweet.user.id).followersCount
            userRank.tweetsCount = 1
            userRank.retweetsCount = tweet.retweetsCount
            userRank.likesCount = tweet.likesCount
            userRank.mentionsCount = 0
            userRank.score = score(userRank.mentionsCount, userRank.retweetsCount)

        userRank.save()

    mentions = UserMention.objects.filter(topic_id=topicId)
    for mention in mentions:
        rank = userRank.objects.filter(topic_id=topicId, user_id=mention.userId)
        rank.mentionsCount += 1
        rank.score = score(userRank.mentionsCount, userRank.retweetsCount)
        rank.save()


def score(mentions, retweets):
    return mentions + retweets
