from __future__ import absolute_import
from celery import shared_task,task

#@shared_task()
#def add(x,y):
#    # return x + y
#    print x + y
#
#@shared_task()
#def mul(x,y):
#    print "%d * %d = %d" %(x,y,x*y)
#    return x*y
#
#@shared_task()
#def sub(x,y):
#    print "%d - %d = %d"%(x,y,x-y)
#    return x - y
#
#@task(ignore_result=True,max_retries=1,default_retry_delay=10)
#def just_print():
#    print "Print from celery task"
#
from scripts.script.hostsinfo import GetMinionInfo
from scripts.script.dashboardinfo import DashboardInfos
from scripts.script.get_master_info import MasterInfo,Masterprocessstatus,Miniononline

@task
def hostsinfo():
    GetMinionInfo()

@task
def dashboardinfo():
    DashboardInfos()

@task
def masterinfo():
    MasterInfo()

@task
def masterprocessstatus():
    Masterprocessstatus()

@task
def miniononline():
    Miniononline()