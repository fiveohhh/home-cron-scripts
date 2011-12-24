#!/usr/bin/python

from TStat import *
import sqlite3
import time

t = TStat('10.12.34.139')
tempInFahr = t.getCurrentTemp()
tempInKelv = (tempInFahr + 459.67) *.555556
tempInsertVal = int(round(tempInKelv*100))

currentTime = int(round(time.time()))
conn = sqlite3.connect('/home/andy/djangoProjects/leeHouseSite/sqlite/db.sql3')
c = conn.cursor()
# 50 is sensor val for kitchen
c.execute("insert into restInterface_temp_entry values (NULL," + str(currentTime) + ",50," + str(tempInsertVal) + ")")
conn.commit()

