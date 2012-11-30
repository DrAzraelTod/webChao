from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed, RssUserland091Feed, Rss201rev2Feed
from webchao.fact.models import Fact
from webchao.blog.models import Post, Comment
import datetime



class FactFeed(Feed):
  title = 'Webchao Fact-Feed'
  link = '/fact/'
  description = "Die neuesten pyChao-Facts im WWW"
  feed_type = Atom1Feed
  title_template = 'feed/fact_title'
  description_template = 'feed/fact_description'
  def items(self):
    return Fact.objects.order_by('-date')[:30]
  def item_title(self, item):
    return item.fact
  def item_description(self,item):
    return item
    
class BlogFeed(Feed):
  title = 'G33KY^2 - The Nerd Strikes Back'
  link = '/fact/'
  description = "Der Newsfeed zum Blog"
  feed_type = Atom1Feed
  title_template = 'feed/blog_title'
  description_template = 'feed/blog_description'
  def items(self):
    return Post.objects.filter(
      status__gte=Post.display_states_above,
      date__lte = datetime.datetime.now()
    ).order_by('-date')[:30]
  def item_title(self, item):
    return item.title
  def item_description(self,item):
    return item.text

class PostsFeed(BlogFeed):
   slug = 'posts'

class BlogCommentFeed(Feed):
  title = "G33KY^2 Kommentare"
  link = "/blog"
  description = "Alle Kommentare auf das Blog"
  feed_type = Atom1Feed
  description_template = 'feed/blog_comment_description'
  def items(self):
    return Comment.objects.filter(
      status__gte=Comment.display_states_above
    ).order_by('-date')[:30]
  def item_title(self, item):
    nickname = item.get_author_nickname()
    title = item.post.title
    return "Kommentar von %s auf %s" % (nickname, title)
  def item_description(self, item):
    return item.text
