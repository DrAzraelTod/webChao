#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('webchao.blog.views',
  (r'^$', 'index'),
  (r'^(?P<post_id>\d+)/(?P<post_title>.*)', 'byId'),
  (r'^tag/(?P<tag_string>.*)$', 'byTag'),
  (r'^search/(?P<q>.*)$', 'search'),
  (r'^search/$', 'search'),
  (r'^author/(?P<username>[a-zA-Z_0-9]*)/.*$', 'byAuthor'),
  (r'^comment/(?P<post_id>\d+)/(?P<param_string>.*)$', 'writeComment'),
  (r'^list/?$', 'biglist'),
)
