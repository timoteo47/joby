#!/bin/bash

for (( i=1; i<256; i++)); do
    sudo ifconfig lo0 -alias 172.168.2.$i
done

#for (( i=1; i<255; i++)); do
#    sudo ifconfig lo0 -alias 172.168.3.$i
#done