import oauth2

from tguru.settings import TWITTER_API_KEY, TWITTER_API_SECRET_KEY, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET


def getTwitterRequestClient():
    consumer = oauth2.Consumer(key=TWITTER_API_KEY, secret=TWITTER_API_SECRET_KEY)
    token = oauth2.Token(key=TWITTER_ACCESS_TOKEN, secret=TWITTER_ACCESS_SECRET)
    return oauth2.Client(consumer, token)