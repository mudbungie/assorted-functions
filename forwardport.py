#!/usr/bin/env python3

# Forwards TCP and UDP ports via iptables.

import subprocess
import re
from sys import exit, argv

# Invokes iptables to forward the port.
def forward_port(wanaddr, toaddr, fromport, toport, proto='tcp'):
	lan_dev, lan_addr = get_lan_if(toaddr)
	wan_dev, netmask = get_wan_if(wanaddr)

	if proto == 'tcp':
		# Allow SYN
		command = ['iptables', '-A', 'FORWARD', '-i', wan_dev, '-o', lan_dev, '-p', 
			proto, '--syn', '--dport', toport, '-m', 'conntrack', '--ctstate', 'NEW',
			'-j', 'ACCEPT']
		subprocess.Popen(command).wait()
		command = ['iptables', '-A', 'FORWARD', '-o', lan_dev, '-p', proto, '--syn',
			'--dport', toport, '-m', 'conntrack', '--ctstate', 'NEW', '-j', 'ACCEPT']
		subprocess.Popen(command).wait()
		# Translate internal address and port.
		command = ['iptables', '-t', 'nat', '-A', 'PREROUTING', '-p', proto, '-d',
			wanaddr, '--dport', fromport, '-j', 'DNAT', '--to-destination', 
			toaddr+':'+toport]
		subprocess.Popen(command).wait()

		# Modify the source address to be the internal interface.
		command = ['iptables', '-t', 'nat', '-A', 'POSTROUTING', '-o', lan_dev, '-p',
			proto, '--dport', toport, '-d', toaddr, '-j', 'SNAT', '--to-source', lan_addr]
		subprocess.Popen(command)

	else:
		# Allow UDP packets to hit the destination.
		command = ['iptables', '-t', 'nat', '-A', 'PREROUTING', '-i', wan_dev, -p, 
			'proto', '-d', wanaddr, '--dport', fromport, '-j', 'DNAT', 
			'--to-destination', toaddr]
		subprocess.Popen(command)

		# Forward traffic.
		command = ['iptables', '-A', 'FORWARD', '-i', wan_dev, '-o', lan_addr, 
			'-p', proto, '-d', wanaddr, '--dport', fromport, '-j' 'DNAT', 
			'--to-destination', toaddr]
		subprocess.Popen(command)

		# Reply traffic.
		command = ['iptables', '-m', 'state', '-A', 'FORWARD', '-o', wan_dev, '-i',
			lan_addr, '-p', proto, '-s', toaddr, '--sport', toport, '--state', 
			'ESTABLISHED,RELATED', '-j', 'ACCEPT']
		subprocess.Popen(command)

# Checks the routing table to find out what interface the packet should leave 
# on.
def get_lan_if(toaddr):
	command = ['ip', 'route', 'get', toaddr]
	route = subprocess.Popen(command, stdout=subprocess.PIPE)
	route.wait() # Make sure that it completes the command
	route = route.stdout.read().decode().split()
	print(route)
	lan_dev = route[2]
	lan_addr = route[4]
	return lan_dev, lan_addr

def get_wan_if(wanaddr):
	command = ['ip', 'addr']
	interfaces = subprocess.Popen(command, stdout=subprocess.PIPE)
	interfaces.wait() # Make sure that it completes the command
	interfaces = interfaces.stdout.read().decode().split()
	ifre = re.compile(r'\d:')

	for idx, datum in enumerate(interfaces):
		# Keep track of the most recently specified interface.
		if ifre.match(datum):
			wandev = interfaces[idx + 1]
		# Look for our address.
		if datum.split('/')[0] == wanaddr:
			netmask = datum.split('/')[1]
			return wandev, netmask
	exit('WAN IP address not found: {}'.format(wanaddr))

def parse_args(argv):
	if not 5 <= len(argv) <= 6:
		exit('Usage: forward_port wanaddress toaddress fromport toport [-u]')
	if '-u' in argv:
		proto = 'udp'
	else:	
		proto = 'tcp'
	# Clear options
	argv = [arg for arg in argv[1:] if not arg.startswith('-')]

	print(argv)
	print(proto)
	forward_port(*argv, proto=proto)
	
if __name__ == '__main__':
	parse_args(argv)
