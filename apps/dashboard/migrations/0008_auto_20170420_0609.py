# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-04-20 06:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_miniononlinenumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='miniononlinenumber',
            name='all',
            field=models.IntegerField(blank=True, verbose_name='\u603b\u91cf'),
        ),
        migrations.AlterField(
            model_name='miniononlinenumber',
            name='offline',
            field=models.IntegerField(blank=True, verbose_name='\u79bb\u7ebf'),
        ),
        migrations.AlterField(
            model_name='miniononlinenumber',
            name='online',
            field=models.IntegerField(blank=True, verbose_name='\u5728\u7ebf'),
        ),
    ]
