# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-04-19 06:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='minionloadavg',
            name='minionid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hostlist.AccHostList', verbose_name='minionid'),
        ),
    ]