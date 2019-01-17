class UserRank:
    phrase = ''
    user_id = ''
    followers_count = 0
    friends_count = 0
    retweets_count = 0
    likes_count = 0
    mentions_count = 0

    def __init__(self, phrase, user_id, followers_count, friends_count, retweets_count, likes_count, mentions_count):
        self.phrase = phrase
        self.user_id = user_id
        self.followers_count = followers_count
        self.friends_count = friends_count
        self.retweets_count = retweets_count
        self.likes_count = likes_count
        self.mentions_count = mentions_count

