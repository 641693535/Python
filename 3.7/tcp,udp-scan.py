import optparse
import socket
import time
from scapy.all import *
import os

#FLAG1=F1.F2.F3

def tcpconnscan(host,port):
	try:
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.connect((host,port))
		print('[+]%d /udp open'%port)
		s.close()
	except:pass
#FLAG2=F4.F5.

def udpconnscan(host,port):
	try:
		rep = sr1(IP(dst=host)/UDP(dport=port),timeout=1,verbose=0)
		if rep.haslayer(ICMP):
			pass
	except:print('[+]%d /udp open'%port)
#FLAG3=F6.F7.F8

def portscan(host):
	for port in range(1,500):
		udpconnscan(host,port)
def main():
	for i in range(1,254):
		ip = '192.168.83.'+str(i)
		ping = os.popen('arping -c 2 '+ip)
		if 'ms' in ping.read():
			print(ip)
			portscan(ip)
#FLAG7=F9.F10
if __name__ == '__main__':
	main()
		
