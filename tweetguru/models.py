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


class Topic(models.Model):
    title = models.CharField(max_length=256, blank=True, null=True)
    topicId = models.CharField(max_length=256, blank=True, null=True)

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

    def __str__(self):
        return self.text


class Hashtag(models.Model):
    tweetId = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    value = models.CharField(max_length=256, blank=True, null=True)


class UserMention(models.Model):
    userId = models.ForeignKey(TweetAuthor, on_delete=models.CASCADE)
    tweetId = models.ForeignKey(Tweet, on_delete=models.CASCADE)
