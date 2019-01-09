# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Influencer(models.Model):
    fullName = models.TextField()
    nick = models.TextField()

    def __str__(self):
        return self.fullName


class Topic(models.Model):
    title = models.TextField()

    def __str__(self):
        return self.title

