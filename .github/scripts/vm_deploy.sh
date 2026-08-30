#!/bin/bash

# Config
VM_IP="${GCP_VM_IP}"
VM_USER="jyablonski9"
REPO_DIR="nba_elt_dashboard"
GIT_COMMIT="${GIT_COMMIT:-unknown}"
DBT_SEMANTIC_MANIFEST_URI="${DBT_SEMANTIC_MANIFEST_URI:-}"

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

  echo "Pulling latest code from main..."
  git pull origin main

  echo "Rebuilding Docker image with commit SHA: $GIT_COMMIT..."
  sudo docker build \
    -f docker/Dockerfile \
    --build-arg GIT_COMMIT=$GIT_COMMIT \
    -t nba_elt_dashboard_local .

  echo "Staging the dbt semantic manifest for the MCP image..."
  DBT_SEMANTIC_MANIFEST_URI="$DBT_SEMANTIC_MANIFEST_URI" bash .github/scripts/fetch_semantic_manifest.sh

  echo "Rebuilding MCP image with commit SHA: $GIT_COMMIT..."
  sudo docker build \
    -f docker/Dockerfile.mcp \
    --build-arg GIT_COMMIT=$GIT_COMMIT \
    -t nba_elt_mcp_local .

  echo "Starting updated service with Docker Compose..."
  sudo ~/.docker/cli-plugins/docker-compose up -d

  echo "Checking disk usage..."
  df -h / | grep -v Filesystem

  echo "Deployment complete."
EOF
