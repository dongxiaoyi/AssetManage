# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-04-05 21:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fileupload', '0006_remove_uploadfiles_filesource'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadfiles',
            name='groups',
        ),
    ]
