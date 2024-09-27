# udp_client.py (Client on Host 1)
import socket

def udp_client():
    server_ip = "10.0.0.2"  # IP of Host 2 (Server)
    server_port = 12345      # Port on which server is listening
    message = "Hello from Host 1 (Client)"  # Message to send

    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Send the message to the server
        print(f"Sending message to {server_ip}:{server_port}")
        client_socket.sendto(message.encode(), (server_ip, server_port))

        # Receive the response from the server
        response, server_address = client_socket.recvfrom(1024)
        print(f"Received response from {server_address}: {response.decode()}")

    finally:
        # Close the socket
        client_socket.close()

if __name__ == "__main__":
    udp_client()
