#!/bin/bash

# Update system packages
sudo apt-get update
sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Create app directory
mkdir -p ~/streamlit-app

# Add current user to docker group
sudo usermod -aG docker $USER

# Install monitoring tools
sudo apt-get install -y htop nginx

# Configure Nginx as reverse proxy
sudo tee /etc/nginx/sites-available/streamlit <<EOF
server {
    listen 80;
    server_name YOUR_DOMAIN_OR_IP;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }
}
EOF

# Enable the Nginx site
sudo ln -s /etc/nginx/sites-available/streamlit /etc/nginx/sites-enabled
sudo rm /etc/nginx/sites-enabled/default
sudo systemctl restart nginx 