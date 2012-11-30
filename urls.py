#!/usr/bin/python
# -*- coding: utf-8 -*-
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^webchao/', include('webchao.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
  (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
  (r'^admin/', include(admin.site.urls)),
  ####################
  # Newsfeeds
  ####################
  (r'^feed/', include('webchao.feed.urls')),
  (r'^feeds/', include('webchao.feed.urls')),
  (r'^lastfacts.xml$', include('webchao.feed.urls')),                          #altlast
  ####################
  # Weblog
  ####################
  (r'^blog/', include('webchao.blog.urls')),
  (r'^(?P<year>[12][0-9]{3})/(?P<month>[0-1]?[0-9])/(?P<day>[0-3]?[0-9])/(?P<title>.*)/$', 'webchao.blog.views.byDate'), #/2010/02/07/e-t-software/
  (r'^(?P<year>[12][0-9]{3})/(?P<month>[0-1]?[0-9])/(?P<day>[0-3]?[0-9])/(?P<title>.*)$', 'webchao.blog.views.byDate'), #/2010/02/07/foobar
  (r'^(?P<year>[12][0-9]{3})/(?P<month>[0-1]?[0-9])/(?P<title>.*)\.html$', 'webchao.blog.views.byDate'), #/2010/02/e-t-software.html
  (r'^(?P<year>[12][0-9]{3})/(?P<month>[0-1]?[0-9])/(?P<title>.*)$', 'webchao.blog.views.byDate'), #/2010/02/e-t-software
  (r'^(?P<year>[12][0-9]{3})/(?P<month>[0-1]?[0-9])/(?P<day>[0-3]?[0-9])/?$', 'webchao.blog.views.byDate'), #/2010/02/07
  (r'^(?P<year>[12][0-9]{3})/(?P<month>[0-1]?[0-9])/?$', 'webchao.blog.views.byDate'), #/2010/02/
  (r'^OSX_-_function_follows_form$', 'webchao.blog.views.byId', {'post_id': '1534'}),
#  (r'^(?P<year>[12][0-9]{3})/?$', 'webchao.blog.views.byDate'), #/2010/
  (r'^(?P<post_id>\d+)$', 'webchao.blog.views.byId'), #/1234
  ####################
  # Fact-Spezifisches
  ####################
  (r'^$', 'webchao.blog.views.index'),
  (r'^fact/(?P<fact_id>\d+).html/$', 'webchao.fact.views.byId'),                #aus hyster^Whistorischen Gründen
  (r'^fact/(?P<fact_text>.*)/$', 'webchao.fact.views.byFact'),
  (r'^fs/$', 'webchao.fact.views.index'),                                       #um irc-kommandos komplett zu unterstüzuen
  (r'^fact/$', 'webchao.fact.views.index'),
  (r'^fs/(?P<fact_text>.*)/$', 'webchao.fact.views.byFact'),
  (r'^fid/(?P<fact_id>\d+)/$', 'webchao.fact.views.byId'),
  (r'^fsname/(?P<fact_nickname>.*)/$', 'webchao.fact.views.byNickname'),
  (r'^fname/(?P<fact_nickname>.*)/$', 'webchao.fact.views.byNicknameOne'),
  ####################
  # Statisches Zeugs
  ####################
  (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/dat/webchao/web'}),
  (r'^[Hh][oO][cC][hH][zZ][eE][iI][tT]/?$', redirect_to, {'url': 'https://www.dropbox.com/sh/dbe6t0czpnqwct4/yYys74ZWP5'}),
  (r'^dropbox/?$', redirect_to, {'url':'http://db.tt/xpxZO66'}),
)
