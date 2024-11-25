# Deployment Guide

This guide provides detailed instructions for deploying the AI Code Challenge Generator on AWS EC2.

## Prerequisites

- AWS Account with EC2 access
- SSH key pair
- Domain name (optional)
- API keys:
  - OpenAI API key
  - Tavily API key
  - MongoDB URI (optional)

## Step 1: Launch EC2 Instance

1. **Launch EC2 Instance with these specifications:**
   - AMI: Ubuntu 22.04 LTS or Amazon Linux 2023
   - Type: t3.medium (recommended minimum)
   - Storage: 20GB+ gp3
   - Security Group Settings:
     - SSH (Port 22) from your IP
     - HTTP (Port 80) from anywhere
     - HTTPS (Port 443) from anywhere

2. **Connect to your instance:**
   ```bash
   # For Ubuntu
   ssh -i your-key.pem ubuntu@your-instance-ip
   
   # For Amazon Linux
   ssh -i your-key.pem ec2-user@your-instance-ip
   ```

## Step 2: Initial Setup

1. **Install Git:**
   ```bash
   # For Ubuntu
   sudo apt-get update
   sudo apt-get install -y git

   # For Amazon Linux
   sudo yum update -y
   sudo yum install -y git
   ```

2. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/codegen.git
   cd codegen
   ```

3. **Make setup script executable:**
   ```bash
   # For Ubuntu
   chmod +x scripts/setup_ec2.sh
   ./scripts/setup_ec2.sh

   # For Amazon Linux
   chmod +x scripts/setup_amazon_linux.sh
   ./scripts/setup_amazon_linux.sh
   ```

## Step 3: Configure Environment

1. **Edit the environment file:**
   ```bash
   cd ~/codegen/secrets
   sudo nano .env
   ```

2. **Update these variables with your actual values:**
   ```
   OPENAI_API_KEY=your_actual_openai_key
   TAVILY_API_KEY=your_actual_tavily_key
   USE_MONGODB=false
   MONGODB_URI=your_actual_mongodb_uri
   ```

3. **Save and secure the file:**
   ```bash
   sudo chmod 600 .env
   ```

## Step 4: Configure Nginx

1. **Update Nginx configuration with your domain/IP:**
   ```bash
   # For Ubuntu
   sudo nano /etc/nginx/sites-available/streamlit

   # For Amazon Linux
   sudo nano /etc/nginx/conf.d/streamlit.conf
   ```

2. **Replace `YOUR_DOMAIN_OR_IP` with your actual domain or IP address**

3. **Verify Nginx configuration:**
   ```bash
   sudo nginx -t
   ```

4. **Restart Nginx:**
   ```bash
   sudo systemctl restart nginx
   ```

## Step 5: Start the Application

1. **Return to application directory:**
   ```bash
   cd ~/codegen
   ```

2. **Start the application:**
   ```bash
   docker-compose up -d
   ```

3. **Verify the application is running:**
   ```bash
   docker-compose ps
   docker-compose logs -f
   ```

## Monitoring and Maintenance

### Check Application Status
```bash
# View running containers
docker-compose ps

# View logs
docker-compose logs -f

# Check system resources
htop

# Check Nginx status
sudo systemctl status nginx
```

### Common Issues and Solutions

1. **If Docker containers won't start:**
   ```bash
   # Check logs for errors
   docker-compose logs
   
   # Restart containers
   docker-compose down
   docker-compose up -d
   ```

2. **If Nginx shows errors:**
   ```bash
   # Check Nginx error logs
   sudo tail -f /var/log/nginx/error.log
   
   # Verify configuration
   sudo nginx -t
   ```

3. **If permission issues occur:**
   ```bash
   # Fix ownership
   sudo chown -R $USER:$USER ~/codegen
   
   # Fix .env permissions
   sudo chmod 600 ~/codegen/secrets/.env
   ```

## Security Best Practices

1. **Keep system updated:**
   ```bash
   # For Ubuntu
   sudo apt update && sudo apt upgrade -y
   
   # For Amazon Linux
   sudo yum update -y
   ```

2. **Monitor logs regularly:**
   ```bash
   # Application logs
   docker-compose logs
   
   # System logs
   sudo tail -f /var/log/syslog
   ```

3. **Backup important data:**
   ```bash
   # Backup .env
   cp ~/codegen/secrets/.env ~/codegen/secrets/.env.backup
   ```

4. **AWS Security:**
   - Regularly review security group rules
   - Use AWS CloudWatch for monitoring
   - Enable AWS GuardDuty for threat detection

## Additional Resources

- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/)
- [Docker Documentation](https://docs.docker.com/)
- [Nginx Documentation](https://nginx.org/en/docs/)
