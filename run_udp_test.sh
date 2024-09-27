#!/bin/bash

# Start Mininet with two hosts and a switch
echo "Starting Mininet..."
sudo mn --topo=single,2 --mac --switch=ovsk --controller=none <<EOF

# Start the UDP server on Host 2 (h2)
h2 python3 /home/ansafnagori/src-cloud/scripts/mitm_udp_server.py &

# Wait for the server to start
sleep 5

# Run the UDP client on Host 1 (h1)
h1 python3 /home/ansafnagori/src-cloud/scripts/mitm_udp_client.py

# Wait for a while to ensure communication happens
sleep 5

EOF

# Prevent Mininet from exiting immediately
echo "UDP communication completed. Mininet will now shut down."
