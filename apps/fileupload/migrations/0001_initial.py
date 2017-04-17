# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-04-02 18:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('saltstack', '0003_auto_20170330_1526'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u6587\u4ef6\u540d')),
                ('groups', models.ManyToManyField(blank=True, null=True, to='saltstack.Service', verbose_name='\u6240\u5c5e\u670d\u52a1')),
            ],
            options={
                'verbose_name': '\u4e0a\u4f20\u6587\u4ef6',
                'verbose_name_plural': '\u4e0a\u4f20\u6587\u4ef6',
            },
        ),
    ]