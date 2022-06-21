from pyroute2 import IPDB

ip = IPDB()
with ip.interfaces.lo0 as lo0:
    lo0.add_ip("192.168.0.1/24")
ip.release()
