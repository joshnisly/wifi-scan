#!/usr/bin/python

import datetime

from scapy.all import *

import db
import macs

PROBE_REQUEST_TYPE=0
PROBE_REQUEST_SUBTYPE=4

encountered_beacons = {}

# Ignore chromesys
encountered_beacons['chromesys'] = 0

def PacketHandler(pkt):
    if pkt.haslayer(Dot11):
        if pkt.type==PROBE_REQUEST_TYPE and pkt.subtype == PROBE_REQUEST_SUBTYPE:
            PrintRequestPacket(pkt)
        elif pkt.type==PROBE_REQUEST_TYPE and pkt.subtype == 8:
            PrintBeaconPacket(pkt)

def PrintRequestPacket(pkt):
    ssid = pkt.getlayer(Dot11ProbeReq).info
    try:
        ssid = unicode(ssid, 'utf8').encode('utf8', 'replace')
    except:
        print repr(ssid)
        raise
        return

    local = ssid and ssid in encountered_beacons
    if local:
        return

    print "Request: ", datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),

    rssi = calc_rssi(pkt)
    db.register(pkt.addr2, ssid, rssi)
    print "Source: %s SSID: %s RSSi: %d"%(pkt.addr2,ssid,rssi),
    print macs.lookup(pkt.addr2)

def PrintBeaconPacket(pkt):
    ssid = pkt.getlayer(Dot11Beacon).info
    if encountered_beacons.get(ssid, 0) < 3:
        print "Beacon: ", datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
        rssi = calc_rssi(pkt)
        print 'Source: %s SSID: %s RSSi: %d' % (pkt.addr2, ssid, rssi)
    if not ssid in encountered_beacons:
        encountered_beacons[ssid] = 1
    else:
        encountered_beacons[ssid] += 1

def calc_rssi(pkt):
    try:
        extra = pkt.notdecoded
        return -(256-ord(extra[-4:-3]))
    except:
        return None

def main():
    try:
        sniff(iface=sys.argv[1],prn=PacketHandler, store=0)
    except KeyboardInterrupt:
        print 'exiting...'    

if __name__=="__main__":
    main()
