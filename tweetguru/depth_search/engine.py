import os
import json
from tguru.settings import BASE_DIR


def load_file():
    tweetFile = open(os.path.join(BASE_DIR, 'tweetguru', 'depth_search', 'sample-tweet.json'))
    tweet = json.load(tweetFile)

    tweetFile.close()
    return tweet
