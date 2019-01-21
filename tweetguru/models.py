# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Topic(models.Model):
    title = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.title


class TweetAuthor(models.Model):
    twitterUserId = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=256, blank=True, null=True)
    fullName = models.CharField(max_length=256, blank=True, null=True)
    followersCount = models.IntegerField()
    friendsCount = models.IntegerField()


class Tweet(models.Model):
    twitterContentId = models.BigIntegerField(unique=True)
    date = models.CharField(max_length=256, blank=True, null=True)
    text = models.CharField(max_length=256, blank=True, null=True)
    user = models.ForeignKey(TweetAuthor, on_delete=models.CASCADE)
    retweetsCount = models.IntegerField()
    likesCount = models.IntegerField()

    def __str__(self):
        return self.text


class Hashtag(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    value = models.CharField(max_length=256, blank=True, null=True)


class UserMention(models.Model):
    user = models.ForeignKey(TweetAuthor, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)


class SearchResult(models.Model):
    tag = models.CharField(max_length=2048, blank=True, null=True)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)


class UserRank(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    user = models.ForeignKey(TweetAuthor, on_delete=models.CASCADE)
    followersCount = models.IntegerField()
    tweetsCount = models.IntegerField()
    retweetsCount = models.IntegerField()
    likesCount = models.IntegerField()
    mentionsCount = models.IntegerField()
