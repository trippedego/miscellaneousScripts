import socket
from scapy.all import *

def scanMe():
	while True:
		target = str(input("Enter the target IP (or enter nothing to exit program)... "))
		if not target:
			exit()
		try:
			socket.inet_aton(target)
			try:
				port = int(input("Enter port you wish to scan... "))
				proto = str(input("TCP or UDP Scan??? "))
				if proto == "TCP" or proto == "tcp":
					sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					result = sock.connect((target,port))
					print("Port {} is OPEN".format(port))
				elif proto == "UDP" or proto == "udp":
					interface = str(input("Enter interface to send packet out of... "))
					ans, unans = sr(IP(dst=target)/UDP(sport=65500, dport=port)/Raw(load='test'), iface=interface, timeout=5, verbose=0)
					
					if ans.summary().find("ICMP") != -1:
						print("Port {} is CLOSED".format(port))
						continue
					else:
						print("Port {} is OPEN / FILTERED".format(port))
						continue
						
				else:
					print("You did not specify either TCP or UDP...")
				continue
			except:
				print("Port {} is CLOSED".format(port))
				continue
		except:
			print("Not a valid IP address!!!")
			exit()
		
		return

scanMe()
