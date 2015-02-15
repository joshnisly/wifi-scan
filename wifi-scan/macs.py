#!/usr/bin/python

_DATA = {}

def _load():
    global _DATA
    _DATA = {}
    for line in open('mac_manufacturers.txt'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        data, ignored, desc = line.partition('#')
        if data[2] != ':':
            continue
        mac, man = data.split()

        _DATA[mac] = (desc or man).strip()


def lookup(mac):
    if not _DATA:
        _load()

    mac = mac[:8].upper()
    
    return _DATA.get(mac)
        
if __name__ == '__main__':
    print lookup('00:01:63')
