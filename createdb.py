#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sqlite3
import sys

from config import DB_PATH


if os.path.exists(DB_PATH):
    print("ERROR: File already exists: %s" % DB_PATH)
    sys.exit(2)

db = sqlite3.connect(DB_PATH)
cursor = db.cursor()
cursor.execute("CREATE TABLE users (username vchar(25) PRIMARY KEY, password vchar(255) default '', enable boolean default 0, maxallow SMALLINT unsigned default 1, until datetime default '2055-01-01 00:00:00');")
print("* Users database created at %s" % DB_PATH)
