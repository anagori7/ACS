from scapy.all import sniff, IP, ICMP, sr1, send
import threading
import time

# Function to sniff ICMP traffic
def sniff_icmp_traffic():
    def process_packet(packet):
        print(f"Captured packet: {packet.summary()}")
        if ICMP in packet and packet[ICMP].type == 8:  # Check if it's an ICMP Echo Request (type 8)
            ip_layer = packet[IP]
            icmp_layer = packet[ICMP]
            print(f"Captured ICMP Echo Request from {ip_layer.src} to {ip_layer.dst}")

            # Craft a spoofed ICMP Echo Reply
            spoofed_reply = IP(src="10.0.0.5", dst=ip_layer.src) / ICMP(type=0, id=icmp_layer.id, seq=icmp_layer.seq)
            print(f"Sending spoofed reply to {ip_layer.src} from 10.0.0.5")

            # Send the spoofed reply
            send(spoofed_reply)

    print("Starting ICMP sniffing...")
    sniff(iface='h1-eth0', filter="icmp", prn=process_packet)  # Adjust the interface if needed

# Function to send ICMP requests (ping) to target hosts
def send_icmp_requests():
    target_ips = ["10.0.0.2", "10.0.0.3", "10.0.0.4", "10.0.0.5"]  # List of target IPs to ping
    for target_ip in target_ips:
        print(f"Pinging {target_ip}")
        pkt = IP(dst=target_ip)/ICMP()
        reply = sr1(pkt, timeout=2, verbose=False)  # Send the packet and wait for a reply
        if reply:
            print(f"Reply from {target_ip}: {reply.src}")
        else:
            print(f"No reply from {target_ip}")

# Main function to run sniffing and sending traffic concurrently
if __name__ == "__main__":
    # Start sniffing in a separate thread so it runs in the background
    sniff_thread = threading.Thread(target=sniff_icmp_traffic)
    sniff_thread.daemon = True  # Daemon thread will exit when the main program exits
    sniff_thread.start()

    # Give the sniffing a moment to initialize
    time.sleep(1)

    # Send ICMP requests (ping) from h1 to h2, h3, h4, and 10.0.0.5
    send_icmp_requests()

    # Allow sniffing to continue for 10 more seconds after pings
    time.sleep(10)

    print("Stopping ICMP sniffing.")
