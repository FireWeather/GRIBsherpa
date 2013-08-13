#!/usr/bin/python3
# -*- coding: utf-8 -*-
# --------------------------------------------------------
# Copyright (c) 2013 Matthew Pate and Daniel Catalano
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source distribution
# of this software for license terms.
# --------------------------------------------------------


import psycopg2
import sys

con = None

try:
    con = psycopg2.connect(database='vagrant', user='vagrant')
    cur = con.cursor()
    cur.execute('SELECT version()')
    ver = cur.fetchone()
    print( ver )

except (psycopg2.DatabaseError, e):
    print( 'Error %s' % e)
    sys.exit(1)

finally:

    if con:
        con.close()
