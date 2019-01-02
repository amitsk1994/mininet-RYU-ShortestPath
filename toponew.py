#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8', autoStaticArp=False)

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=RemoteController,
                         ip= '127.0.0.1',
                      port=6633)

    info( '*** Add switches\n')
    sw1 = net.addSwitch('sw1', cls=OVSKernelSwitch)
    sw2 = net.addSwitch('sw2', cls=OVSKernelSwitch)
    sw3 = net.addSwitch('sw3', cls=OVSKernelSwitch)
    sw4 = net.addSwitch('sw4', cls=OVSKernelSwitch)
    sw5 = net.addSwitch('sw5', cls=OVSKernelSwitch)
    sw6 = net.addSwitch('sw6', cls=OVSKernelSwitch)
    sw7 = net.addSwitch('sw7', cls=OVSKernelSwitch)
    sw8 = net.addSwitch('sw8', cls=OVSKernelSwitch)
    sw9 = net.addSwitch('sw9', cls=OVSKernelSwitch)
    sw10 = net.addSwitch('sw10', cls=OVSKernelSwitch)
    sw11 = net.addSwitch('sw11', cls=OVSKernelSwitch)
    sw12 = net.addSwitch('sw12', cls=OVSKernelSwitch)
    sw13 = net.addSwitch('sw13', cls=OVSKernelSwitch)
    sw14 = net.addSwitch('sw14', cls=OVSKernelSwitch)
    sw15 = net.addSwitch('sw15', cls=OVSKernelSwitch)
    sw16 = net.addSwitch('sw16', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.1.0.1',mac='00:00:00:00:00:01', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.1.0.2',mac='00:00:00:00:00:02', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='10.1.0.3',mac='00:00:00:00:00:03', defaultRoute=None)

    #Chicago
    s1 = net.addHost('s1', cls=Host, ip='10.0.0.1',mac='00:00:00:00:00:11', defaultRoute=None)#file server
    s2 = net.addHost('s2', cls=Host, ip='10.0.0.2',mac='00:00:00:00:00:12', defaultRoute=None)#email server
    s3 = net.addHost('s3', cls=Host, ip='10.0.0.3',mac='00:00:00:00:00:13', defaultRoute=None)#web server
    s4 = net.addHost('s4', cls=Host, ip='10.0.0.4',mac='00:00:00:00:00:14', defaultRoute=None)#backup server
    #NewYork
    s5 = net.addHost('s5', cls=Host, ip='10.0.1.1',mac='00:00:00:00:00:21', defaultRoute=None)#file server
    s6 = net.addHost('s6', cls=Host, ip='10.0.1.2',mac='00:00:00:00:00:22', defaultRoute=None)#email server
    s7 = net.addHost('s7', cls=Host, ip='10.0.1.3',mac='00:00:00:00:00:23', defaultRoute=None)#web server
    s8 = net.addHost('s8', cls=Host, ip='10.0.1.4',mac='00:00:00:00:00:24', defaultRoute=None)#backup server
    #Seattle
    s9 = net.addHost('s9', cls=Host, ip='10.0.2.1',mac='00:00:00:00:00:31', defaultRoute=None)#file server
    s10 = net.addHost('s10', cls=Host, ip='10.0.2.2',mac='00:00:00:00:00:32', defaultRoute=None)#email server
    s11 = net.addHost('s11', cls=Host, ip='10.0.2.3',mac='00:00:00:00:00:33', defaultRoute=None)#web server
    s12 = net.addHost('s12', cls=Host, ip='10.0.2.4',mac='00:00:00:00:00:34', defaultRoute=None)#backup server
    info( '*** Add links\n')
    net.addLink(s1, sw1)
    net.addLink(s2, sw1)
    net.addLink(s3, sw2)
    net.addLink(s4, sw2)
    net.addLink(sw1, sw3)
    net.addLink(sw2, sw4)
    net.addLink(sw2, sw3)
    net.addLink(sw1, sw4)

    net.addLink(s5, sw5)
    net.addLink(s6, sw5)
    net.addLink(s7, sw6)
    net.addLink(s8, sw6)
    net.addLink(sw5, sw7)
    net.addLink(sw6, sw8)
    net.addLink(sw6, sw7)
    net.addLink(sw5, sw8)

    net.addLink(s9, sw9)
    net.addLink(s10, sw9)
    net.addLink(s11, sw10)
    net.addLink(s12, sw10)
    net.addLink(sw9, sw11)
    net.addLink(sw10, sw12)
    net.addLink(sw10, sw11)
    net.addLink(sw9, sw12)

    net.addLink(h1, sw13)
    net.addLink(h2, sw14)
    net.addLink(h3, sw16)

    net.addLink(sw3, sw13)
    net.addLink(sw3, sw14)
    net.addLink(sw4, sw14)
    net.addLink(sw7, sw13)
    net.addLink(sw7, sw14)
    net.addLink(sw7, sw15)
    net.addLink(sw8, sw15)
    net.addLink(sw8, sw16)
    net.addLink(sw11, sw14)
    net.addLink(sw12, sw15)
    net.addLink(sw12, sw16)


    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('sw1').start([c0])
    net.get('sw2').start([c0])
    net.get('sw3').start([c0])
    net.get('sw4').start([c0])
    net.get('sw5').start([c0])
    net.get('sw6').start([c0])
    net.get('sw7').start([c0])
    net.get('sw8').start([c0])
    net.get('sw9').start([c0])
    net.get('sw10').start([c0])
    net.get('sw11').start([c0])
    net.get('sw12').start([c0])
    net.get('sw13').start([c0])
    net.get('sw14').start([c0])
    net.get('sw15').start([c0])
    net.get('sw16').start([c0])

    info( '*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()


