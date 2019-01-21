# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.shortcuts import render

from crawler.depth_search_engine import DepthSearchEngine
from crawler.tweet_downloader import downloadLastWeekTweets, save
from ranker.ranker import rank_topic
from .models import Topic, TweetAuthor, Tweet

from django.http import HttpResponse


def index(request):
    influencers = TweetAuthor.objects.all()
    topics = Topic.objects.all()

    topic = ''
    if (request.method == 'POST'):
        topic = request.POST['topic']
        selectedTopic = request.POST['selectedTopic']

        if (len(selectedTopic) > 0):
            topic = selectedTopic

    context = {
        'influencers': influencers,
        'topic': topic,
        'topics': topics,
        'tweets': 215214
    }

    return render(request, 'index.html', context)


def interval_fetching(request):
    topics = Topic.objects.all()
    amount = 10
    for topic in topics:
        topic_name = topic.title
        content = downloadLastWeekTweets(topic_name, amount)
        # TODO save to database
        save(content, topic_name)
        engine = DepthSearchEngine(topic_name, content)
        engine.loadAuthorsTweets()
    return HttpResponse("Fetch finished")


def ranker(request, topicId):
    print(request)
    print('FOO')
    print(topicId)
    tweetsBefore = Tweet.objects.filter(id=topicId)
    rank_topic(topicId)
    tweetsAfter = Tweet.objects.filter(id=topicId)
    response = {topicId: topicId, tweetsBefore: tweetsBefore, tweetsAfter: tweetsAfter}
    return HttpResponse(response)
