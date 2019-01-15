from crawler.depth_search_engine import DepthSearchEngine
from crawler.properties import properties
from crawler.tweet_downloader import save, downloadLastWeekTweets


def interval_fetching():
    print("RUN BG TASK")
    amount = properties()['amount']
    for tag in properties()['tags']:
        content = downloadLastWeekTweets(tag, amount)
        save(content, tag)
        engine = DepthSearchEngine(tag, content)
        engine.loadAuthorsTweets()
        # engine.loadMentionedUsersTweets()
