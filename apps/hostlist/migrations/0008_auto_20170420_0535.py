# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-04-20 05:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostlist', '0007_auto_20170420_0513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acchostlist',
            name='mem_total',
            field=models.CharField(blank=True, max_length=99999, null=True, verbose_name=b'Mem\xe6\x80\xbb\xe9\x87\x8f'),
        ),
    ]
