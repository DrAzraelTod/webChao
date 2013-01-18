from webchao.blog.models import Post, Comment, UserProfile, Tag
from django.contrib import admin
from django.contrib.auth.models import User

admin.site.register(Tag)
admin.site.register(UserProfile)

class PostAdmin(admin.ModelAdmin):
    list_display  = ('title', 'author', 'status', 'date')
    list_filter   = ('tags', 'author', 'status')
    list_editable = ('status', 'date')
    list_order    = ('-date',)
    search_fields = ('title', 'text', 'tags__name')
    list_display_links = 'title',
    date_hierarchy = 'date'
admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display  = ('__unicode__', 'date', 'status', 'post', 'url', 'nickname', 'author', 'email', 'ip', 'text')
    list_filter   = ('status', 'authenticated', 'author')
    list_order    = ('-date',)
    search_fields = ('text', 'nickname', 'email', 'url', 'post__title', 'ip')
    list_editable = ('status',)
    list_display_links = '__unicode__',
    date_hierarchy = 'date'
admin.site.register(Comment, CommentAdmin)

