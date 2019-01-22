# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import threading

from django.shortcuts import render

from crawler.depth_search_engine import DepthSearchEngine
from crawler.tweet_downloader import downloadLastWeekTweets, save
from crawler.twitter_request_client import getTwitterRequestClient
from ranker.ranker import rank_topic, rank_all
from .models import Topic, TweetAuthor, Tweet, UserRank, SearchResult

from django.http import HttpResponse


def index(request):
    influencers = []
    topics = Topic.objects.all()
    tweetsNumber = 0

    topic = ''
    if (request.method == 'POST'):
        topic = request.POST['topic']
        selectedTopic = request.POST['selectedTopic']
        filteredTopics = Topic.objects.filter(title=selectedTopic)
        if len(filteredTopics) > 0:
            topicId = filteredTopics[0].id
            ranks = UserRank.objects.filter(topic_id=topicId).order_by('-score')[:5]
            for rank in ranks:
                influencer = TweetAuthor.objects.filter(id=rank.user_id)[0]
                influencer.fullName = influencer.fullName.split('\'')[1]
                influencers.append(influencer)
            topic = selectedTopic
            tweetsNumber = len(SearchResult.objects.filter(tag=topic))
        else:
            tweetsNumber = 5
            adHocTweets = json.loads(downloadLastWeekTweets(topic, tweetsNumber))
            if 'statuses' in adHocTweets:
                for tweet in adHocTweets['statuses']:
                    influencer = TweetAuthor()
                    influencer.fullName = tweet['user']['name']
                    influencer.name = tweet['user']['screen_name']
                    influencer.avatar = tweet['user']['profile_image_url']
                    influencer.score = tweet['user']['followers_count']
                    influencers.append(influencer)

    context = {
        'influencers': influencers,
        'topic': topic,
        'topics': topics,
        'tweets': tweetsNumber
    }

    return render(request, 'index.html', context)


def interval_fetching(request):
    fetch_thread = threading.Thread(target=fetch_tweets, args=())
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


def fix_avatars(request):
    client = getTwitterRequestClient()
    requestUrl = "https://api.twitter.com/1.1/users/show.json"
    authors = TweetAuthor.objects.all()
    for author in authors:
        print(author)
        if author.avatar == None or author.avatar == '':
            timelineUrl = requestUrl + "?count=1&user_id=" + str(author.twitterUserId)
            resp, content = client.request(timelineUrl, method="GET")
            print(content)
            jsonContent = json.loads(content.decode('utf8'))
            if 'profile_image_url' in jsonContent:
                author.avatar = jsonContent['profile_image_url']
                author.save()
                print(resp)
                print(author.avatar)
    return HttpResponse('fixed it')
