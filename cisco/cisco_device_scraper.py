# cisco_cli_scraper.py
import netmiko as n

class CiscoDeviceInfoScraper(object):
    """
    The CiscoDeviceInfoScraper is designed to collect the following
    information.
    ~ Hostname
    ~ Serial number
    ~ Model number
    ~ IOS Version

    The information is extracted from the 'show verion' command.
    Therefore devices such as 6500 and 4500 CAT are not supported,
    as they hold this information on the 'show inventory' command

    Output will print to screen for copy/pasting and save device
    information in a python list named 'results'
    
    Printed output
    If supported hardware
    DEVICENAME, IP_ADDRESS, SERIAL_NUM, MODEL_NUM, IOS_VERSION
    If not supported hardware
    DEVICENAME, IP_ADDRESS, ERROR, ERROR, ERROR
    
    Use at your own risk!
    """
    def _hostname(self, d):
        """Collect Hostname"""
        int_hn = d.send_command('sh run | i hostname').split()
        return int_hn[-1]

    def _serial_number(self, d):
        """Collect Serial Number"""
        int_sn = d.send_command(
            'sh ver | i System Serial Number'
        ).split()
        if len(int_sn) == 0:
            int_sn = d.send_command(
            'sh ver | i System serial number'
            ).split()
        # Single Device
        if len(int_sn) == 5: return [int_sn[-1]]
        # Stacked Device
        elif len(int_sn) > 5: return int_sn[4::5]
        # Not supported
        else: return ['ERROR']

    def _model_number(self, d):
        """Collect Model Number"""
        int_mod = d.send_command(
            'sh ver | i Model Number'
        ).split()
        if len(int_mod) == 0:
            int_mod = d.send_command(
            'sh ver | i Model number'
            ).split()
        # Single Device
        if len(int_mod) == 4: return [int_mod[-1]]
        # Stacked Device
        elif len(int_mod) > 4: return int_mod[3::4]
        # Not supported
        else: return ['ERROR']

    def _ios_version(self, d):
        """Collect IOS Version"""
        ios = d.send_command('sh ver | i \*').split()
        if len(ios) > 0: return ios[4]
        else: return 'ERROR'

    def start_scraping(self):
        """Run this shit"""
        # Setup for Cisco IOS
        platform = 'cisco_ios'

        # Change these
        user = 'username'
        passwd = 'password'
        ip_file = 'ip_list.txt'

        # Read IP address text file and make a python list
        with open(ip_file,'r') as f:
            ip_add_file_dupes = f.readlines()

        # Remove duplicates
        ip_add_list = list(set(ip_add_file_dupes))
        results = []
        print("Start CLI scraping")
        print("Total IP Addresses : %s" % len(ip_add_list))
        for ip in ip_add_list:
            ip = ip.strip()
            try:
                # Create SSH session
                device = n.ConnectHandler(
                      device_type=platform,
                      ip=ip,
                      username=user,
                      password=passwd
                )
                # Collect information
                device.send_command('enable')
                hn = self._hostname(device)
                _sn = self._serial_number(device)
                _mod = self._model_number(device)
                ios = self._ios_version(device)
                # Iterate over the information
                for sn, mod in zip(_sn, _mod):
                    # Put result in the list
                    results.append((hn,ip,sn,mod,ios))
                    # Print result to the screen
                    print(
                        "%s, %s, %s, %s, %s" % (
                            hn, ip, sn, mod, ios
                        )
                    )
                device.cleanup()
            except n.ssh_exception.NetMikoTimeoutException:
                print("Unable to SSH to IP Address : %s" % ip)
        print("Finished, time for a beer!")
        return(results)

# Execute class
results = CiscoDeviceInfoScraper().start_scraping()
