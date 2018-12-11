import json

class Tweet:
    id = ''
    date = ''
    text = ''
    hashtags = []
    usersMentions = []
    user = {}

    def __init__(self, tweet):
        self.id = tweet['id']
        self.date = tweet['created_at']
        self.text = tweet['text']
        self.user = User(tweet['user'])
        for hashtag in  tweet['entities']['hashtags']:
            self.hashtags.append(hashtag['text'])
        for user in tweet['entities']['user_mentions']:
            self.usersMentions.append(BasicUser(user))

    def toJSON(self):
        return  json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4, separators=(',', ': '))

class User:
    id = ''
    name = ''
    fullName = ''
    followersCount= ''
    friendsCount =''

    def __init__(self, user):
        self.id = user['id']
        self.name = user['screen_name']
        self.fullName = user['name']
        self.followersCount = user['followers_count']
        self.friendsCount = user['friends_count']

class BasicUser:
    id =''
    name =''
    fullName = ''

    def __init__(self, user):
        self.id = user['id']
        self.name = user['screen_name']
        self.fullName = user['name']