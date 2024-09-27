#!/bin/bash

# Start the UDP server on Host 2 (h2)
echo "Starting UDP server on h2..."
sudo mn &

h2 sudo python3 /home/ansafnagori/src-cloud/scripts/mitm_udp_server.py &

sleep 2

echo "Starting UDP client on h1..."
h1 sudo python3 /home/ansafnagori/src-cloud/scripts/mitm_udp_client.py
