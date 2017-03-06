#_*_coding:utf-8_*_
#from __future__ import absolute_import
#import os
#import django
#
#from celery import Celery
#from django.conf import settings
#
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AssetManage.settings')
#django.setup()
#
#app = Celery('hostlist','users')
#
#app.config_from_object('django.conf:settings')
#app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)