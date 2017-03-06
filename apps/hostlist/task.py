#_*_coding:utf-8_*_
from AssetManage.celery import app

@app.task
def GetHostList():
    pass