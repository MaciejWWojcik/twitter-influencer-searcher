from crawler.tweet import User, Tweet
from ranker.user_rank import UserRank


class Ranker:
    def rank_user(self, phrase, user: User, user_tweets: [Tweet]):
        retweets_count = 0
        likes_count = 0
        for tweet in user_tweets:
            retweets_count += tweet.retweets_count
            likes_count += tweet.likes_count
        return UserRank(phrase, user.id, user.followersCount, user.friendsCount, retweets_count, likes_count, mentions_count)
