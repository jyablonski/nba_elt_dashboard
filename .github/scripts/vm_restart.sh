#!/bin/bash

# Config
VM_IP="${GCP_VM_IP}"
VM_USER="jyablonski9"
REPO_DIR="nba_elt_dashboard"

echo "SSHing into $VM_USER@$VM_IP..."

ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null $VM_USER@$VM_IP <<EOF
  set -e
  echo "Navigating to project directory..."
  cd ~/$REPO_DIR

  echo "Restarting Docker Compose services..."
  sudo ~/.docker/cli-plugins/docker-compose down
  sudo ~/.docker/cli-plugins/docker-compose up -d

  echo "Refresh complete."
EOF
