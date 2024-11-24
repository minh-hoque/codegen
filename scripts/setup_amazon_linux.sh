#!/bin/bash

# Update system packages
sudo yum update -y

# Install Docker
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Create app directory and env file directory
mkdir -p ~/codegen
mkdir -p ~/codegen/secrets

# Create a secure env file
sudo tee ~/codegen/secrets/.env <<EOF
OPENAI_API_KEY=your_openai_key_here
TAVILY_API_KEY=your_tavily_key_here
USE_MONGODB=false
MONGODB_URI=your_mongodb_uri_here

# Production settings
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_ENABLE_CORS=false
STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=true
EOF

# Secure the env file
sudo chmod 600 ~/codegen/secrets/.env

# Add current user to docker group
sudo usermod -aG docker $USER

# Install monitoring tools (Amazon Linux alternatives)
sudo yum install -y htop nginx

# Configure Nginx as reverse proxy
sudo tee /etc/nginx/conf.d/streamlit.conf <<EOF
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

# Start and enable Nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# Configure firewall (using AWS security groups is recommended instead)
sudo yum install -y firewalld
sudo systemctl start firewalld
sudo systemctl enable firewalld
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload

echo "Setup complete! Please:"
echo "1. Update the .env file with your actual credentials"
echo "2. Update the Nginx configuration with your actual domain/IP"
echo "3. Log out and log back in for docker group membership to take effect" 