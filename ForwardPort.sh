#!/bin/bash

# basic router port forwarding
# implementation is basic, and assumes a functional masquerade
# for an implementation, see BasicRouter.sh

# function for forwarding a given port to a downstream host
ForwardPort(){

# assign variables to intelligible names
WanInterface=$1
ExternalPort=$2
InternalPort=$3
ServerAddress=$4

# the iptables rules
iptables -t nat -A PREROUTING -p tcp -i $WanInterface --dport $ExternalPort -j DNAT --to-destination $ServerAddress:$InternalPort
iptables -A FORWARD -p tcp -d $ServerAddress --dport $InternalPort -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT
}

