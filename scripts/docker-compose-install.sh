#!/bin/bash

# Set the version of Docker Compose you want to install
DOCKER_COMPOSE_VERSION="v2.12.2"  # You can change this to any version you prefer

# Step 1: Download Docker Compose
echo "Downloading Docker Compose version $DOCKER_COMPOSE_VERSION..."
sudo curl -L "https://github.com/docker/compose/releases/download/$DOCKER_COMPOSE_VERSION/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Step 2: Make the binary executable
echo "Applying executable permissions to Docker Compose binary..."
sudo chmod +x /usr/local/bin/docker-compose

# Step 3: Verify installation
echo "Verifying Docker Compose installation..."
docker-compose --version

# Step 4: Check if Docker Compose is installed successfully
if command -v docker-compose &>/dev/null; then
    echo "Docker Compose version $DOCKER_COMPOSE_VERSION installed successfully."
else
    echo "Failed to install Docker Compose."
fi