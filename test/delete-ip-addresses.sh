#!/bin/bash

for (( i=1; i<256; i++)); do
    sudo ifconfig lo0 -alias 192.168.2.$i
    sudo ifconfig lo0 -alias 192.168.3.$i
done
