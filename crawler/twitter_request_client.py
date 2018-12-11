import configparser
import oauth2

def getTwitterRequestClient():
    config = configparser.ConfigParser()
    config.read('../auth.ini')
    api_key = config['twitter.com']['ApiKey']
    api_secret_key = config['twitter.com']['ApiSecretKey']
    access_token = config['twitter.com']['AccessToken']
    access_token_secret = config['twitter.com']['AccessTokenSecret']

    consumer = oauth2.Consumer(key=api_key, secret=api_secret_key)
    token = oauth2.Token(key=access_token, secret=access_token_secret)
    return oauth2.Client(consumer, token)