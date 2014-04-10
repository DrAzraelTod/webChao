#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from UserProfile import UserProfile
from Post import Post
from django.template import Context, loader
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from webchao.blog.settings import *
import datetime
import re
import codecs
from collections import *


COMMENT_STATUS = (
  (7,  'öffentlich'),
  (6,  'auto-öffentlich'),
  (4,  'unbekannt'),
  (2,  'gelöscht'),
  (1,  'auto-Spam'),
  (0,  'Spam'),
)

class Comment(models.Model):
  authenticated = models.BooleanField()
  author = models.ForeignKey(UserProfile, blank=True, null=True)
  text = models.TextField()
  status = models.IntegerField(choices=COMMENT_STATUS, default=4)
  nickname = models.CharField(max_length=128, blank=True, null=True)
  email = models.EmailField(blank=True, null=True)
  ip = models.IPAddressField(default='127.0.1.2')
  url = models.URLField(blank=True, null=True)
  referenced = models.ForeignKey("self", related_name="referencing", blank=True, null=True, verbose_name="Bezug auf")
  post = models.ForeignKey(Post, related_name='comments')
  date = models.DateTimeField('geschrieben am')
  template = loader.get_template('blog/comment.html')
  # filter what states (__gte) should be displayed public
  display_states_above = 6

  class Meta:
    db_table = 'blog_comment'
    get_latest_by = 'date'
    ordering = ['date']
    verbose_name = 'Kommentar'
    verbose_name_plural = 'Kommentare'
  #some kind of poor-mans spamfilter
  #maybe someday i will be bored enough to compile a list of bad words

  def autodecide_status(self):
    #Filter based on previous comments with same text
    blocked = Comment.objects.filter(text=self.text, status__in=[1,0,2]).count()
    if blocked >= 1:
      self.status = 1
    else:
      #Filter based on previous comments, allready moderated by admin
      blocked = Comment.objects.filter(email=self.email, status=0).count()
      blocked = blocked+Comment.objects.filter(url=self.url, status=0).count()
      allowed = Comment.objects.filter(email=self.email, status=7).count()
      #pessimistic aproach: noone is allowed to post, except he is NOT categorized as spam
      #yeah.. this was optimistic before.. who might have guessed
      if (blocked >= allowed):
        self.status = 1
      else:
        self.status = 6
        return self.status
    fh = codecs.open(SPAMFILTER_URLS,encoding='utf-8')
    for line in fh.readlines():
      if (line[:-1] in self.url):
        raise PermissionDenied()
#    referer = request.META.get('HTTP_REFERER', '')
#    if (referer == u"-"):
#      raise PermissionDenied()
    fh = codecs.open(SPAMFILTER_WORDS,encoding='utf-8')
    text_count = 0
    name_count = 0
    for line in fh.readlines():
      if (line[:-1] in self.text):
        text_count += 1
      if (line[:-1] in self.nickname):
        name_count += 1
    if (name_count >= SPAMFILTER_WORDS_NAME_MAX or text_count >= SPAMFILTER_WORDS_TEXT_MAX):
      raise PermissionDenied()
    c = Counter(re.findall(r"href=",self.text.lower()))
    if c['href='] >= 6:
      raise PermissionDenied()
    if len(re.findall(r"https?://",self.text.lower())) > 10:
      raise PermissionDenied()
    return self.status
  #we need to fill a comment from an user-object... maybe via User->UserProfile

  def fill_from_user(self,user):
    if (user.is_authenticated()):
      self.authenticated = True
      try:
        profile = UserProfile.objects.get(user=user)
        self.author = profile
      except:
        self.nickname = user.username
        self.url = reverse('webchao.blog.views.byAuthor', args=[user.username])
      self.email = user.email
      self.status = 6
    else:
      self.authenticated = False
      self.autodecide_status()
    self.date = datetime.datetime.now()

  def get_author_nickname(self):
    if (self.authenticated and not self.nickname):
      if (self.author.nickname):
        return self.author.nickname
      else:
        return self.author.user.username
    else:
      return self.nickname

  def __unicode__(self):
    return '#%s von %s' % (self.id, self.get_author_nickname())

  def render(self):
    c = Context({
      'comment': self,
      'nickname': self.get_author_nickname(),
      'references': self.referencing.filter(status__gte=self.display_states_above),
    })
    return self.template.render(c)

  def get_absolute_url(self, byId = True):
    return "%s#comment_%s" % (self.post.get_absolute_url(byId), self.id)
