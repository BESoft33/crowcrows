from django.contrib import admin
from .models import *


# Register your models here.
# @admin.register(Blogger)
class BloggerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email',)
    model = Author


class ModeratorAdmin(admin.ModelAdmin):
    model = Moderator

class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'role')

admin.site.register(Author, BloggerAdmin)
admin.site.register(Editor, BloggerAdmin)
admin.site.register(Moderator, ModeratorAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(ActivityLog)