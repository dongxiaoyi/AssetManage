# _*_coding:utf-8_*_
from __future__ import unicode_literals
import os,sys,subprocess
os.path.join(os.path.dirname(__file__),'../../..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AssetManage.settings')
import django
django.setup()
import os.path, datetime, glob, time, gzip, re
from weblog.models import WebLog

def get_log_cutting_list():
    list_files = glob.glob('/var/log/nginx/*log*gz')
    list_files_timestamp = {}
    for file in list_files:
        list_files_timestamp[str(file)] = str(datetime.datetime.fromtimestamp(os.path.getmtime(file))).split(' ')[0]
    now = datetime.datetime.now()
    now_formatted = now.strftime("%Y-%m-%d")
    log_cutting_list = []
    for file, mtime in list_files_timestamp.items():
        file = file
        mtime_timestamp = time.mktime(time.strptime(mtime, "%Y-%m-%d"))
        now_timestamp = time.mktime(time.strptime(str(now_formatted), "%Y-%m-%d"))
        if int(mtime_timestamp) == int(now_timestamp):
            log_cutting_list.append(file)
    return log_cutting_list


def get_data_log(log):
    with gzip.open(log, 'r') as logfile:
        for line in logfile:
            yield line


def log_sql_data():
    log_list = get_log_cutting_list()
    for log in log_list:
        data = get_data_log(log)
        if getattr(data, '__iter__', None):
            for line in data:
                matchdata = re.match(r'(.*) - (.*) \[(.*)\] \"(.*) (\/.*) (.*)\" (.*) (.*) \"(.*)\" \"(.*)\" \"(.*)\"',
                                     line, re.I)
                if matchdata != None:
                    remote_addr = matchdata.group(1)
                    remote_user = matchdata.group(2)
                    time_local = matchdata.group(3)
                    method = matchdata.group(4)
                    request = matchdata.group(5)
                    status = matchdata.group(7)
                    body_bytes_sent = matchdata.group(8)
                    http_referer = matchdata.group(9)
                    http_user_agent = matchdata.group(10)

                    add_log_record = WebLog.objects.create(logname=str(log),
                                                           remote_addr=str(remote_addr),
                                                           remote_user=str(remote_user),
                                                           time_local=str(time_local),
                                                           method=str(method),
                                                           request=str(request),
                                                           status=str(status),
                                                           body_bytes_sent=str(body_bytes_sent),
                                                           http_referer=str(http_referer),
                                                           http_user_agent=str(http_user_agent))
                    add_log_record.save()


