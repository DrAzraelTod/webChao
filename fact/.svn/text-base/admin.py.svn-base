from webchao.fact.models import Fact
from django.contrib import admin

class FactAdmin(admin.ModelAdmin):
    list_display  = ('id', 'nickname', 'fact', 'channel')
    list_filter   = ('channel', 'nickname')
    list_editable = ('nickname',)
    search_fields = ('fact', 'nickname', 'channel')
    list_order    = ('-id',)
    list_display_links = 'id',
admin.site.register(Fact, FactAdmin)
