# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-04-03 16:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fileupload', '0004_remove_uploadfiles_filesource'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadfiles',
            name='filesource',
            field=models.FileField(default=1, upload_to='upload/sls/', verbose_name='\u6587\u4ef6\u8def\u5f84'),
            preserve_default=False,
        ),
    ]
