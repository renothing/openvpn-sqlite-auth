#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright © 2015-11-13 15:38 renothing <frankdot@qq.com>
#
# Distributed under terms of the Apache license.

import os
import sqlite3
import sys
import telnetlib

from config import DB_PATH


if not os.path.exists(DB_PATH):
    print("ERROR: Database not found: %s" % DB_PATH)
    sys.exit(2)

host = '127.0.0.1'
port = 2015
db = sqlite3.connect(DB_PATH)
cursor = db.cursor()

cursor.execute("SELECT username FROM users where enable=0 or until < datetime('now','localtime');")
results = cursor.fetchall()

if __name__ == '__main__':
    if results:
        try:
            tn = telnetlib.Telnet(host,port)
            for res in results:
                tn.write('kill ' + str(res[0]) + '\n')
                print("%s has been kicked out" % res)
        except (RuntimeError, TypeError, NameError,EOFError):
            pass
        finally:
            tn.close() 
