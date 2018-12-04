import configparser
import oauth2
import json



def downloadLastWeekTweets(search_query, count):

    url = 'https://api.twitter.com/1.1/search/tweets.json?q=' + search_query + '&count=' + str(count);
    config = configparser.ConfigParser()
    config.read('../auth.ini')
    api_key = config['twitter.com']['ApiKey']
    api_secret_key = config['twitter.com']['ApiSecretKey']
    access_token = config['twitter.com']['AccessToken']
    access_token_secret = config['twitter.com']['AccessTokenSecret']

    consumer = oauth2.Consumer(key=api_key, secret=api_secret_key)
    token = oauth2.Token(key=access_token, secret=access_token_secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request(url, method="GET")
    return content


def save(content, tag):
    jsonContent = json.loads(content)

    tweets = jsonContent["statuses"]

    for tweet in tweets:
        date = tweet["created_at"]
        author = tweet["user"]["name"]
        authorId = tweet["user"]["id"]
        tweetId = tweet["id"]

        file = open('../logs/' + tag + '_' + str(tweetId) + '_' + author + '.json', 'w+')

        data = {}
        data['author'] = author
        data['date'] = date
        data['authorId'] = authorId

        file.write(json.dumps(data));
        file.close()

# Example of usage
# content = downloadLastWeekTweets('tesla',50)
# search_query is a string
# count takes values between 1-100

tag = 'tesla'
amount = 10;

content = downloadLastWeekTweets(tag,amount)
save(content,tag)

