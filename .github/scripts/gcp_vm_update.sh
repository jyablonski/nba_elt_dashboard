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

  echo "Stopping current Docker Compose services..."
  sudo docker compose down

  echo "Pulling latest code from master..."
  git pull origin master

  echo "Rebuilding Docker image..."
  sudo docker build -f docker/Dockerfile -t nba_elt_dashboard_local .

  echo "Starting updated service with Docker Compose..."
  sudo ~/.docker/cli-plugins/docker-compose up -d

  echo "Deployment complete."
EOF
