#!/bin/bash

# Variables
CONTAINER_NAME="my-mysql-container"
ROOT_PASSWORD="Thaothaothao223051"
DB_NAME="managelibrary"

# Pull MySQL Docker image
docker pull mysql

# Create and start the MySQL container
docker run -d \
  --name $CONTAINER_NAME \
  -e MYSQL_ROOT_PASSWORD=$ROOT_PASSWORD \
  -e MYSQL_DATABASE=$DB_NAME \
  -p 3306:3306 \
  mysql

# Wait for container initialization
echo "Waiting for container to initialize..."
sleep 10

# Verify if the container is running
if [ "$(docker container inspect -f '{{.State.Running}}' $CONTAINER_NAME)" = "true" ]; then
  echo "MySQL container is running."
else
  echo "MySQL container failed to start. Please check the logs."
  exit 1
fi

# Print connection details
echo "MySQL Database Details:"
echo "Host: 127.0.0.1"
echo "Port: 3306"
echo "Username: root"
echo "Password: $ROOT_PASSWORD"
echo "Database: $DB_NAME"
