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
					result = sock.connect_ex((target,port))
					if result == 0:
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
