#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models

class Tag(models.Model):
  name = models.CharField(max_length=128, unique=True)
  def __unicode__(self):
    return self.name
  def get_absolute_url(self):
    return reverse('webchao.blog.views.byTag', args=[self.name])
  class Meta:
    db_table = 'blog_tag'
    ordering = ['name']
    verbose_name = 'Tag'
    verbose_name_plural = 'Tags'

