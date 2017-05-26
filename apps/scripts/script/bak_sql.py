#!/usr/bin/env python
# --coding:utf8--
import subprocess,os,sys,shutil

from time import time,localtime,strftime
Now = strftime('%Y-%m-%d',localtime(time()))
RemoteIp = '192.168.0.5'
RemotePort = '3306'
BakDataDir = '/data/bakdata'
BakDataDirDay = ('%s/%s' % (BakDataDir,Now))
User = "sk"
PassWd = 'sk927312'
MySQL = '`/usr/bin/which mysql`'
MySQLDump = '`/usr/bin/whcih mysqldump`'

get_db_name = ("%s -u%s -p%s -e \"SELECT schema_name FROM information_schema.schemata where schema_name not in (\'information_schema\',\'sys\',\'performance_schema\')\" --skip-column-names" % (MySQL,User,PassWd))
get_db = subprocess.Popen(get_db_name, stdout=subprocess.PIPE, shell=True)
stdout = get_db.communicate()[0].decode('unicode_escape')
db=[]
for db_name in str(stdout).strip().split("\n"):
	db.append(db_name)

def Dump():
    if os.path.exists(BakDataDir):
        if os.path.exists(BakDataDirDay):
            for db_name in db:
                bak_cmd = ('%s --master-data=2 --single-transaction  --routines --triggers --events -u%s -p%s -h %s -P %s %s|gzip >%s/%s-%s.sql' % (MySQLDump,User,PassWd,RemoteIp,RemotePort,db_name,BakDataDir,RemoteIp,db_name))
                bak_sql = subprocess.Popen(bak_cmd, shell=True)
                bak_sql.wait()
        else:
            os.mkdir(BakDataDirDay)
            for db_name in db:
                bak_cmd = ('%s --master-data=2 --single-transaction  --routines --triggers --events -u%s -p%s -h %s -P %s %s|gzip >%s/%s-%s.sql' % (MySQLDump, User, PassWd, RemoteIp, RemotePort,db_name, BakDataDir, RemoteIp, db_name))
                bak_sql = subprocess.Popen(bak_cmd, shell=True)
                bak_sql.wait()
    else:
        for db_name in db:
            os.makedirs(BakDataDirDay)
            bak_cmd = ('%s --master-data=2 --single-transaction  --routines --triggers --events -u%s -p%s -h %s -P %s %s|gzip >%s/%s-%s.sql' % (MySQLDump, User, PassWd, RemoteIp, RemotePort,db_name, BakDataDir, RemoteIp, db_name))
            bak_sql = subprocess.Popen(bak_cmd, shell=True)
            bak_sql.wait()
if __name__ == '__main__':
    Dump()

#!/usr/bin/env python
# --coding:utf8--
import subprocess,shutil
def delete():
    get_del_dir_cmd = "find /data/bakdata/ -type d -mtime -1 -name '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'"
    get_del_dir = subprocess.Popen(get_del_dir_cmd,stdout=subprocess.PIPE, shell=True)
    stdout = get_del_dir.communicate()[0].decode('unicode_escape')
    for dir in str(stdout).strip().split('\n'):
        shutil.rmtree(str(dir))

if __name__ == '__main__':
    delete()