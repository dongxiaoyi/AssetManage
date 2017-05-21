#_*_coding:utf-8_*_
from __future__ import unicode_literals

import os,sys,subprocess,commands
import json
cmd = 'ifconfig'
cmd_head = str(cmd).split(' ')[0]
space = ' '
cmd_body = space.join(str(cmd).split(' ')[1:])
cmd_head_which = commands.getoutput('/usr/bin/which %s' % cmd_head)
cmd_head = str(cmd_head_which)
cmd = cmd_head + ' ' + cmd_body
cmd = "salt-call cmd.run \'" + cmd + "\'"
result = []
minions = ['mariadb',]
for minion in minions:
    command = "salt " + "\'" + str(minion) + "\' " + "cmd.run " + "\'" + cmd + "\'"
    print command
    docommand = subprocess.Popen(command, stdout=subprocess.PIPE,shell=True)
    stdout = docommand.communicate()[0].decode('unicode_escape')
    print stdout

    #for cmd_line in stdout.split('\n'):
    #    if cmd_line.split(':')[0] in minionlist:
    #        cmd_line = cmd_line.replace(cmd_line,
    #                                    '<ul class="nav nav-pills nav-stacked"><li class="active"><a href="#">' + minion + '</a></li></ul>')
    #    else:
    #        cmd_line = cmd_line.replace(cmd_line, '<code>' + cmd_line + '</code>')
    #    result.append(cmd_line)
#return result
