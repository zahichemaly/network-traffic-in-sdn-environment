
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
c0 = net.addController('c0',controller=RemoteController,ip="192.168.1.75",port=6633)
# Adding Hosts/Switches
h0 = net.addHost('h0')
s0 = net.addSwitch('s0')
h1 = net.addHost('h1')
s1 = net.addSwitch('s1')
s2 = net.addSwitch('s2')
# Adding Links
net.addLink(h0,s0)
net.addLink(h1,s1)
net.addLink(s0,s1)
net.addLink(s0,s2)
net.addLink(s2,s1)

#net.build()
net.start()
#net.pingAll()
CLI(net)


