#!/usr/bin/python
# -*- coding: utf-8 -*-
from django import forms
import datetime
from webchao.blog.models import *

class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = ('text',)
  referenced = forms.ModelChoiceField(
    queryset = Comment.objects.filter(
      status__gte=Post.display_states_above,
      date__lte = datetime.datetime.now()
    ),
    empty_label="Artikel",
    label = 'Bezug auf',
    required = False,
  )
  text = forms.CharField(
    label = 'Text',
    widget = forms.Textarea,
    error_messages={'required': 'Inhaltslose Kommentare sind ja fast schon normal, aber das ist Rekord!'},
    required = True,
  )

class UnauthenticatedCommentForm(CommentForm):
  class Meta:
    model = Comment
    fields = ('referenced', 'nickname', 'email', 'url', 'text')
  url = forms.URLField(
    label = 'Link',
    error_messages={
      'invalid': 'Es wurde keine gültige URL angegeben.',
      'invalid_link': 'Dieser Link scheint kürzlich verstorben.',
    },
    required = False,
#    verify_exists = True,
  )
  email = forms.EmailField(
    label = 'E-Mail',
    error_messages={'required': 'Es wurde keine gültige E-Mail-Addresse angegeben.'},
    required = True,
  )

    
class AuthenticatedCommentForm(CommentForm):
  class Meta:
    model = Comment
    fields = ('referenced', 'text')
