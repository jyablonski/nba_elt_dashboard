#!/bin/bash

# Config
VM_IP="${GCP_VM_IP}"
VM_USER="jyablonski9"
REPO_DIR="nba_elt_dashboard"
GIT_COMMIT="${GIT_COMMIT:-unknown}"

echo "SSHing into $VM_USER@$VM_IP..."
echo "Deploying commit: $GIT_COMMIT"

ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null $VM_USER@$VM_IP <<EOF
  set -e
  echo "Navigating to project directory..."
  cd ~/$REPO_DIR

  echo "Stopping current Docker Compose services..."
  sudo ~/.docker/cli-plugins/docker-compose down

  echo "Cleaning up Docker resources..."
  sudo docker system prune -a -f
  sudo docker volume prune -f

  echo "Pulling latest code from master..."
  git pull origin master

  echo "Rebuilding Docker image with commit SHA: $GIT_COMMIT..."
  sudo docker build \
    -f docker/Dockerfile \
    --build-arg GIT_COMMIT=$GIT_COMMIT \
    -t nba_elt_dashboard_local .

  echo "Starting updated service with Docker Compose..."
  sudo ~/.docker/cli-plugins/docker-compose up -d

  echo "Checking disk usage..."
  df -h / | grep -v Filesystem

  echo "Deployment complete."
EOF
