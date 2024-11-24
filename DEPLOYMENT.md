# Deployment Instructions

## EC2 Instance Setup

### For Ubuntu/Debian
```bash
chmod +x scripts/setup_ec2.sh
./scripts/setup_ec2.sh
```

### For Amazon Linux
```bash
chmod +x scripts/setup_amazon_linux.sh
./scripts/setup_amazon_linux.sh
```

## Setting up Environment Variables

1. SSH into your EC2 instance
2. Navigate to the codegen directory:
   ```bash
   cd ~/codegen/secrets
   ```

3. Edit the .env file with your actual credentials:
   ```bash
   sudo nano .env
   ```

4. Replace the placeholder values with your actual API keys and credentials:
   ```
   OPENAI_API_KEY=your_actual_openai_key
   TAVILY_API_KEY=your_actual_tavily_key
   USE_MONGODB=false
   MONGODB_URI=your_actual_mongodb_uri
   ```

5. Save the file and ensure it has secure permissions:
   ```bash
   sudo chmod 600 .env
   ```

## EC2 Security Group Settings

Ensure your EC2 security group has the following inbound rules:
- HTTP (Port 80) from anywhere (for Nginx)
- HTTPS (Port 443) from anywhere (if using SSL)
- SSH (Port 22) from your IP address

## Starting the Application

After setting up the environment variables:

```bash
cd ~/codegen
docker-compose up -d
```

## Monitoring

Check the application status:
```bash
docker-compose ps
docker-compose logs -f
```

Check Nginx status:
```bash
# For Ubuntu/Debian
sudo systemctl status nginx

# For Amazon Linux
sudo service nginx status
```

## Security Best Practices

- Never commit the .env file to version control
- Keep the .env file outside of the application directory
- Use read-only mounting for the .env file in Docker
- Regularly rotate API keys and credentials
- Consider using AWS Secrets Manager for production deployments
- Use AWS security groups as your primary firewall
- Consider using AWS Certificate Manager for SSL/TLS
