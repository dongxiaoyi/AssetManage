# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-03-12 01:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('saltstack', '0002_auto_20170307_1647'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CommonOperate',
        ),
        migrations.DeleteModel(
            name='ConfigUpdate',
        ),
        migrations.DeleteModel(
            name='DangerCommand',
        ),
        migrations.DeleteModel(
            name='DeployModules',
        ),
        migrations.DeleteModel(
            name='ModulesLock',
        ),
    ]
