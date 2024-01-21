from django.contrib import admin
from .models import *


# Register your models here.
# @admin.register(Blogger)
class BloggerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'role',)


# @admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'title', 'published_on',)
    model = Article


admin.site.register(Article, ArticleAdmin)
admin.site.register(Author, BloggerAdmin)
admin.site.register(Subscriber, BloggerAdmin)
admin.site.register(Editor, BloggerAdmin)
