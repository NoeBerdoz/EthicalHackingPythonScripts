# EthicalHackingPythonScripts
Some of my Python scripts related to Ethical hacking.

These files were made for an **educational purpose only**.

## Reverse Backdoor
*/reverse_backdoor*
This little malware will create a backdoor to the machine where it's executed.  
It's adapted for Windows and it's currently detected by Windows Defender.
The backdoor allows me to get acces to the victim machine via a command prompt.

## Key Logger
*/key_logger*  
This Script will record keystrokes made by a user.
It will then send the recorded data to an email.

## ARP Spoof
*arp_spoof.py*  
The ARP protocol was not designed for security,
so it does not verify that a response to an ARP request really comes from an authorized party.  
This script allows a MITM attack

## DNS Spoofing
*dns_spoof.py*  
This script will redirect a victim to a target website
It works by doing an MITM attack first with *arp_spoof.py*

## Crawler
*domain_crawler.py*  
will find any domain folder related to a wordlist.

*link_crawler.py*   
will find all links present in a website given a start point page.  

## Replace Download & Code Injector
These scripts work with the *arp_spoof.py* script

*replace_downloads.py*  
Will look for a download request and change the packet's response to modify the target file for a user to download.

*code_injector.py*  
Will change a packet's response to modify the HTML page and inject javascript code to a web page that a user is requesting.

## Packet sniffer
*packet_sniffer.py*  
This script will monitor the network and look for non encrypted data that concerns credentials

## Network scanner
*network_scanner.py*  
Takes a given network and returns all local IPs

## Mac Changer
*mac_changer.py*  
Let a debian machine change its mac address
