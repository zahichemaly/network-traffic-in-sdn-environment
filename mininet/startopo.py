
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node , Controller, RemoteController, OVSSwitch
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.util import irange
from mininet.link import TCLink

net = Mininet( controller=RemoteController)
c0 = net.addController('c0',controller=RemoteController,ip="192.168.1.75",port=6633)

class NetworkTopo( Topo ):
    "A simple topology of a double-star access/dist/core."

    def build( self ):

        h1 = self.addHost( 'h1', ip='10.10.2.1/24', defaultRoute='via 10.10.2.254' )
        h2 = self.addHost( 'h2', ip='10.10.2.2/24', defaultRoute='via 10.10.2.254' )
        h3 = self.addHost( 'h3', ip='10.10.2.3/24', defaultRoute='via 10.10.2.254' )
        h4 = self.addHost( 'h4', ip='10.10.2.4/24', defaultRoute='via 10.10.2.254' )
        h5 = self.addHost( 'h5', ip='10.10.2.5/24', defaultRoute='via 10.10.2.254' )
        h6 = self.addHost( 'h6', ip='10.10.2.6/24', defaultRoute='via 10.10.2.254' )
        g1 = self.addHost( 'g1', ip='10.10.2.254/24')
        
        s1 = self.addSwitch( 's1', dpid='0000000000000001',protocols='OpenFlow13' )
        s2 = self.addSwitch( 's2', dpid='0000000000000002',protocols='OpenFlow13' )
        s3 = self.addSwitch( 's3', dpid='0000000000000003',protocols='OpenFlow13' )
        s4 = self.addSwitch( 's4', dpid='0000000000000004',protocols='OpenFlow10' )
        s5 = self.addSwitch( 's5', dpid='0000000000000005',protocols='OpenFlow13' )
        s6 = self.addSwitch( 's6', dpid='0000000000000006',protocols='OpenFlow13' ) 

        #core
        self.addLink ( s1, s2 )

        #distribution
        self.addLink ( s1, s3 )
        self.addLink ( s1, s4 )
        self.addLink ( s1, s5 )
        self.addLink ( s1, s6 )

        self.addLink ( s2, s3 )
        self.addLink ( s2, s4 )
        self.addLink ( s2, s5 )
        self.addLink ( s2, s6 )

        #acccess
        self.addLink( s3, h1 )
        self.addLink( s3, h2 )
        self.addLink( s4, h3 ) 
        self.addLink( s4, h4 ) 
        self.addLink( s5, h5 ) 
        self.addLink( s5, h6 ) 
        self.addLink( s6, g1) 

def run():
    topo = NetworkTopo()
    net = Mininet( topo=topo, controller=c0 )
    net.start()

    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()