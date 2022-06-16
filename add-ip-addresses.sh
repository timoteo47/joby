#!/bin/bash

for (( i=1; i<128; i++)); do
    sudo ifconfig lo0 alias 192.168.2.$i
    sudo ifconfig lo0 alias 192.168.3.$i
done

for (( i=128; i<192; i++)); do
    sudo ifconfig lo0 alias 192.168.2.$i
done

for (( i=192; i<255; i++)); do
    sudo ifconfig lo0 alias 192.168.3.$i
done
