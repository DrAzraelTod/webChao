#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class UserProfile(models.Model):
  user = models.ForeignKey(User, unique=True)
  nickname = models.CharField(max_length=128)
  jabber_id = models.EmailField(unique=True)
  def __unicode__(self):
    return self.nickname
  def get_absolute_url(self, byId = False):
    return reverse('webchao.blog.views.byAuthor', args=[self.user.username])
  class Meta:
    db_table = 'blog_userprofile'

