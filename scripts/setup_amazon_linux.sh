#!/bin/bash

# Exit on any error
set -e

echo "Starting Amazon Linux EC2 setup script..."

# Update system packages
echo "Updating system packages..."
sudo yum update -y

# Install Docker
echo "Installing Docker..."
sudo yum install -y docker
sudo systemctl start docker
if ! sudo systemctl is-active --quiet docker; then
    echo "Error: Docker failed to start"
    exit 1
fi
sudo systemctl enable docker
echo "Docker installed and running successfully"

# Install Docker Compose
echo "Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
if ! docker-compose --version > /dev/null 2>&1; then
    echo "Error: Docker Compose installation failed"
    exit 1
fi
echo "Docker Compose installed successfully"

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
echo "Environment file created and secured"

# Add current user to docker group
echo "Adding current user to docker group..."
sudo usermod -aG docker $USER

# Install monitoring tools
echo "Installing monitoring tools..."
sudo yum install -y htop nginx

# Configure Nginx as reverse proxy
echo "Configuring Nginx as reverse proxy..."
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
echo "Starting Nginx service..."
sudo systemctl start nginx
if ! sudo systemctl is-active --quiet nginx; then
    echo "Error: Nginx failed to start"
    exit 1
fi
sudo systemctl enable nginx
echo "Nginx configured and running successfully"

# Verify installations
echo -e "\nVerifying installations:"
echo "Docker version: $(docker --version)"
echo "Docker Compose version: $(docker-compose --version)"
echo "Nginx version: $(nginx -v 2>&1)"

echo -e "\nSetup complete! Please:"
echo "1. Update the .env file with your actual credentials at ~/codegen/secrets/.env"
echo "2. Update the Nginx configuration with your actual domain/IP in /etc/nginx/conf.d/streamlit.conf"
echo "3. Log out and log back in for docker group membership to take effect"
echo "4. Verify that Nginx is running: sudo systemctl status nginx"
echo "5. Check firewall status: sudo firewall-cmd --state"
echo -e "\nNote: If using AWS, make sure to configure security groups to allow HTTP (80) and HTTPS (443) traffic" 