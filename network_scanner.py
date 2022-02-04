#!usr/bin/env python
# If you have issues with the scapy module
# Do the following commands :
# 1) sudo mkdir /usr/lib/python2.7/dist-packages/scapy
# 2) cd /usr/lib/python3/dist-packages/
# 3) sudo cp -avr scapy/* /usr/lib/python2.7/dist-packages/scapy

import scapy.all as scapy
import argparse


def get_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--target", dest="target", help="Target to scan")
    parser.add_argument("-m", "--mask", dest="mask", help="CIDR ip routing")
    options = parser.parse_args()

    if not options.target:
        parser.error("Please specify an ip target")

    return options


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)

    return clients_list


def print_result(results_list):
    print("------------------------------------------------------------")
    print("IP\t\t\tMAC Adress\n------------------------------------------------------------")
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])


options = get_arguments()
scan_result = scan(options.target + "/" + options.mask) if options.mask else scan(options.target)
print_result(scan_result)
