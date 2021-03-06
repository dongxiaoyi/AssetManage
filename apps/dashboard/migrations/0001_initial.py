# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-04-19 02:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hostlist', '0006_auto_20170407_2352'),
    ]

    operations = [
        migrations.CreateModel(
            name='MinionLoadAvg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('one', models.CharField(blank=True, max_length=30, verbose_name='1 min')),
                ('five', models.CharField(blank=True, max_length=30, verbose_name='5 min')),
                ('fifteen', models.CharField(blank=True, max_length=30, verbose_name='15 min')),
                ('processes', models.CharField(blank=True, max_length=30, verbose_name='\u8fd0\u884c\u8fdb\u7a0b\u6570/\u603b\u8fdb\u7a0b\u6570')),
                ('nowprocesspid', models.CharField(blank=True, max_length=30, verbose_name='\u6700\u8fd1\u8fd0\u884c\u7ecf\u5e38PID')),
                ('updatetime', models.CharField(blank=True, max_length=30, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('minionid', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='hostlist.AccHostList', verbose_name='minionid')),
            ],
            options={
                'verbose_name': 'minion\u8d1f\u8f7d',
                'verbose_name_plural': 'minion\u8d1f\u8f7d',
            },
        ),
    ]
