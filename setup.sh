#!/bin/bash

# Stop services
sudo systemctl stop melodymint_backend.service

# Copy service files
sudo cp melodymint_backend.service /etc/systemd/system/

# Reload systemctl daemon
sudo systemctl daemon-reload

# Enable services
sudo systemctl enable melodymint_backend.service

# Start services
sudo systemctl start melodymint_backend.service

echo "Setup completed."
