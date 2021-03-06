#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context, loader
from webchao.blog.models import Post, Tag, UserProfile, Comment
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render_to_response, get_object_or_404
from webchao.blog import UnauthenticatedCommentForm, AuthenticatedCommentForm
import datetime
#from webchao.lib import jabber_status

blog_template = loader.get_template('blog/blog.html')
short_post_template = loader.get_template('blog/short_post.html')
micro_post_template = loader.get_template('blog/micro_post.html')
post_template = loader.get_template('blog/post.html')

global page_limit
page_limit = 50

def biglist(request):
  global page_limit
  page_limit = 0
  all_posts = Post.objects.order_by('-date')
  return renderSomething(all_posts, request)

def index(request):
  global page_limit
  page_limit = 50
  all_posts = Post.objects.order_by('-date')
  return renderSomething(all_posts, request)


def byId(request, post_id, post_title = ''):
  post = get_object_or_404(Post, id=post_id)
  return renderSomething([post], request)

def byDate(request, year, month = '', day = '', title = ''):
  posts = Post.objects.filter(date__year=year)
  if (month != ''):
    posts = posts.filter(date__month = month)
  if (day != ''):
    posts = posts.filter(date__day = day)
  if (title != ''):
    for post in posts:
      if (post.get_slug().lower() == title.lower()):
        return renderSomething([post], request)
    return renderSomething([], request)
  return renderSomething(posts, request)

def search(request,q = ''):
  q=request.REQUEST.get('q', q)
  all_posts = Post.objects.filter(text__contains=q)
  return renderSomething(all_posts, request)

def byAuthor(request, username):
  author = get_object_or_404(UserProfile, user__username=username)
  posts = author.posts.all()
  return renderSomething(posts, request)


def byTag(request, tag_string):
  tag = get_object_or_404(Tag, name=tag_string)
  posts = tag.posts.all()
  return renderSomething(posts, request)

def renderBlog(content, title = ''):
  profiles = UserProfile.objects.annotate(num_posts=Count('posts')).order_by('-num_posts')[:5]
  c = Context({
    'content':        content,
    'css':            ['/static/page.css'],
    'title':          title,
    'rss':            [
      ['neueste Facts', '/feed/facts'],
      ['Artikel', '/feed/blog'],
      ['Kommentare', '/feed/comments'],
#      ['DATs Shared', 'http://feeds.feedburner.com/SharedByDrAzraelTod'],
#      ['DATs Starred', 'http://feeds.feedburner.com/StarredByDrAzraelTod'],
      ['Diaspora', 'https://pod.geraspora.de/public/drazraeltod.atom'],
      ['Soup.io', 'http://soup.g33ky.de/rss/original']
    ],
    'last_posts':     Post.objects.filter().order_by('-date').filter(status__gte=Post.display_states_above, date__lte = datetime.datetime.now())[:5],
    'authors':        profiles,
  })
  return HttpResponse(blog_template.render(c))

def renderSomething(posts, request):
  # Anzahl feststellen, Eingabewerte filtern
  if (isinstance(posts,list)):
    count = len(posts)
    if (count == 1):
      posts = posts[0]
  else:
    try:
      # filter every non-published post
      posts = posts.filter(status__gte=Post.display_states_above, date__lte = datetime.datetime.now())
      count = posts.count()
      if(count == 1):
        posts = posts[0]
    except:
      count = 1
      posts = posts[0]

  # Ausgeben
  title = ''
  if (count > 1):
    content = renderPosts(posts)
  elif (count == 1):
    content = renderSinglePost(posts, request)
    title   = posts.title
  else:
    content = 'Keine Beiträge gefunden'
  return renderBlog(content, title)

def renderPosts(posts):
  ret = ''
  if (page_limit == 0):
    ret +='<ul class="postlist">'
  temp = posts
  if (page_limit > 0):
    temp = posts[:page_limit]
  for p in temp:
    c = Context({
      'post': p
    })
    if (page_limit > 0):
      ret += short_post_template.render(c)
    else:
      ret += micro_post_template.render(c)
  if (page_limit == 0):
    ret += '</ul>'
  return ret

def renderSinglePost(post, request):
  if request.method == 'POST':
    if (request.user.is_authenticated()):
      comment_form = AuthenticatedCommentForm(request.POST)
    else:
      comment_form = UnauthenticatedCommentForm(request.POST)
  else:
    if (request.user.is_authenticated()):
      comment_form = AuthenticatedCommentForm()
    else:
      comment_form = UnauthenticatedCommentForm()
  comment_form.fields['referenced'].queryset = Comment.objects.filter(
    post=post.id,
    status__gte=Comment.display_states_above
  )
  c = Context({
    'post': post,
    'comments': post.comments.filter(referenced__isnull=True, status__gte=Comment.display_states_above),
    'comment_form': comment_form,
  })
  return post_template.render(c)

def writeComment(request, post_id, param_string):
  #get the Object
  post = Post.objects.get(id=post_id)
  comment = Comment()
  if (request.user.is_authenticated()):
    comment.authenticated = True
    cf = AuthenticatedCommentForm(request.POST, comment)
  else:
    comment.authenticated = False
    cf = UnauthenticatedCommentForm(request.POST, comment)
  cf.fields['referenced'].queryset = Comment.objects.filter(
    post=post.id,
    status__gte=Comment.display_states_above
  )
  #read the data and fill it in
  if cf.is_valid():
    comment = cf.save(commit=False)
    comment.fill_from_user(request.user)
    try:
      comment.ip = request.META['REMOTE_ADDR']
    except:
      comment.ip = '1.1.1.1'
    comment.post = post
    comment.save()
    return HttpResponseRedirect(post.get_absolute_url())
  else:
    print(cf)
  return byId(request, post.id)
