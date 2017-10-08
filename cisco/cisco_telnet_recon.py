import telnetlib
from time import sleep
import re
import os


HOST_IPs = [
    "172.16.1.253", "172.16.1.254"
]
telnet_password = b"pass_here"
enable_password = b"pass_here"
show_commands_list = [
    b"show run",
    b"show ip arp",
    b"show vlan",
    b"show cdp neighbors",
    b"show ip interface brief"
    b"show interface status",
    b"show interface description",
    b"show etherchannel summary"
]
for HOST_IP in HOST_IPs:
    tn = telnetlib.Telnet(HOST_IP)
    any_host_name = re.findall('[A-z,0-9,\-\_]', '_')
    tn.read_until(b"Password: ")
    tn.write(telnet_password + b"\r\n")
    sleep(0.5)
    host_name = re.sub(
        '\r\n',"",tn.read_very_eager().decode('ascii'))[:-1]
    if not os.path.exists(host_name):
        os.makedirs(host_name)
    tn.write(b"enable\r\n")
    tn.write(enable_password + b"\r\n")
    tn.write(b"terminal length 0\r\n")
    tn.read_very_eager().decode('ascii')
    sleep(1)
    for show_command in show_commands_list:
        tn.write(show_command+b"\r\n")
        sleep(1)
        out = tn.read_very_eager().decode('ascii')
        file_name = re.sub(' ', '_', show_command.decode('ascii'))
        with open(host_name+'/'+file_name+'.txt','w') as f:
            f.write(out)

    tn.close()
