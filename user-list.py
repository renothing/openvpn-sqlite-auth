#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sqlite3
import sys

from config import DB_PATH


if not os.path.exists(DB_PATH):
    print("ERROR: Database not found: %s" % DB_PATH)
    sys.exit(2)

db = sqlite3.connect(DB_PATH)
cursor = db.cursor()

cursor.execute("SELECT username,enable,maxallow,until FROM users;")
results = cursor.fetchall()

print("username - enabled - maxallow - expired:")
for res in results:
    print("%-14s %-4d %-2d %-20s" % res)
