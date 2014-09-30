#!/usr/bin/python
#
#	pifinder Server - 2014 Steve Newbury
#	see ./LICENSE for more info

import socket
import threading
import SocketServer
from time import sleep
import sys
import subprocess
import datetime

# the response we will be looking for 
pf_packet = "PIFINDER"

# lazy function to get a current timestamp
def ts():
	return str(datetime.datetime.now())
	
# basic log function  
def log(string):
	d = datetime.date.today()
	logFile = "/var/log/pifinder.log"
	mode = 'a+'
	try:
		f = open(logFile, mode)
		f.write('\n %s : %s' % (ts(), string))
		f.close()
	except IOError as e:
		sys.exit(0)

class packetHandler(SocketServer.BaseRequestHandler):
	
	def handle(self):
		data = bytearray(self.request[0].strip())
		log("Beacon recieved from %s : %s" % (str(self.client_address), data))
		sock = self.request[1]
		if data == pf_packet: # if we get the magic sauce
			m = self.getAddresses()
			try:
				sock.sendto(m, self.client_address)
			except (socket.timeout, socket.error) as e:
				log("Error when responding - %s" % e)
					
	def getAddresses(self):
		ps = subprocess.Popen("/sbin/ifconfig eth0", shell=True, stdout=subprocess.PIPE)
		msg = []
		for line in iter(ps.stdout.readline, ''):
			if "HWaddr" in line:
				l = line.split(' ')
				for index, item in enumerate(l):
					if item == "HWaddr":
						macindex = index + 1
						break
				mac = l[macindex] 
				msg.append("\tMAC: %s" % mac)
			elif "inet addr" in line:
				l = line.strip().split(':')
				for index, item in enumerate(l):
					if item == "inet addr":
						ipindex = index + 1
						ipline = l[ipindex].split(' ') # splits line containing ip address by spaces
						ip = ipline[0]
						msg.append("\tIP Address: %s " % ip)
		
		return '\n'.join(msg)
	
		
class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
	pass
	
class Pi_Finder_Server():
	
	def __init__(self):
		self.HOST = "0.0.0.0"
		self.PORT = 8899
		self.server = ThreadedUDPServer((self.HOST, self.PORT), packetHandler)
		self.server_thread = threading.Thread(target=self.server.serve_forever)
		self.server_thread.daemon = True
				
	def start(self):
		try:
			self.server_thread.start()
			log("========== Server started ============")
		except socket.error as e:
			log("=== Server could not start : %s" % e)
			sys.exit(1)
		else:
			while 1:
				log("listening...") 
				sleep(7200)

if __name__ == "__main__":
	s = Pi_Finder_Server()
	s.start()

