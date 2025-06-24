#!/bin/bash
set -e
# Update and install packages
sudo apt-get update -y
sudo apt-get install -y git apt-transport-https ca-certificates curl software-properties-common


# Install Git and Docker (from Ubuntu repo)
sudo apt-get install -y git docker.io
 
# Add user to the docker group
sudo usermod -aG docker $USER || true

# Enable and start Docker
sudo systemctl enable docker
sudo systemctl start docker
