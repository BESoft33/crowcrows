# Generated by Django 4.0.1 on 2024-07-09 09:14

import users.managers
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('display_name', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('profile_img', models.ImageField(default='placeholder.png', upload_to='images')),
                ('role', models.CharField(choices=[('READER', 'reader'), ('AUTHOR', 'author'), ('EDITOR', 'editor'), ('MODERATOR', 'moderator'), ('ADMIN', 'admin')], default='READER', max_length=25)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('current_login_ip', models.GenericIPAddressField(blank=True, null=True)),
                ('last_login_ip', models.GenericIPAddressField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'permissions': [('can_view_article', 'Can read an Article')],
            },
        ),
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_type', models.CharField(choices=[('Create', 'Create'), ('Read', 'Read'), ('Update', 'Update'), ('Delete', 'Delete'), ('Login', 'Login'), ('Logout', 'Logout'), ('Login Failed', 'Login Failed')], max_length=15)),
                ('action_time', models.DateTimeField(auto_now_add=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Success', 'Success'), ('Failed', 'Failed')], default='Success', max_length=7)),
                ('data', models.JSONField(default=dict)),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('actor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype')),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
            ],
            options={
                'permissions': [('can_add_editorial', 'Can create an Editorial'), ('can_change_editorial', 'Can modify an Editorial'), ('can_view_editorial', 'Can view an Editorial'), ('can_delete_editorial', 'Can delete an Editorial'), ('can_schedule_publish_editorial', 'Can schedule the Editorial to publish'), ('can_add_article', 'Can add an Article'), ('can_change_article', 'Can update an Article'), ('can_view_article', 'Can view an Article'), ('can_delete_article', 'Can delete an Article'), ('can_approve_article', 'Can approve an Article to publish'), ('can_schedule_publish_article', 'Can schedule an Article to publish'), ('can_view_author', 'Can view the author of article'), ('can_add_author', 'Can add a new Author'), ('can_change_author', 'Can modify an Author'), ('can_delete_author', 'Can delete the author')],
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('users.user',),
            managers=[
                ('objects', users.managers.AdminManager()),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
            ],
            options={
                'permissions': [('can_add_article', 'Can create an Article'), ('can_view_article', 'Can view an Article'), ('can_publish_article', 'Can publish an Article'), ('can_schedule_publish_article', 'Can schedule an Article to publish')],
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('users.user',),
            managers=[
                ('objects', users.managers.AuthorManager()),
            ],
        ),
        migrations.CreateModel(
            name='Editor',
            fields=[
            ],
            options={
                'permissions': [('can_add_editorial', 'Can create an Editorial'), ('can_change_editorial', 'Can modify an Editorial'), ('can_view_editorial', 'Can view an Editorial'), ('can_delete_editorial', 'Can delete an Editorial'), ('can_schedule_publish_editorial', 'Can schedule the Editorial to publish'), ('can_change_article', 'Can update an Article'), ('can_view_article', 'Can view an Article'), ('can_approve_article', 'Can approve an Article to publish'), ('can_schedule_publish_article', 'Can schedule an Article to publish'), ('can_view_author', 'Can view the author of article')],
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('users.user',),
            managers=[
                ('objects', users.managers.EditorManager()),
            ],
        ),
        migrations.CreateModel(
            name='Moderator',
            fields=[
            ],
            options={
                'permissions': [('can_add_editorial', 'Can create an Editorial'), ('can_change_editorial', 'Can modify an Editorial'), ('can_view_editorial', 'Can view an Editorial'), ('can_delete_editorial', 'Can delete an Editorial'), ('can_schedule_publish_editorial', 'Can schedule the Editorial to publish'), ('can_change_article', 'Can update an Article'), ('can_view_article', 'Can view an Article'), ('can_delete_article', 'Can delete an Article'), ('can_approve_article', 'Can approve an Article to publish'), ('can_schedule_publish_article', 'Can schedule an Article to publish'), ('can_view_author', 'Can view the author of article'), ('can_delete_author', 'Can delete the author')],
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('users.user',),
            managers=[
                ('objects', users.managers.ModeratorManager()),
            ],
        ),
    ]