# Generated by Django 4.0.1 on 2024-05-25 05:38

import crowapp.managers
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crowapp', '0013_remove_user_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('crowapp.user',),
            managers=[
                ('objects', crowapp.managers.AdminManager()),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='display_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('READER', 'reader'), ('AUTHOR', 'author'), ('EDITOR', 'editor'), ('MODERATOR', 'moderator'), ('ADMIN', 'admin')], default='READER', max_length=25),
        ),
    ]
