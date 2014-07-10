#!/usr/bin/python
'''
    Gets the current temperature from the thermostat in 
    Kitchen 
'''
from TStat import *
import time
import requests
t = TStat('thermostat-FD-BB-6F.chiefmarley.local')
try:
    tempInFahr = t.getCurrentTemp()
    tempInKelv = ((tempInFahr - 32) *.555556) + 273.15
    tempInsertVal = int(round(tempInKelv*100))
    requests.get('http://127.0.0.1/restInterface/msg/TMP50' + str(tempInsertVal))
except:
    pass
