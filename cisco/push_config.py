from getpass import getpass
import sys
import netmiko as ne
import time


def log_to_file(
    log_msg,
    log_file_loc='report.txt'
    ):
    try:
        log_file = open(log_file_loc, 'a')
    except FileNotFoundError:
        sys.exit("File not found: {} ".format(log_file_loc))
    log_file.write(log_msg)
    log_file.close()

def string_colour(
    text,
    colour=7
    ):
    """
    Create string text in a particular colour to the terminal.
    BLACK   : 0
    RED     : 1
    GREEN   : 2
    YELLOW  : 3
    BLUE    : 4
    MAGENTA : 5
    CYAN    : 6
    WHITE   : 7
    """
    return "\x1b[1;%dm" % (30 + colour) + str(text) + "\x1b[0m"

def open_device_list_file(
    file_path='device_list.txt'
    ):
    try:
        handle = open(file_path, 'r')
    except FileNotFoundError:
        sys.exit("File not found: {} ".format(file_path))
    reader = handle.readlines()
    handle.close()
    return [i for i in reader if i is not '']

def ssh_to_device(
    device_ip,
    username,
    password,
    device_type='cisco-ios',
    timeout=10
    ):
    try:
        try:
            session = ne.ConnectHandler(
                  device_type=device_type,
                  ip=device_ip,
                  username=username,
                  password=password,
                  timeout=timeout
            )
            return session
        except ne.NetMikoAuthenticationException as e:
            print(
                "Authentication failed for IP: {}".format(
                    device_ip
                )
            )
    except ne.ssh_exception.NetMikoTimeoutException:
        print(
            "SSH TimeOut to IP: {}".format(
                device_ip
            )
        )
    return None

def enter_password():
    user_password = getpass(
        prompt="Enter User Password:"
    )
    enable_password = getpass(
        prompt="Enter Enable Password or hit Return if the same:"
    )
    if not enable_password:
        enable_password = user_password
    return user_password, enable_password


if len(sys.argv) != 4:
    raise AttributeError(
        "Usage: push_config.py <hostfile> <username> <TFTP-IP> <source-file>"
    )

# User input variables
host_list_file = sys.argv[1]
username = sys.argv[2]
tftp_server = sys.argv[3]
config_file = sys.argv[4]
user_password, enable_password = enter_password()

# File input locations
device_file_loc = 'device_list.txt'
log_file_loc = 'log_file.txt'

# Get a list of the devices
devices_list = open_device_list_file(device_file_loc)

# Iterate over each device in the list
for device_ip in devices_list:

    # Create session
    session = ssh_to_device(
        device_ip,
        username,
        user_password
    )

    # Save the current configuration
    session.save_config()

    # Backup config to flash
    time_now = int(time.time())
    backup_result = session.send_command_timing(
        "copy running-config flash:running-config-backup{}".format(time_now)
    )
    print(string_colour(backup_result, colour=3))

    # Copy the configuration file to the device
    tftp_result = session.send_command_timing(
        "copy tftp://{}/{} running-config".format(tftp_server, config_file)
    )
    print(string_colour(tftp_result, colour=6))

    # Merge the configuration file to the device
    merge_result = session.send_command_timing(
        "copy {} running-config".format(config_file)
    )
    print(string_colour(merge_result, colour=1))

    # Log the session to a text file
    log_msg = "{} : Complete".format(device_ip)
    log_to_file(log_msg, log_file_loc)

    # Disconnect SSH session
    session.disconnect()
