#!/usr/bin/python
# -*- coding: utf-8 -*-

class StatisticsMiddleware(object):

  def process_request(self, request):
    if not request.META.has_key('REMOTE_ADDR'):
      try:
        request.META['REMOTE_ADDR'] = request.META['HTTP_X_REAL_IP']
      except:
        request.META['REMOTE_ADDR'] = '1.1.1.1' # This will place a valid IP in REMOTE_ADDR but this shouldn't happen
    self.save_entry(request)
    
  def save_entry(self, request):
    foo = request.META['REMOTE_ADDR']
    port = request.META['SERVER_PORT']
    user_agent = request.META['HTTP_USER_AGENT']
    host = request.META['HTTP_HOST']
    remote_host = request.META['REMOTE_HOST']
    protocol = request.META['SERVER_PROTOCOL']
    method = request.META['REQUEST_METHOD']
    lang = request.META['HTTP_ACCEPT_LANGUAGE']
    path = request.META['PATH_INFO']
    encoding = request.META['HTTP_ACCEPT_ENCODING']
#    print('%s' % request.META)
    print('%s %s %s %s %s %s %s %s %s %s' % (foo, port, user_agent, host, remote_host, protocol, method, lang, path, encoding))
