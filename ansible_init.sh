#!/usr/bin/env bash

# Initialize host for ansible.

curl -s https://www.mudbungie.net/ansible.pub >> $HOME/.ssh/authorized_keys
if (($? == 0)); then
	echo "Key installed"
	exit 0
else
	echo "Key installation failed"
	exit 1
fi
