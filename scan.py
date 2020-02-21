import socket
import ipaddress
import sys
from concurrent.futures import ThreadPoolExecutor

# Number Of Threads
THREADS=20
SAVE_FILE="success.txt"

if len(sys.argv)!=2:
	print("ERROR: Invalid Syntax!!!")
	print("python scan.py HOST_IP")
	print("python scan.py HOST_IP_RANGE")
	print("python scan.py IP_FILE")
ipi=sys.argv[1]
ip_list=[]

def check_ip(ip):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(2)
	try:
		s.connect((ip,80))
		print("Conecting to {0} : Success !!!".format(ip))
		f=open(SAVE_FILE,"a")
		f.write(ip+"\n")
		f.close()
	except:
		print("Conecting to {0} : Failed ...".format(ip))
	finally:
		s.close()


if ipi.count(".")==3:
	if "/" in ipi:
		ip_list+=[str(ip) for ip in ipaddress.IPv4Network(ipi)]
	else:
		ip_list.append(ipi)
else:
	f=open(ipi)
	l=f.read().split('\n')
	f.close()
	for ipi in l:
		if len(ipi)<5:
			continue
		if "/" in ipi:
			ip_list+=[str(ip) for ip in ipaddress.IPv4Network(ipi)]
		else:
			ip_list.append(ipi)


with ThreadPoolExecutor(max_workers=THREADS) as pool:
	pool.map(check_ip,ip_list)
print("All IPs Processed !!!! ")