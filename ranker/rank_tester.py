import json

from crawler.twitter_request_client import getTwitterRequestClient



def downloadLastWeekTweets(search_query, count):
    url = 'https://api.twitter.com/1.1/search/tweets.json?q=' + search_query + '&count=' + str(count);
    client = getTwitterRequestClient()
    resp, content = client.request(url, method="GET")
    return content


phrase = 'Tesla'
search_results = downloadLastWeekTweets(phrase, 90)
jsonContent = json.loads(search_results)
tweets = jsonContent["statuses"]
userRanks = [UserRank]
for tweet in tweets:
    is_in_array = False
    for rank in userRanks:
        tweetLikes =  tweet['favorite_count']
        retweets = tweet['retweet_count']
        if tweet['user']['id'] == rank.userId:
            rank.tweetsCount += 1
            rank.likesCount += tweetLikes
            rank.retweetsCount += retweets
            is_in_array = True

    if not is_in_array:
        new_rank = UserRank()
        new_rank.phrase = phrase
        new_rank.userId = tweet['id']
        new_rank.followersCount = tweet['user']['followers_count']
        new_rank.retweetsCount = retweets
        new_rank.likesCount = tweetLikes
        new_rank.mentionsCount = 0
        new_rank.tweetsCount = 1
        userRanks.append(new_rank)



print(json.dumps(userRanks[0]))
print(userRanks.__len__())
