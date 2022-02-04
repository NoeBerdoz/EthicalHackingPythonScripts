#!/usr/bin/env python
# Regex created with https://pythex.org/

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()

    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")

    (options, arguments) = parser.parse_args()

    if not options.interface and not options.new_mac:
        parser.error("Please specify an interface and a mac address, use --help for more info.")
    elif not options.interface:
        parser.error("Please specify an interface, use --help for more info.")
    elif not options.new_mac:
        parser.error("Please specify a mac address, use --help for more info.")
    return options


def change_mac(interface, new_mac):
    subprocess.call(["sudo", "ifconfig", interface, "down"])
    subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["sudo", "ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", options.interface])

    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))

    if mac_address_search_result:
        return mac_address_search_result.group(0)

    if not mac_address_search_result:
        print("Could not find MAC address")


options = get_arguments()
current_mac = get_current_mac(options.interface)

if current_mac == options.new_mac:
    print("Changed MAC address for " + options.interface + " " + options.new_mac)


if current_mac != options.new_mac:
    print("Didn't change MAC address")

