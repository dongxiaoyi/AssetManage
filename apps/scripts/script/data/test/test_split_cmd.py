#_*_coding:utf-8_*_
from __future__ import unicode_literals

import os,sys,subprocess,commands
import json
cmd = 'ps -ef|grep salt'
cmd_head = str(cmd).split(' ')[0]
space = ' '
cmd_body = space.join(str(cmd).split(' ')[1:])
cmd_head_which = commands.getoutput('/usr/bin/which %s' % cmd_head)
cmd_head = str(cmd_head_which)
cmd = cmd_head + ' ' + cmd_body
