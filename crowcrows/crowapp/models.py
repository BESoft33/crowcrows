from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import AbstractUser
from .managers import (UserManager, AuthorManager, EditorManager, ModeratorManager, AdminManager, ReaderManager)
from django.utils.translation import gettext_lazy as _

# User Activities
CREATE, READ, UPDATE, DELETE = "Create", "Read", "Update", "Delete"
LOGIN, LOGOUT, LOGIN_FAILED = "Login", "Logout", "Login Failed"
ACTION_TYPES = [
    (CREATE, CREATE),
    (READ, READ),
    (UPDATE, UPDATE),
    (DELETE, DELETE),
    (LOGIN, LOGIN),
    (LOGOUT, LOGOUT),
    (LOGIN_FAILED, LOGIN_FAILED),
]

SUCCESS, FAILED = "Success", "Failed"
ACTION_STATUS = [(SUCCESS, SUCCESS), (FAILED, FAILED)]


class User(AbstractUser):
    class Role(models.IntegerChoices):
        AUTHOR = 1, _("Author")
        EDITOR = 2, _("Editor")
        MODERATOR = 3, _("Moderator")
        ADMIN = 4, _("Admin")
        READER = 5, _("Reader")

    username = None  # To avoid errors because the django team decided to keep default username field required even if I set USERNAME_FIELD to email.
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    profile_img = models.ImageField(upload_to='images', default='placeholder.png')
    role = models.PositiveSmallIntegerField(choices=Role.choices, default=Role.READER)
    last_login = models.DateTimeField(blank=True, null=True)
    current_login_ip = models.GenericIPAddressField(blank=True, null=True)
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.first_name

    def get_display_name(self):
        return self.display_name if self.display_name else self.first_name

    def full_name(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        permissions = [('can_view_article', 'Can read an Article')]


UserModel = get_user_model()


class ActivityLog(models.Model):
    actor = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True)
    action_type = models.CharField(choices=ACTION_TYPES, max_length=15)
    action_time = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True, null=True)
    status = models.CharField(choices=ACTION_STATUS, max_length=7, default=SUCCESS)
    data = models.JSONField(default=dict)

    # for generic relations
    content_type = models.ForeignKey(
        ContentType, models.SET_NULL, blank=True, null=True
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey()

    def __str__(self) -> str:
        return f"{self.action_type} by {self.actor} on {self.action_time}"


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


class Moderator(User):
    objects = ModeratorManager()

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
            ('can_delete_article', 'Can delete an Article'),
            ('can_approve_article', 'Can approve an Article to publish'),
            ('can_schedule_publish_article', 'Can schedule an Article to publish'),
            ('can_view_author', 'Can view the author of article'),
            ('can_delete_author', 'Can delete the author'),
        ]


class Admin(User):
    objects = AdminManager()

    class Meta:
        proxy = True
        permissions = [
            ('can_add_editorial', 'Can create an Editorial'),
            ('can_change_editorial', 'Can modify an Editorial'),
            ('can_view_editorial', 'Can view an Editorial'),
            ('can_delete_editorial', 'Can delete an Editorial'),
            ('can_schedule_publish_editorial', 'Can schedule the Editorial to publish'),
            ('can_add_article', 'Can add an Article'),
            ('can_change_article', 'Can update an Article'),
            ('can_view_article', 'Can view an Article'),
            ('can_delete_article', 'Can delete an Article'),
            ('can_approve_article', 'Can approve an Article to publish'),
            ('can_schedule_publish_article', 'Can schedule an Article to publish'),
            ('can_view_author', 'Can view the author of article'),
            ('can_add_author', 'Can add a new Author'),
            ('can_change_author', 'Can modify an Author'),
            ('can_delete_author', 'Can delete the author'),
        ]


class Reader(User):
    objects = ReaderManager()

    class Meta:
        proxy = True
