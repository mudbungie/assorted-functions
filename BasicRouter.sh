#!/bin/bash

#iptables settings to make this a basic router
# should be invoked by /etc/network/interfaces
# as a pre-up option on the internal interface
# I haven't bothered to generalize this, but
# it's not complicated

# this should be on, but it's good to make sure
echo 1 > /proc/sys/net/ipv4/ip_forward

# clear out old rules, so that I can run this sequentially
/sbin/iptables -F

# masquerage eth1 (internal, isolated) to VPN interface
/sbin/iptables -t nat -A POSTROUTING -o tun0 -j MASQUERADE
/sbin/iptables -A FORWARD -i tun0 -o eth1 -m state --state RELATED,ESTABLISHED -j ACCEPT
/sbin/iptables -A FORWARD -i eth1 -o tun0 -j ACCEPT

