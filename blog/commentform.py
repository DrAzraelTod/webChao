#!/usr/bin/python
# -*- coding: utf-8 -*-
from django import forms

class CommentForm(forms.ModelForm):
  class Meta:
    model = Comments
#  nickname = forms.CharField(max_length=128)
#  email    = forms.EmailField89
#  text     = forms.CharField()
#  url      = forms.



#  authenticated = models.BooleanField()
#  author = models.ForeignKey(UserProfile, blank=True, null=True)
#  text = models.TextField()
#  status = models.IntegerField(choices=COMMENT_STATUS)
#  nickname = models.CharField(max_length=128, blank=True, null=True)
#  email = models.EmailField(blank=True, null=True)
#  ip = models.IPAddressField()
#  url = models.URLField(blank=True, null=True)
#  referenced = models.ForeignKey("self", related_name="referencing", blank=True, null=True)
#  post = models.ForeignKey(Post, related_name='comments')
#  date = models.DateTimeField('date commented')
#  template = loader.get_template('blog/comment.html')

