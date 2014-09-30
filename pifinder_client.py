#!/usr/bin/python
#
#	pifinder Client - 2014 Steve Newbury
#	see ./LICENSE for more info

import socket
import sys

# the response the server will be looking for 
pf_packet = "PIFINDER"

# lazy function to get a current timestamp
def ts():
	return str(datetime.datetime.now())
	
def client(ip, port, message):	
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	sock.settimeout(10)
	print "Searching the network..."
	try:
		sock.sendto(message, (ip, port))
		response = sock.recv(1024)
		print "Raspberry pi found:\n%s" % response
		sock.close()
	except socket.timeout as t:
		print "No response received"
		return -1
	except socket.error as e:
		print "Socket error: %s" % e
		return -1
	return 0
	

broadcast_address = "255.255.255.255"
while 1:
	if client(broadcast_address, 8899, pf_packet) < 0:
		if raw_input("Try again (Y/n)? : ") == "y":
			continue
	break

sys.exit(0)

