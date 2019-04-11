## Traffic Engineering in a Software Defined Network (SDN)

This project requires a virtual network such as mininet and a controller to manage the network such as HP SDN Controller.
The user can call intelligent Python scripts via the controller to:
- Redirect the traffic from a source to a destination
- Block a certain traffic passing through a specific switch (In case of a malicious host for example)

### Prerequisites

- **VirtualBox** (https://www.virtualbox.org/wiki/Downloads)
- **mininet VM image** (http://mininet.org/download/)
- **HPE VAN SDN Controller 2.8.8** (http://h30326.www3.hpe.com/hpn/hpe-van-sdn-ctlr-2.8.8-ova.zip?merchantId=MNP_DROPBOX)
- **HP SDN Client** (https://hp-sdn-client.readthedocs.io/en/latest/user/install.html)

### Installation

1. Move the script files inside `\mininet` to the root directory of mininet

2. Move the files inside `\controller` to the root directory of HP SDN Controller

3. Follow [this](https://hp-sdn-client.readthedocs.io/en/latest/user/install.html) tutorial install the hp-sdn-client Python library so you can call the scripts on the controller.


### How to use

* To redirect the traffic between 2 nodes, and passing through specific switches

		python traffic.py "IP_SOURCE" "IP_DESTINATION" ["DPID_SWITCH_1", "DPID_SWITCH_2", ... , "DPID_SWITCH_N"]
		

* To implement an access list on a specific switch:

        python access.py "IP_SOURCE" "DPID_SWITCH"

This script will block all incoming/outcoming traffic from IP_SOURCE (and that passes through switch DPID_SWITCH)

        
