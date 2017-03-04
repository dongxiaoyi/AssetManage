# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-03-04 17:24
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0010_auto_20170304_1409'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmaliVerifyRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, verbose_name='\u9a8c\u8bc1\u7801')),
                ('email', models.EmailField(max_length=50, verbose_name='\u90ae\u7bb1')),
                ('send_type', models.CharField(choices=[(b'register', '\u6ce8\u518c'), (b'forget', '\u627e\u56de\u5bc6\u7801'), (b'up_email', '\u4fee\u6539\u90ae\u7bb1')], max_length=10, verbose_name='\u9a8c\u8bc1\u7801\u7c7b\u578b')),
                ('send_time', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'\xe5\x8f\x91\xe9\x80\x81\xe6\x97\xb6\xe9\x97\xb4')),
            ],
            options={
                'verbose_name': '\u90ae\u7bb1\u9a8c\u8bc1\u7801',
                'verbose_name_plural': '\u90ae\u7bb1\u9a8c\u8bc1\u7801',
            },
        ),
    ]
