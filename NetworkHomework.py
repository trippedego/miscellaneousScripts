###############NETWORK HOMEWORK######################
##### CSEC-380/480 Security Automation - Ryan Haley####
'''
You have just joined an elite 3-letter government agency’s red team.
On your first assignment, you gain access to a host on the target network,
but are unable to upload or run any unauthorized tools due to strict
application control on the host. You do notice, however, that python is
a whitelisted application on the host. Knowing this, you decide to use
it to do your reconnaissance (scanning) of the network.
 
Create a program that simulates nmap (network scanning tool).
Your program must accept options for IP(s), TCP or UDP,
and port numbers or ranges. The program will then tell the
user which ports are open on the target IP(s). 

You are to scan your Windows 10 host (10.12.0.15) from your Kali system (10.12.0.10) ONLY!!!

Required Conditions (0.75 pts/each - 5 pts total):
	Does it run without errors? 
	Can it successfully scan 1 IP? 
	Can it successfully scan multiple IPs? 
	Can it attempt to identify open/closed UDP ports? 
	Can it identify open/closed TCP ports? 
	Can it successfully scan multiple ports? 
	Does it properly inform the user of findings? 

Bonus Conditions (+3.5 possible):
	Fingerprint any port/service running a webserver (What service and version was discovered). (0.5 pt)
                Inform the user of the type and version server found. (0.5pts)
                If Service is a webserver:
                        Inform the user of the status code returned (for a root request – aka "GET / HTTP/1.1"). (0.5pts)
                        Inform the user of the title of the page found. (0.5pts)
	Option to take a list (txt file) of IPs to scan. (0.5 pts)
	Option to take a timeout value between each port scan. (0.5 pts)
	Option to save results to a  txt file (0.5 pts)
'''

import socket

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
					sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
					result = sock.connect((target,port))
					print("Port {} is OPEN".format(port))
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