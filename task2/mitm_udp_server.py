# udp_server.py
import socket

# Server settings
UDP_IP = "10.0.0.2"  # IP of Host 2
UDP_PORT = 12345      # Port to listen on

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Server listening on {UDP_IP}:{UDP_PORT}")

while True:
    # Receive data from the client
    data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes
    print(f"Received message: {data.decode()} from {addr}")

    # Send a response back to the client
    response = f"Message received: {data.decode()}"
    sock.sendto(response.encode(), addr)
