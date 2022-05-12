from django.contrib import admin
from .models import *
# Register your models here.
# @admin.register(Blogger)
class BloggerAdmin(admin.ModelAdmin):
    # model=Blogger
    list_display=('first_name', 'last_name')

# @admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display=('blogger','title','published_on',)
    model=Article

admin.site.register(Article, ArticleAdmin)
admin.site.register(Blogger,BloggerAdmin)