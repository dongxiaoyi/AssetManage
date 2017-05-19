#_*_coding:utf-8_*_
from __future__ import absolute_import
import os
import celery
from celery import Celery,platforms
from django.conf import settings
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AssetManage.settings')
app = Celery('celery',broker='redis://192.168.0.5:6379/0',backend='redis://192.168.0.5:6379/1')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
platforms.C_FORCE_ROOT = True

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))



