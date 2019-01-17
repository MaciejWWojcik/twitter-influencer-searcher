# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.

class Influencer(models.Model):
    fullName = models.CharField(max_length=256, blank=True, null=True)
    nick = models.CharField(max_length=256, blank=True, null=True)
    avatar = models.CharField(max_length=256, blank=True, null=True)
    userId = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.fullName

class InfluencerRank(models.Model):
        userId = models.CharField(max_length=256, blank=True, null=True)
        followersCount = models.IntegerField()
        retweetsCount = models.IntegerField()
        likesCount = models.IntegerField()
        mentionsCount = models.IntegerField()


class Topic(models.Model):
    title = models.CharField(max_length=256, blank=True, null=True)
    topicId = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.title

class Tweet(models.Model):
    tweetId = models.CharField(max_length=256, blank=True, null=True)
    date = models.DateField()
    text = models.CharField(max_length=256, blank=True, null=True)
    userId = models.CharField(max_length=256, blank=True, null=True)

