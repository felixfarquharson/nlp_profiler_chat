# Generated by Django 3.2.4 on 2021-06-06 16:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_lastseen_logintime'),
    ]

    operations = [
        migrations.DeleteModel(
            name='LoginTime',
        ),
    ]
