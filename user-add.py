#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import os
import sqlite3
import sys
from getpass import getpass

from config import DB_PATH, PASSWORD_LENGTH_MIN, HASH_ALGORITHM


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
enable=True
db = sqlite3.connect(DB_PATH)
cursor = db.cursor()
try:
    cursor.execute("INSERT INTO users(username,password,enable) VALUES (?, ?, ?);", (username, password,enable))
except sqlite3.IntegrityError:
    print("ERROR: user '%s' already exists" % username)
    sys.exit(2)
db.commit()

print("* User %s successfully created" % username)
