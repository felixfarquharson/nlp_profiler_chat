# Generated by Django 3.2.4 on 2021-06-06 16:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_delete_logintime'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lastseen',
            old_name='person',
            new_name='user',
        ),
    ]
