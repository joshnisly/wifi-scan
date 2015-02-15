#!/usr/bin/python

import datetime
import os
import sqlobject

CONN = None

DB_PATH='/home/cubie/ramdisk/db.sqlite'

class Mac(sqlobject.SQLObject):
    mac = sqlobject.StringCol(length=17, unique=True)

class ProbeRequest(sqlobject.SQLObject):
    mac = sqlobject.ForeignKey('Mac')
    time = sqlobject.DateTimeCol()
    ssid = sqlobject.StringCol()
    rssi = sqlobject.IntCol()


def register(mac, ssid, rssi):
    if not hasattr(sqlobject.sqlhub, 'processConnection'):
        sqlobject.sqlhub.processConnection = sqlobject.connectionForURI('sqlite://' + DB_PATH)
        if not os.path.exists(DB_PATH):
            Mac.createTable()
            ProbeRequest.createTable()

    mac_row = Mac.select(Mac.q.mac==mac)
    if not len(list(mac_row)):
        mac_row = Mac(mac=mac)
    else:
        mac_row = mac_row[0]

    ProbeRequest(mac=mac_row, time=datetime.datetime.now(), ssid=ssid, rssi=rssi)

if __name__ == '__main__':
    register('ac:b3:13:74:7f:f0', 'bogus', -79)
