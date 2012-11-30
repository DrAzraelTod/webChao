#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from UserProfile import UserProfile
from Tag import Tag
from django.core.urlresolvers import reverse

POST_STATUS = (
  (1,  'gelöscht'),
  (2,  'Veröffentlichen'),
  (0,  'Entwurf'),
)

class Post(models.Model):
  text = models.TextField('Inhalt')
  title = models.CharField('Titel', max_length=255)
  author = models.ForeignKey(UserProfile, related_name="posts")
  date = models.DateTimeField('veröffentlicht ab')
  tags = models.ManyToManyField(Tag, symmetrical=False, related_name="posts")
  status = models.IntegerField('Status', choices=POST_STATUS)
  # filter what states (__gte) should be displayed public
  display_states_above = 2
  def created_today(self):
    return self.date.date() == datetime.date.today()
  def get_slug(self):
    slug = self.title.replace(' ', '-') # spaces are bad in urls
    slug = slug.replace('#', '')        # because we would want to see things after this in the url
    slug = slug.replace("&quot;", '')   # because i was once migrating from wordpress... dont ask!
    slug = slug.replace('?', '')        # questionmark because this should not get pushed into parameters
    slug = slug.replace('\\', '')       # dont really know if we will need this...
    slug = slug.replace('/', '')        # obvious
    slug = slug.replace('---', '-')     # ' - ' gets converted to '---' -> 'foo---bar' ->'foo-bar'
    return slug
  def get_absolute_url(self, byId = False):
    if (byId):
      return reverse('webchao.blog.views.byId', args=[self.id, self.get_slug()])
    else:
      return reverse('webchao.blog.views.byDate', args=[self.date.date().year, self.date.date().month, self.date.date().day, self.get_slug()])
  def __unicode__(self):
    return self.title
  class Meta:
    db_table = 'blog_post'
    get_latest_by = 'date'
    ordering = ['-date']
    verbose_name = 'Artikel'
    verbose_name_plural = 'Artikel'

