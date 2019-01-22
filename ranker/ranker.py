from django import db

from tweetguru.models import TweetAuthor, UserRank, UserMention, Tweet, SearchResult, Topic


def rank_all():
    print('rank_all')
    topics = Topic.objects.all()
    for t in topics:
        print(t.title)
        rank_topic(t.title)


def rank_topic(topic):
    print('rank_topic', topic)
    tag_search_results = SearchResult.objects.filter(tag=topic)
    topicId = Topic.objects.get(title=topic).id
    UserRank.objects.filter(topic_id=topicId).delete()

    for search_result in tag_search_results:
        tweet = Tweet.objects.filter(id=search_result.tweet_id)[0]
        try:
            userRank = UserRank.objects.get(user_id=tweet.user_id, topic_id=topicId)
            userRank.tweetsCount += 1
            userRank.retweetsCount += tweet.retweetsCount
            userRank.likesCount += tweet.likesCount
            userRank.score = score(userRank.mentionsCount, userRank.retweetsCount)
            print('save1')
            userRank.save()
        except UserRank.DoesNotExist:
            userRank = UserRank()
            userRank.topic_id = topicId
            userRank.user_id = tweet.user_id
            userRank.followersCount = TweetAuthor.objects.get(id=tweet.user.id).followersCount
            userRank.tweetsCount = 1
            userRank.retweetsCount = tweet.retweetsCount
            userRank.likesCount = tweet.likesCount
            userRank.mentionsCount = 0
            userRank.score = score(userRank.mentionsCount, userRank.retweetsCount)
            print('save2', userRank.user.id)
            userRank.save()

        mentions = UserMention.objects.filter(tweet_id=tweet.id)
        for mention in mentions:
            try:
                rank = UserRank.objects.get(topic_id=topicId, user_id=mention.user.id)
                rank.mentionsCount += 1
                rank.likesCount += tweet.likesCount
                rank.score = score(rank.mentionsCount, rank.retweetsCount)
                print('save3')
                rank.save()
            except UserRank.DoesNotExist:
                rank = UserRank()
                rank.topic = Topic.objects.get(id=topicId)
                rank.user = TweetAuthor.objects.get(id=mention.user.id)
                rank.followersCount = rank.user.followersCount
                rank.tweetsCount = 0
                rank.retweetsCount = 0
                rank.mentionsCount = 1
                rank.likesCount = tweet.likesCount
                rank.score = score(rank.mentionsCount, rank.retweetsCount)
                print('save4', mention.user.id)
                rank.save()


def score(mentions, retweets):
    return mentions + retweets
