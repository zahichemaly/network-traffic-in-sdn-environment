import hpsdnclient as hp
import sys
import ast
import socket
from multiprocessing import Queue

#get IP of eth0
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8',1))

#configuration
controller=s.getsockname()[0]
auth=hp.XAuthToken(user='sdn',password='skyline',server=controller)
api=hp.Api(controller=controller,auth=auth)

# flow template (first flow in the first datapath)
id = api.get_datapaths()[0].dpid
flow_temp = api.get_flows(id)[0]
flow_temp.byte_count='0'
flow_temp.match.eth_type="ipv4"
flow_temp.match.eth_dst = ""
flow_temp.match.eth_src = ""
flow_temp.priority="30005"

# connected hosts
hosts = api.get_nodes()


def insert_flow(ipsrc, ipdst, inPort, outPort, dpid):
	flow = flow_temp
	flow.actions.output = outPort
	flow.match.in_port = inPort
	flow.match.ipv4_src = ipsrc
	flow.match.ipv4_dst = ipdst
	api.add_flows(dpid,flow)

def get_endhost_port(ip):
	i = 0
	while (i < len(hosts)):
		if (hosts[i].ip == ip):
			port = hosts[i].port # dst port of the host (by ip)
			return port
		i += 1
	return 0

def get_link(firstSwitch, nextSwitch):
	links = api.get_links(firstSwitch)
	i = 0
	while (i < len(links)):
		if (links[i].dst_dpid == nextSwitch):
			return links[i]
		i += 1
	return None

def create_path(ipSrc, ipDst, switches):
	nextPorts = Queue()
	# first switch
	link = get_link(switches[0], switches[1])
	outPort = link.src_port #get outport from the next switch
	nextPorts.put(link.dst_port)
	inPort = get_endhost_port(ipSrc)
	insert_flow(ipSrc, ipDst, inPort, outPort, switches[0])
	# next switches
	i = 1
	while (i < len(switches)-1):
		link = get_link(switches[i], switches[i+1])
		outPort = link.src_port
		nextPorts.put(link.dst_port) # enqeue inport port of switch i
		inPort = nextPorts.get() # get dst port of switch i-1 => inport of switch i
		insert_flow(ipSrc, ipDst, inPort, outPort,switches[i])
		i += 1
	# last switch
	index = len(switches)-1
	inPort = nextPorts.get()
	outPort = get_endhost_port(ipDst)
	insert_flow(ipSrc, ipDst, inPort, outPort,switches[index])


ipSrc = sys.argv[1]
ipDst = sys.argv[2]
switches = ast.literal_eval(sys.argv[3])

create_path(ipSrc,ipDst,switches)
