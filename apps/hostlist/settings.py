#_*_coding:utf-8_*_
#celery相关
#import djcelery
#djcelery.setup_loader()
#BROKER_URL = 'redis://127.0.0.1:6379/0'
#CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler' # 定时任务
#CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
#CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1'
#CELERY_ACCEPT_CONTENT = ['application/json']
#CELERY_TASK_SERIALIZER = 'json'
#CELERY_RESULT_SERIALIZER = 'json'
#CELERY_TIMEZONE = 'Asia/Shanghai'
#
#INSTALLED_APPS = (
#    'django.contrib.admin',
#    'django.contrib.auth',
#    'django.contrib.contenttypes',
#    'django.contrib.sessions',
#    'django.contrib.messages',
#    'django.contrib.staticfiles',
#    'hostlist',
#    'djcelery',
#    'kombu.transport.django',
#
#)
#TIME_ZONE = 'Asia/Shanghai'
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql',
#        'NAME': 'madking',
#        'USER': 'madking',
#        'PASSWORD': 'moonlight',
#        'HOST': '127.0.0.1',
#        'PORT': '43306',
#
#    }
#}
#