# Generated by Django 4.0.1 on 2024-01-21 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crowapp', '0005_user_current_login_ip_user_last_login_ip_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
