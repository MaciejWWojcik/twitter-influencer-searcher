# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, JsonResponse

from tweetguru.depth_search.engine import load_file


def index(request):
    return HttpResponse('Hello world, tweetguru here')


def engine(request):
    tweetContent = load_file()
    return JsonResponse(tweetContent)
