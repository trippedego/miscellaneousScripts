import socket
from scapy.all import *

def scanMe():
	while True:
		target = str(input("Enter the target IP (or enter nothing to exit program)..."))
		if not target:
			exit()
		try:
			socket.inet_aton(target)
			try:
				port = int(input("Enter port you wish to scan..."))
				proto = str(input("TCP or UDP Scan???"))
				if proto == "TCP" or proto == "tcp":
					sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					result = sock.connect((target,port))
					print("Port {} is OPEN".format(port))
				elif proto == "UDP" or proto == "udp":
					timeout = 10
					pkt = sr1(IP(dst=target)/UDP(sport=43644, dport=port)/Raw(load='test'),timeout=2, verbose=0)
					
					if pkt == None:
						print("Port {} is Open / Filtered".format(port))
					else:
						if pkt.haslayer(ICMP):
							print("Port {} is Closed".format(port))
						elif pkt.haslayer(UDP):
							print("Port {} is Open".format(port))
						else:
							print("Unknown response...")
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
