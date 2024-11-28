#!/bin/bash

# Update system packages
echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install MongoDB
echo "Installing MongoDB..."
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt update
sudo apt install -y mongodb-org

# Start and enable MongoDB service
echo "Starting MongoDB service..."
sudo systemctl start mongod
sudo systemctl enable mongod

# Check MongoDB status
echo "Checking MongoDB service status..."
sudo systemctl status mongod --no-pager

# Install Python and pip (if not already installed)
echo "Installing Python and pip..."
sudo apt install -y python3 python3-pip

# Install pymongo
echo "Installing pymongo..."
pip3 install pymongo

# Verify installations
echo "Verifying installations..."
echo "MongoDB version:"
mongod --version

echo "Python version:"
python3 --version

echo "pymongo version:"
pip3 show pymongo | grep Version

echo "Setup completed! MongoDB is installed and running. You can now use pymongo to connect to your database."
