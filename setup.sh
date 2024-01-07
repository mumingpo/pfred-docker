#!/bin/bash

# Setup script for PFRED
# must be run with root privilege

# # install and setup docker for ubuntu
# apt-get update
# apt-get install -y ca-certificates curl gnupg
# install -m 0755 -d /etc/apt/keyrings
# curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
# chmod a+r /etc/apt/keyrings/docker.gpg
# echo \
#   "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
#   $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
#   tee /etc/apt/sources.list.d/docker.list > /dev/null
# apt-get update

# apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# install and setup docker for amazon-linux-2023
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user

# build docker image
sudo docker build -t pfredimg:latest .
