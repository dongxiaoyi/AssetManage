# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-05-31 07:16
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WebLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logname', models.CharField(max_length=15, verbose_name='app\u540d\u79f0')),
                ('remote_addr', models.CharField(max_length=15, verbose_name='\u76ee\u6807IP')),
                ('remote_user', models.CharField(max_length=255, verbose_name='\u76ee\u6807\u7528\u6237')),
                ('time_local', models.CharField(max_length=255, verbose_name='\u672c\u5730\u65f6\u95f4')),
                ('method', models.CharField(max_length=255, verbose_name='\u65b9\u6cd5')),
                ('request', models.CharField(max_length=255, verbose_name='request')),
                ('status', models.CharField(max_length=255, verbose_name='\u72b6\u6001')),
                ('body_bytes_sent', models.CharField(max_length=255, verbose_name='\u4e3b\u4f53\u5927\u5c0f')),
                ('http_referer', models.CharField(max_length=255, verbose_name='\u6765\u81ea\u94fe\u63a5')),
                ('http_user_agent', models.CharField(max_length=255, verbose_name='\u5ba2\u6237\u7aef')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u6dfb\u52a0\u65f6\u95f4')),
            ],
            options={
                'verbose_name': 'WebLog',
                'verbose_name_plural': 'WebLog',
            },
        ),
    ]