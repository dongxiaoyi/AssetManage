# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-04-20 02:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_auto_20170420_0138'),
    ]

    operations = [
        migrations.CreateModel(
            name='MasterProcessStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updatetime', models.CharField(blank=True, max_length=30, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('status', models.CharField(blank=True, max_length=30, verbose_name='\u72b6\u6001')),
            ],
            options={
                'verbose_name': 'master\u8fdb\u7a0b\u72b6\u6001',
                'verbose_name_plural': 'master\u8fdb\u7a0b\u72b6\u6001',
            },
        ),
    ]