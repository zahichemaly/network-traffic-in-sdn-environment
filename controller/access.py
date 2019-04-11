import hpsdnclient as hp
import sys
import socket

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
flow_temp.priority="65535"

def insert_flow(ipsrc, ipdst, inPort, outPort, dpid):
	flow = flow_temp
	flow.actions.output = outPort
	flow.match.ipv4_src = ipsrc
	flow.match.ipv4_dst = ipdst
	flow.match.in_port = inPort
	api.add_flows(dpid,flow)


def delete_old_flows(dpid, ipSrc):
	for flow in api.get_flows(dpid):
		if (flow.match.ipv4_src == ipSrc):
			api.delete_flows(dpid,flow)


def get_ports(id):
	ports = []
	for p in api.get_ports(id):
		if (p.id != 'LOCAL'):
			ports.append(p.id)
	for p in ports:
		node = api.get_nodes(dpid=id,port=p)
		if ( len(node) != 0):
			ports.remove(p)
	return ports
				

def create_blacklist(ipSrc, id):
	delete_old_flows(id, ipSrc)
	ports = get_ports(id)
	node = api.get_nodes(dpid=id)
	ipDst = node[0].ip
	for port in ports:
		insert_flow(ipSrc,ipDst,port,'0',id)
		

ipSrc = sys.argv[1]
dpid = sys.argv[2]
create_blacklist(ipSrc, dpid)


