#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from webchao.feed import FactFeed, BlogFeed, BlogCommentFeed
feeds = {
  'facts'   : FactFeed,
  ''        : FactFeed,                                       #altlast
  'blog'    : BlogFeed,
  'comments': BlogCommentFeed
}

urlpatterns = patterns('django.contrib.syndication.views',
  (r'^(?P<url>.*)$', 'feed', {'feed_dict': feeds}),
  (r'^$', 'feed', {'feed_dict': feeds}),
)
