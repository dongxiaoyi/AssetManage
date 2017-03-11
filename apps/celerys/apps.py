#_*_encoding:utf-8_*_
from __future__ import unicode_literals
default_app_config = "celerys.apps.CelerysConfig"

from django.apps import AppConfig


class CelerysConfig(AppConfig):
    name = 'celerys'
    verbose_name = u'计划任务与异步队列'
