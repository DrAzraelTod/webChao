#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
from django.http import HttpResponse, Http404
from webchao.fact.models import Fact
from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
import types

fact_template = loader.get_template('fact/fact.html')
facts_template = loader.get_template('fact/facts.html')
amount_default = 20

def index(request):
  fact_text=request.REQUEST.get('fact_text', '')
  facts = Fact.objects.filter(fact__contains=fact_text)
  return HttpResponse(renderFacts(facts))

def byId(request,fact_id):
  #print('by id %s' % fact_id)
  fact = get_object_or_404(Fact, id=fact_id)
  return HttpResponse(renderFacts([fact]))

def byNickname(request, fact_nickname):
  facts = Fact.objects.filter(nickname__iexact=fact_nickname)
  ret = renderFacts(facts)
  return HttpResponse(ret)
  
def byNicknameOne(request, fact_nickname):
  facts = Fact.objects.filter(nickname__iexact=fact_nickname)[:1]
  #facts = Fact.objects.filter(nickname__iexact=fact_nickname).order_by('-date')[:1]
  ret = renderFacts(facts)
  return HttpResponse(ret)

def byFact(request, fact_text):
  facts = Fact.objects.filter(fact__contains=fact_text)
  ret = renderFacts(facts)
  return HttpResponse(ret)

def byFactOne(request, fact_text):
  facts = Fact.objects.filter(fact__contains=fact_text)[:1]
  ret = renderFacts(facts)
  return HttpResponse(ret)

def byChannel(request, fact_channel):
  facts = Fact.objects.filter(channel__iexact=fact_channel)
  ret = renderFacts(facts)
  return HttpResponse(ret)

def byChannelOne(request, fact_channel):
  facts = Fact.objects.filter(channel__iexact=fact_channel)[:1]
  ret = renderFacts(facts)
  return HttpResponse(ret)

def renderFacts(facts):
  only_one = False
  title = 'Webchao - Facts'
  try:
    count = facts.count()
  except TypeError:
    count = 1
    only_one = True
    title = 'Webchao - Fact #%s' % facts[0].id
  facts = facts[:amount_default]
  if (count < amount_default):
    count = False
  else:
    print('%s Facts zum Anzeigen' % count)
  fact_texts = []
  for fact in facts:
    print(fact)
    c = Context({
      'fact': fact,
      'referenced':   fact.referenced.all(),
      'referencing':  fact.referencing.all(),
    })
    fact_texts.append(fact_template.render(c))
  c = Context({
    'count':          count,
    'facts':          fact_texts,
    'max_count':      amount_default,
    'only_one':       only_one,
    'css':            ['/static/page.css'],
    'title':          title,
    'authors':        ['Dr_Azrael_Tod', 'profmakx', 'Snookie', 'Daeva', 'RobVinc'],
                      # FactCount.models.filter(count__gte=60)
    'rss':            [
      ['neueste Facts', '/feed/facts'],
      ['Blog', '/feed/blog'],
      ['DATs Shared', 'http://feeds.feedburner.com/SharedByDrAzraelTod'],
      ['DATs Starred', 'http://feeds.feedburner.com/StarredByDrAzraelTod'],
    ],
  })
  return facts_template.render(c)