# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Topic, TweetAuthor, Tweet, Hashtag, UserMention, SearchResult, UserRank

# Register your models here.

admin.site.register(Topic)
admin.site.register(TweetAuthor)
admin.site.register(Tweet)
admin.site.register(Hashtag)
admin.site.register(UserMention)
admin.site.register(SearchResult)
admin.site.register(UserRank)

