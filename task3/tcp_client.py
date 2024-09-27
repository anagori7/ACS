import socket

# Client setup
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('10.0.0.1', 5555))

client.sendall(b"Hello, Server!")
data = client.recv(1024)
print(f"Server reply: {data.decode()}")

client.close()
