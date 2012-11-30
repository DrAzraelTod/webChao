#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template import Context, loader

class Path(models.Model):
  url = models.CharField('URL',max_length="512" , unique=True)
  def __unicode__(self):
    return self.url
  class Meta:
    verbose_name = 'Pfad'
    verbose_name_plural = 'Pfade'

class Client(models.Model):
  name = models.CharField('Name', max_length=64, unique=True)
  last_seen = models.DateTimeField('zuletzt gesehen')
  def __unicode__(self):
    return self.name
  class Meta:
    ordering = ['last_seen']

class Entry(models.Model):
  request_time = models.DateTimeField('Zeitpunkt')
  path = models.ForeignKey(Path, related_name="requests", blank=True, null=True, verbose_name="Pfad")
  client = models.ForeignKey(Client, related_name="requests", blank=True, null=True)
  user = models.ForeignKey(User)
  class Meta:
    ordering = ['request_time']
    verbose_name = 'Eintrag'
    verbose_name_plural = 'Einträge'
