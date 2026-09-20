#!/bin/sh

# This script is only for development purposes

sudo docker stop homeassistant 2>/dev/null
sudo docker rm homeassistant 2>/dev/null
find ./custom_components -type d -name "__pycache__" -exec rm -r {} +
sudo mkdir -p /var/ha_config/custom_components
sudo cp -r ./custom_components/* /var/ha_config/custom_components/
docker pull ghcr.io/home-assistant/home-assistant:latest
docker run --name homeassistant -v /var/ha_config:/config -p 8123:8123 ghcr.io/home-assistant/home-assistant:latest
