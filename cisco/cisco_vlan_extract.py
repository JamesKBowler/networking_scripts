from ciscoconfparse import CiscoConfParse as ccp


def extract_vlan(vlans):
    """
    Will convert ACTIVE vlans in the 'show vlan' command .....
    
    switch#show vlan
    VLAN Name                             Status    Ports
    ---- -------------------------------- --------- -------------------------------
    1    default                          active    Fa0/48
    2    AAAAA                            active
    3    BBBBB                            active
    4    CCCCC                            active    Fa0/1, Fa0/2, Fa0/3, Fa0/4, Fa0/5, Fa0/6, Fa0/7
    5    DDDDD                            active
    6    EEEEE                            active
    7    FFFFF                            active    Fa0/25, Fa0/26, Fa0/27, Fa0/28, Fa0/29, Fa0/30
    1002 fddi-default                     act/unsup
    1003 token-ring-default               act/unsup
    1004 fddinet-default                  act/unsup
    1005 trnet-default                    act/unsup
    
    To configuration like this .....
    vlan 2
     name AAAAA
    vlan 3
     name BBBBB
    vlan 4
     name CCCCC
    vlan 5
     name DDDDD
    vlan 6
     name EEEEE
    vlan 7
     name FFFFF
    """
    active_vlans = vlans.find_objects("active")
    for i in active_vlans:
        if not " ".join(i.text.split()[0:1]) == "1":
            print("vlan", " ".join(i.text.split()[0:1]))
            print(" name"," ".join(i.text.split()[1:2]))

extract_vlan(ccp("show_vlan.txt"))
