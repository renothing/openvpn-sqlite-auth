#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright © 2015-11-13 15:38 renothing <frankdot@qq.com>
#
# Distributed under terms of the Apache license.

import telnetlib
import re
from pprint import pprint

host='127.0.0.1'
port=2015

if __name__=='__main__':
    try:
        tn  = telnetlib.Telnet(host,port)
        cmd = tn.write('status\n')
        res = tn.read_until('END\r\n')
	pprint(res)
	connectpref=re.compile(r'^\S+?((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))).*',re.M)
        print connectpref.search(res).group()
        clientpref=re.compile(r'^((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))).*',re.M)
        print clientpref.search(res).group()
    except (RuntimeError, TypeError, NameError,EOFError):
        pass
    finally:
        tn.close() 
