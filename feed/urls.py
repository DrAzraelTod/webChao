#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from webchao.feed import FactFeed, BlogFeed, BlogCommentFeed
feeds = {
  'facts'   : FactFeed(),
  ''        : FactFeed(),                                       #altlast
  'blog'    : BlogFeed(),
  'comments': BlogCommentFeed()
}

urlpatterns = patterns('',
#  (r'^(?P<url>.*)$', 'Feed', {'feed_dict': feeds}),
#  (r'^$', 'Feed', {'feed_dict': feeds}),
  (r'^facts$', FactFeed()),
  (r'^$', FactFeed()),
  (r'^blog$', BlogFeed()),
  (r'^comments$', BlogCommentFeed()),
)
