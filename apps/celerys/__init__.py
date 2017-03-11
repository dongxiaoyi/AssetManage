default_app_config = "celerys.apps.CelerysConfig"

from .celery import app as celery_app
import pymysql
pymysql.install_as_MySQLdb()