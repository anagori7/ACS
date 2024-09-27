from scapy.all import *

# Function to handle sniffed ICMP packets
def icmp_monitor(packet):
    if packet.haslayer(ICMP):
        icmp_layer = packet.getlayer(ICMP)
        if icmp_layer.type == 8:  # ICMP Echo Request (ping request)
            print(f"[+] Ping request from {packet[IP].src} to {packet[IP].dst}")
        elif icmp_layer.type == 0:  # ICMP Echo Reply (ping reply)
            print(f"[+] Ping reply from {packet[IP].src} to {packet[IP].dst}")

# Sniff ICMP packets (both incoming and outgoing)
print("Sniffing ICMP packets...")
sniff(filter="icmp", prn=icmp_monitor, store=False)
