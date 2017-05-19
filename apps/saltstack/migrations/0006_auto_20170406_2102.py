# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-04-06 21:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fileupload', '0007_remove_uploadfiles_groups'),
        ('saltstack', '0005_auto_20170406_2100'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='file',
        ),
        migrations.AddField(
            model_name='service',
            name='file',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fileupload.UploadFiles', verbose_name='\u914d\u7f6e\u9644\u4ef6'),
        ),
    ]
