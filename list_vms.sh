#!/bin/bash

# Configuration
SERVER_IP="100.81.45.53"
USER="root"

echo "Listing running VMs on Proxmox ($SERVER_IP)..."

# Use SSH to run the 'qm list' command on the server
# 'qm list' shows QEMU/KVM Virtual Machines
# Filtering for VMs with status 'running'
ssh "$USER@$SERVER_IP" "qm list" | awk '$3 == "running" {print $1, $2}' | while read -r vmid name; do
    echo "VM ID: $vmid | Name: $name"
done

# If you also want to list running LXC containers, uncomment the following:
# echo -e "\nListing running containers..."
# ssh "$USER@$SERVER_IP" "pct list" | awk '$2 == "running" {print $1, $3}' | while read -r vmid name; do
#     echo "CT ID: $vmid | Name: $name"
# done
