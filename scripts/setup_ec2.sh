#!/bin/bash

echo "Starting EC2 Ubuntu setup script..."

# Update system packages
echo "Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install Docker
echo "Installing Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
rm get-docker.sh  # Clean up the downloaded script

# Install Docker Compose
echo "Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Create app directory and env file directory
echo "Creating application directories..."
mkdir -p ~/codegen
mkdir -p ~/codegen/secrets

# Create a secure env file
echo "Creating and securing environment file..."
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
echo "Adding current user to docker group..."
sudo usermod -aG docker $USER

# Install monitoring tools and nginx
echo "Installing monitoring tools and nginx..."
sudo apt-get update
sudo apt-get install -y htop nginx
if ! sudo systemctl is-active --quiet nginx; then
    echo "Error: Nginx failed to start"
    exit 1
fi
sudo systemctl enable nginx
echo "Nginx installed and running successfully"

# Configure Nginx as reverse proxy
echo "Configuring Nginx as reverse proxy..."
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
echo "Enabling Nginx configuration..."
sudo ln -s /etc/nginx/sites-available/streamlit /etc/nginx/sites-enabled
sudo rm /etc/nginx/sites-enabled/default
sudo systemctl restart nginx

echo "Setup complete! Please:"
echo "1. Update the .env file with your actual credentials at ~/codegen/secrets/.env"
echo "2. Update the Nginx configuration with your actual domain/IP in /etc/nginx/sites-available/streamlit"
echo "3. Log out and log back in for docker group membership to take effect"
echo "4. Verify that Nginx is running: sudo systemctl status nginx"