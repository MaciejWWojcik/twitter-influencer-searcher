# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.shortcuts import render

from crawler.depth_search_engine import DepthSearchEngine
from crawler.tweet_downloader import downloadLastWeekTweets, save
from .models import Influencer
from .models import Topic

from django.http import HttpResponse


def index(request):

    influencers = Influencer.objects.all()
    topics = Topic.objects.all()

    topic = ''
    if(request.method == 'POST'):
        topic = request.POST['topic']
        selectedTopic = request.POST['selectedTopic']

        if(len(selectedTopic)>0):
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
        jsonContent = json.loads(content)
        tweets = jsonContent["statuses"]
        save(tweets, topic_name)
        engine = DepthSearchEngine(topic_name, content)
        engine.loadAuthorsTweets()
    return HttpResponse("Fetch finished")
