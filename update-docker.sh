#!/bin/bash

# Get the ID of the only running container
CONTAINER_ID=$(sudo docker ps -q)

if [ -n "$CONTAINER_ID" ]; then
    echo "Stopping container: $CONTAINER_ID"
    sudo docker stop $CONTAINER_ID
else
    echo "No running containers found"
fi

echo "Pulling latest changes from main branch..."
git pull origin main

echo "Building new Docker image..."
sudo docker build -t computer-use-demo:latest .

echo "Process completed"