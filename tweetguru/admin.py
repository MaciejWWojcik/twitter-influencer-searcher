# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Influencer
from .models import Topic
# Register your models here.

admin.site.register(Influencer)
admin.site.register(Topic)