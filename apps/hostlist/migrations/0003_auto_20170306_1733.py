# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-03-06 17:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hostlist', '0002_auto_20170306_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostlist',
            name='nocn',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='hostlist.NetworkOperator', verbose_name='\u8fd0\u8425\u5546\u5168\u79f0'),
        ),
    ]
