# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
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

