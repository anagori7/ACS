from scapy.all import *

# Function to extract the latest sequence and acknowledgment numbers
def packet_callback(packet):
    if packet.haslayer(TCP):
        tcp_layer = packet.getlayer(TCP)
        if packet.haslayer(IP):
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            sport = tcp_layer.sport
            dport = tcp_layer.dport
            seq_num = tcp_layer.seq
            ack_num = tcp_layer.ack
            
            # We are interested in the communication between Host 1 and Host 2
            if (src_ip == "10.0.0.2" and dst_ip == "10.0.0.1") or (src_ip == "10.0.0.1" and dst_ip == "10.0.0.2"):
                print(f"Captured packet: {src_ip}:{sport} -> {dst_ip}:{dport} Seq={seq_num} Ack={ack_num}")
                return seq_num, ack_num

# Sniff the latest SEQ and ACK
def sniff_seq_ack():
    sniff(prn=packet_callback, filter="tcp", iface="h3-eth0", count=1)

# Start sniffing continuously for the latest SEQ and ACK
sniff_seq_ack()

