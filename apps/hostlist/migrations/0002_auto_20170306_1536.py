# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-03-06 15:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hostlist', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dzhuser',
            name='username',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u7528\u6237\u540d'),
        ),
        migrations.AlterField(
            model_name='hostlist',
            name='catagorycn',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='hostlist.Catagory', verbose_name='\u7c7b\u522b'),
        ),
        migrations.AlterField(
            model_name='hostlist',
            name='dccn',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='hostlist.DataCenter', verbose_name='\u673a\u623f\u5168\u79f0'),
        ),
        migrations.AlterField(
            model_name='hostlist',
            name='engineer',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='hostlist.Dzhuser', verbose_name='\u7ef4\u62a4\u4eba\u5458'),
        ),
        migrations.AlterField(
            model_name='hostlist',
            name='nocn',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hostlist.NetworkOperator', verbose_name='\u8fd0\u8425\u5546\u5168\u79f0'),
        ),
        migrations.AlterField(
            model_name='hostlist',
            name='pacn',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hostlist.ProvinceArea', verbose_name='\u5730\u533a\u5168\u79f0'),
        ),
    ]
