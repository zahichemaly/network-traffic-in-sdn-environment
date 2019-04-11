
"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import OVSSwitch, Controller, RemoteController

net = Mininet( controller=RemoteController)
c0 = net.addController('c0',controller=RemoteController,ip="192.168.1.74",port=6633)
# Adding
h0 = net.addHost('h0')
s0 = net.addSwitch('s0')
h1 = net.addHost('h1')
net.addLink(h0,s0)
net.addLink(h1,s0)

net.start()
net.pingAll()
CLI(net)


