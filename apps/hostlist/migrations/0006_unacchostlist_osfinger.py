# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-03-08 20:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostlist', '0005_auto_20170308_1743'),
    ]

    operations = [
        migrations.AddField(
            model_name='unacchostlist',
            name='osfinger',
            field=models.CharField(blank=True, default=b'linux', max_length=60, null=True, verbose_name=b'OS'),
        ),
    ]
