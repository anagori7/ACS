#!/bin/bash

# Start the Mininet topology
sudo python3 hub_topo.py

# Start Mininet CLI and run the commands inside the Mininet environment
sudo mn --custom hub_topo.py --topo mytopo --mac --switch ovsk --controller none <<EOF
h3 python3 /home/ansafnagori/src-cloud/scripts/mitm_attack.py &
h2 python3 /home/ansafnagori/src-cloud/scripts/mitm_udp_server.py &
h1 python3 /home/ansafnagori/src-cloud/scripts/mitm_udp_client.py
EOF
