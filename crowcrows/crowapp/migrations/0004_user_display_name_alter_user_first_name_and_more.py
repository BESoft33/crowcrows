# Generated by Django 4.0.1 on 2024-01-21 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crowapp', '0003_alter_author_options_alter_editor_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='display_name',
            field=models.CharField(default=models.CharField(max_length=255), max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=255),
        ),
    ]
