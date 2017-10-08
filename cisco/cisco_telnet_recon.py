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
    
    # Telnet to the device and login
    tn = telnetlib.Telnet(HOST_IP)
    tn.read_until(b"Password: ")
    tn.write(telnet_password + b"\r\n")
    sleep(0.5)
    
    # Get host name from prompt and make a directory
    host_name = re.sub(
        '\r\n',"",tn.read_very_eager().decode('ascii'))[:-1]
    if not os.path.exists(host_name):
        os.makedirs(host_name)
    
    # Log into enable mode
    tn.write(b"enable\r\n")
    tn.write(enable_password + b"\r\n")
    
    # Set terminal output to 0 
    tn.write(b"terminal length 0\r\n")
    tn.read_very_eager().decode('ascii')
    sleep(1)
    
    # execute show commands and save in the directory created
    for show_command in show_commands_list:
        tn.write(show_command+b"\r\n")
        sleep(1)
        out = tn.read_very_eager().decode('ascii')
        file_name = re.sub(' ', '_', show_command.decode('ascii'))
        with open(host_name+'/'+file_name+'.txt','w') as f:
            f.write(out)
    
    # Close telnet connection
    tn.close()
