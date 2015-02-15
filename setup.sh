#!/bin/bash

HOME="/home/cubie"

if [ ! -e $HOME/ramdisk/db.sqlite ]; then
    mount -osize=16m tmpfs $HOME/ramdisk -t tmpfs
    chmod 777 $HOME/ramdisk
    cp $HOME/db.sqlite $HOME/ramdisk
fi
