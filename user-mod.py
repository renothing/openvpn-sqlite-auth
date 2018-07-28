#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import os
import sqlite3
import sys
import datetime
from getpass import getpass

from config import DB_PATH, PASSWORD_LENGTH_MIN, HASH_ALGORITHM


def fstr(s):
    try:
        return int(s)
    except ValueError:
        return None
if len(sys.argv) != 2:
    print("USAGE: %s <username>" % sys.argv[0])
    sys.exit(1)
if not os.path.exists(DB_PATH):
    print("ERROR: Database not found: %s" % DB_PATH)

hash_func = getattr(hashlib, HASH_ALGORITHM, None)
if hash_func is None:
    print("ERROR: Hashing algorithm '%s' not found" % HASH_ALGORITHM)
    sys.exit(2)

username = sys.argv[1]
menu=("change user password", "change user stauts", "change user expiration", "change user max concurrent", "Exit")

choice = False
while not choice:
    for i in range(len(menu)):
        print(i,menu[i])
    choice = input("\n* Please select operation: ")
    if fstr(choice) in range(len(menu)):
        choice = fstr(choice)
        break
    choice = False
    
if choice == 0:
    password_ok = False
    while not password_ok:
        password = getpass()
        if len(password) < PASSWORD_LENGTH_MIN:
            print("ERROR: password must be at least %d characters long" % PASSWORD_LENGTH_MIN)
            continue
        password_confirm = getpass('Confirm: ')
        if password == password_confirm:
            password_ok = True
        else:
            print("ERROR: passwords don't match")
        password = hash_func(password.encode("UTF-8")).hexdigest()
elif choice == 1:
    enable = input("please enter user status(0:disable,1:enabled):")
    enable = 1 if fstr(enable) else 0
        
elif choice == 2:
    expiration = input("please enter available days for user:")
    if fstr(expiration):
        until = datetime.datetime.now() + datetime.timedelta(days=fstr(expiration))
    else:
        until = datetime.datetime.strptime('2055-01-01 00:00:00','%Y-%m-%d %H:%M:%S')

elif choice == 3:
    maxallow = input("please enter user max concurrent connections (small than 127):")
    maxallow = fstr(maxallow) if fstr(maxallow) else 1

else:
    sys.exit(0)

db = sqlite3.connect(DB_PATH)
cursor = db.cursor()
try:
    if choice == 0:
        cursor.execute("update users set password = ? where username = ?;", (password, username))
    elif choice == 1:
        cursor.execute("update users set enable = ? where username = ?;", (enable, username))
    elif choice == 2:
        cursor.execute("update users set until = ? where username = ?;", (until, username))
    elif choice == 3:
        cursor.execute("update users set maxallow = ? where username = ?;", (maxallow, username))
except sqlite3.IntegrityError:
    print("ERROR: something wrong with '%s'" % username)
    sys.exit(2)
db.commit()
print("* User %s successfully updated" % username)
