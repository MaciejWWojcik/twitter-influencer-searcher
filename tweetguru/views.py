# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import threading

from django.shortcuts import render

from crawler.depth_search_engine import DepthSearchEngine
from crawler.tweet_downloader import downloadLastWeekTweets, save
from ranker.ranker import rank_topic, rank_all
from .models import Topic, TweetAuthor, Tweet, UserRank

from django.http import HttpResponse


def index(request):
    influencers = []
    topics = Topic.objects.all()

    topic = ''
    if (request.method == 'POST'):
        topic = request.POST['topic']
        selectedTopic = request.POST['selectedTopic']
        ranks = UserRank.objects.order_by('-score')[:5]
        for rank in ranks:
            influencer = TweetAuthor.objects.filter(id=rank.user_id)[0]
            print(influencer)
            influencers.append(influencer)

        if (len(selectedTopic) > 0):
            topic = selectedTopic

    context = {
        'influencers': influencers,
        'topic': topic,
        'topics': topics,
        'tweets': len(Tweet.objects.all())
    }

    return render(request, 'index.html', context)


def interval_fetching(request):
    fetch_thread = threading.Thread(target=fetch_tweets,args=())
    fetch_thread.daemon = True
    fetch_thread.start()
    return HttpResponse("Fetch finished")

def fetch_tweets():
    topics = Topic.objects.all()
    amount = 10
    for topic in topics:
        topic_name = topic.title
        content = downloadLastWeekTweets(topic_name, amount)
        jsonContent = json.loads(content)
        tweets = jsonContent["statuses"]
        save(tweets, topic_name)
        engine = DepthSearchEngine(topic_name, content)
        engine.loadAuthorsTweets()


def ranker(request, topic):
    rank_topic(topic)
    return HttpResponse(topic)

def ranker_all(request):
    rank_all()
    return HttpResponse('all')
