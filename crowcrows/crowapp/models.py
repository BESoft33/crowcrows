from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .managers import (UserManager, AuthorManager, EditorManager, SubscriberManager)
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class User(AbstractUser):
    SUBSCRIBED_READER = 'SUBSCRIBED_READER'
    GENERAL_READER = 'GENERAL_READER'
    AUTHOR = 'AUTHOR'
    EDITOR = 'EDITOR'
    ADMIN = 'ADMIN'

    USER_ROLE = (
        (SUBSCRIBED_READER, 'subscriber'),
        (GENERAL_READER, 'reader'),
        (AUTHOR, 'author'),
        (EDITOR, 'editor'),
        (ADMIN, 'admin')
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255, default=first_name)
    email = models.EmailField(unique=True)
    profile_img = models.ImageField(upload_to='images', default='placeholder.png')
    role = models.CharField(choices=USER_ROLE, max_length=25)
    last_login = models.DateTimeField(blank=True, null=True)
    current_login_ip = models.GenericIPAddressField(blank=True, null=True)
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.first_name

    class Meta:
        permissions = [('can_view_article', 'Can read an Article')]


class Author(User):
    objects = AuthorManager()

    class Meta:
        proxy = True
        permissions = [
            ('can_add_article', 'Can create an Article'),
            ('can_view_article', 'Can view an Article'),
            ('can_publish_article', 'Can publish an Article'),
            ('can_schedule_publish_article', 'Can schedule an Article to publish')
        ]


class Editor(User):
    objects = EditorManager()

    class Meta:
        proxy = True
        permissions = [
            ('can_add_editorial', 'Can create an Editorial'),
            ('can_change_editorial', 'Can modify an Editorial'),
            ('can_view_editorial', 'Can view an Editorial'),
            ('can_delete_editorial', 'Can delete an Editorial'),
            ('can_schedule_publish_editorial', 'Can schedule the Editorial to publish'),
            ('can_change_article', 'Can update an Article'),
            ('can_view_article', 'Can view an Article'),
            ('can_approve_article', 'Can approve an Article to publish'),
            ('can_schedule_publish_article', 'Can schedule an Article to publish'),
            ('can_view_author', 'Can view the author of article')
        ]


class Subscriber(User):
    objects = SubscriberManager()

    class Meta:
        proxy = True


class Article(models.Model):
    title = models.CharField(max_length=128, default='')
    published_on = models.DateTimeField(null=True, blank=True)
    content = RichTextUploadingField()
    image = models.ImageField(upload_to='images', blank=True, null=True)
    hide = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    slug = models.SlugField(max_length=128, unique=True, blank=True, null=True)
    created_by = models.ForeignKey(to=Author, on_delete=models.DO_NOTHING, related_name='created_by')
    approved_by = models.OneToOneField(to=Editor, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='approved_by')
    approved_on = models.DateTimeField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug:
            super().save(*args, **kwargs)
        else:
            self.slug = slugify(self.title)
            super().save(*args, **kwargs)


class Editorial(models.Model):
    title = models.CharField(max_length=255)
    content = RichTextField()
    slug = models.SlugField(max_length=128, unique=True)
    created_by = models.OneToOneField(to=Editor, on_delete=models.DO_NOTHING)
    created_on = models.DateTimeField(auto_now=True)
    last_update_on = models.DateTimeField(auto_now_add=True)
    published_on = models.DateTimeField()

    def __str__(self):
        return f"{self.created_by} - {self.title}"

    def save(self, *args, **kwargs):
        if self.slug:
            super().save(*args, **kwargs)
        else:
            self.slug = slugify(self.title)
            super().save(*args, **kwargs)