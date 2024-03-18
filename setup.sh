#!/bin/bash

# Stop services
sudo -n systemctl stop melodymint_backend.service || true

# Copy service files
sudo -n cp melodymint_backend.service /etc/systemd/system/ || true

# Reload systemctl daemon
sudo -n systemctl daemon-reload || true

# Enable services
sudo -n systemctl enable melodymint_backend.service || true

# Start services
sudo -n systemctl start melodymint_backend.service || true

echo "Setup completed."
