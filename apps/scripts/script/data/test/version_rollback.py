# -*- coding: utf-8 -*-
import subprocess,os
version = os.getenv('assetmanage_version')
def create_fabfile():
    with open('/tmp/django_rollback.py','w') as file:
        lines = ['# -*- coding: utf-8 -*-\n',
                 'from fabric.api import *\n',
                 "env.user = 'root'\n",
                 "env.password = 'sk927312*'\n",
                 "env.roledefs = {'web':['192.168.0.4',],'db_master':['192.168.0.5',]}\n",
                 '@task\n',
                 '@roles(\'web\')\n',
                 'def rollback():\n',
                 "    run('rm -fr /etc/nginx/html/django && ln -s /data/projects/html/%s /etc/nginx/html/django')\n"  % (version),
                 "    run('kill -HUP `cat /etc/nginx/html/django/uwsgi.pid`')\n",
                 "    run('nginx -t && nginx -s reload')"
                ]
        file.writelines(lines)
def django_rollback():
    cmd = str("fab rollback -f -P /tmp/django_rollback.py")
    rollback_line =subprocess.Popen(cmd,shell=True)
    rollback_line.wait()


if __name__ == '__main__':
    create_fabfile()
    django_rollback()
