Joby Take Home Python Coding Test
==========
Tim Sylvester  
timothysylvester@gmail.com  
(408) 334-1700  
Date: June 20, 2022

jping is a Python script that verifies which addresses are pingable on two subnets. It returns a list of IP addresses
that are pingable on one subnet but not the other.

Three options for pinging addresses from Python were evaluated. TheThere were two other options for sending ping packets
from Python

- pythonping module: this required running jping as root to use raw sockets.
- built-in ping command using subprocess: this is reliable and feature rich but slower.
- ping3 module with threads: very fast but occasionally misses a ping message.

Using the ping3 module and the built-in ping command were implemented. The default method is to use the built-in ping
command.

jping is a CLI app with options for specifying the:

- test subnets
- start/end IP addresses
- number of pings to send to an address
- maximum number of ping threads
- list of IP addresses to be skipped based on their last octet
- which method to use to ping addresses.

The code has been tested on Python 3.8 and should work on newer versions. The code has been tested on Mac OSX and should
also work on Linux.

Installing Requirements
----------

    $ pip install -r requirements

Running from Source code
----------

    $ python3 src/jping.py

Command Line Options
---------

    $ python3 src/jping.py  --help
    Usage: jping.py [OPTIONS]
    
      jping - ping test two subnets.
    
    Options:
      -a, --subnet-a TEXT       First subnet to test. (default: 192.168.2)
      -b, --subnet-b TEXT       Second subnet to test. (default: 192.168.3)
      --start INTEGER           Starting IP address in subnet. (default: 1)
      --end INTEGER             Ending IP address in subnet. (default: 254
      -e, --excluded-ips TEXT   Quoted, comma seperated list of IP addresses to be
                                excluded. Example: -e "56, 88, 99".
      -c, --ping-count INTEGER  Number of times to attempt pinging IP address.
                                (default: 5)
      -q, --quiet               Turn off debug messages.
      -p, --ping3               Use ping3 module (faster).
      --help                    Show this message and exit.

Running Tests
----------------
Pytest is used to run two test scripts with a total of 14 tests. To set up the test environment, you must first run
test/add-ip-addresses.sh to add additional IP addresses to the loopback interface (lo0). IP address on the
192.168.2.0/24 and 192.168.3.0/24 are added to the loop back interface. There are

    $ test/add-ip-addresses.sh
    $ python3 -m pytest 



