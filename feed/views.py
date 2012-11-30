#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404
from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404

def index(request):
  return facts(request, '')

def facts(request, path):
  fact_text=request.REQUEST.get('fact_text', '')
  facts = Fact.objects.filter(fact__contains=fact_text)
  return HttpResponse(facts)

