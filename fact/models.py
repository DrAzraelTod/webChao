#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
import datetime

class Fact(models.Model):
  fact = models.CharField(max_length=512)
  nickname = models.CharField(max_length=64)
  date = models.DateTimeField('date published')
  channel = models.CharField(max_length=64)
  referenced = models.ManyToManyField("self", through="FactRelation", symmetrical=False, related_name="referencing")
  class Meta:
    db_table = 'fact'
    get_latest_by = 'date'
    managed = False
    ordering = ['?', '-date']
    verbose_name = 'fact'
    verbose_name_plural = 'facts'
  def __unicode__(self):
    return u'[#%s] <%s> %s' % (self.id, self.nickname, self.fact)
  def created_today(self):
    return self.date.date() == datetime.date.today()
  def get_absolute_url(self):
    return reverse('webchao.fact.views.byId', args=[self.id])

class FactRelation(models.Model):
  fid = models.ForeignKey(Fact, related_name='referencingRels', db_column='fid')
  refs = models.ForeignKey(Fact, related_name='referencedRels', db_column='refs')
  class Meta:
    db_table= 'fact_rels'
    managed= False
    ordering= ['refs']
    verbose_name= 'Fact-Relation'
    verbose_name_plural= 'Fact-Relationen'

class FactCount(models.Model):
  #select * from fact_count where c >= 60
  #CREATE VIEW IF NOT EXISTS fact_count AS (SELECT DISTINCT f1.nickname, (SELECT COUNT(*) FROM fact f2 WHERE f1.nickname = f2.nickname) c FROM fact f1 ORDER DESC BY c)
  nickname = models.CharField(max_length=64, primary_key=True)
  count = models.IntegerField(verbose_name="Anzahl Facts", db_column='c')
  class Meta:
    db_table= 'fact_count'
    managed= False
    ordering= ['-count'] #Sortieren in SQLite scheint verdammt langsam
    verbose_name= 'Fact-Zähler'
    verbose_name_plural= 'Fact-Zählerstände'
  def __unicode__(self):
    url = self.get_absolute_url()
    return u'<a href="%s">%s&nbsp;(%s)</a>' % (url, self.nickname, self.count)
  def get_absolute_url(self):
    return reverse('webchao.fact.views.byNickname', args=[self.nickname])