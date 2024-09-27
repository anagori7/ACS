#!/bin/bash

# Step 1: Start Mininet Network Topology
echo "Starting Mininet topology..."
sudo python3 /home/ansafnagori/src-cloud/scripts/task3/hub_topo.py &

# Give some time for Mininet to start
sleep 20

# Step 2: Start the sniffer on Host 3
echo "Starting sniffer on Host 3..."
sudo mnexec -a $(ps -aux | grep 'h3' | awk '{print $2}' | head -n 1) python3 /home/ansafnagori/src-cloud/scripts/task3/sniff.py &

# Step 3: Start the TCP server on Host 1
echo "Starting TCP server on Host 1..."
sudo mnexec -a $(ps -aux | grep 'h1' | awk '{print $2}' | head -n 1) python3 /home/ansafnagori/src-cloud/scripts/task3/tcp_server.py &

# Step 4: Start the TCP client on Host 2
echo "Starting TCP client on Host 2..."
sudo mnexec -a $(ps -aux | grep 'h2' | awk '{print $2}' | head -n 1) python3 /home/ansafnagori/src-cloud/scripts/task3/tcp_client.py &

# Step 5: Start tcpdump on Host 1 to capture traffic on port 5555
echo "Starting tcpdump on Host 1..."
sudo mnexec -a $(ps -aux | grep 'h1' | awk '{print $2}' | head -n 1) tcpdump -i any -n tcp port 5555 > tcpdump_output.txt &

# Give time for network interactions to settle
sleep 5

# Step 6: Run the spoofing script on Host 3
echo "Running spoofing script on Host 3..."
sudo mnexec -a $(ps -aux | grep 'h3' | awk '{print $2}' | head -n 1) python3 /home/ansafnagori/src-cloud/scripts/task3/spoof.py

echo "Attack completed."


