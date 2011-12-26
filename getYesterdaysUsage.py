#!/usr/bin/python

from TStat import *
import sqlite3
from datetime import datetime, timedelta
import time

t = TStat('10.12.34.139')
heatUsage = t.getHeatUsageYesterday()
coolUsage = t.getCoolUsageYesterday()

heatMinutes = heatUsage['hour'] * 60 + heatUsage['minute']
coolMinutes = coolUsage['hour'] * 60 + coolUsage['minute']
print str(heatMinutes)
print str(coolMinutes)

currentTime = int(round(time.time()))

conn = sqlite3.connect('/home/andy/djangoProjects/leeHouseSite/sqlite/db.sql3')
c = conn.cursor()
c.execute("insert into restInterface_hvac_runtime values (NULL," + str(currentTime) + "," + str(heatMinutes) +"," + str(coolMinutes) + ")")
conn.commit()

