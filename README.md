# AI Code Challenge Generator

A Streamlit-based web application that generates, validates, and helps solve coding challenges using AI. The application supports multiple users and integrates with OpenAI's GPT models for intelligent question generation and solution validation.

## 🌟 Features

- **AI-Powered Question Generation**: Creates unique coding challenges using GPT models
- **Interactive Solution Interface**: Write and test solutions in real-time
- **Automated Testing**: Validates solutions against test cases
- **Code Formatting**: Automatically formats submitted code
- **Progress Tracking**: Monitors user progress through challenges
- **MongoDB Integration**: Persistent storage of questions and user progress
- **Multi-user Support**: Handles concurrent users efficiently

## 🛠 Tech Stack

- Python 3.13
- Streamlit
- OpenAI LLMs
- MongoDB
- Docker
- Nginx
- AWS EC2 (for deployment)

## 📋 Prerequisites

- Python 3.13+
- Docker and Docker Compose
- OpenAI API key
- Tavily API key
- MongoDB URI (for production)

## 🚀 Quick Start

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/codegen.git
   cd codegen
   ```

2. **Set Up Environment**
   ```bash
   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**
   Create a `.streamlit/secrets.toml` file:
   ```toml
   OPENAI_API_KEY = "your-openai-key"
   TAVILY_API_KEY = "your-tavily-key"
   MONGODB_URI = "your-mongodb-uri"  # Optional for local development
   ```

4. **Run Locally**
   ```bash
   streamlit run CodeGen.py
   ```

## 🐳 Docker Deployment

1. **Build and Run with Docker Compose**
   ```bash
   docker-compose up --build -d
   ```

2. **Access the Application**
   ```
   http://localhost:8501
   ```

## 🌍 Production Deployment

1. **Prepare EC2 Instance**
   - Launch t3.medium EC2 instance (or larger)
   - Configure security groups for ports 22, 80, 443, 8501

2. **Deploy Application**
   ```bash
   # SSH into EC2 instance
   ssh -i your-key.pem ubuntu@your-ec2-ip

   # Run setup script
   ./scripts/setup_ec2.sh
   ```

3. **Monitor Application**
   ```bash
   # Start monitoring script
   python scripts/monitor.py
   ```

## 📁 Project Structure
See [PROJECT_STRUCTURE](project_structure) for detailed information about the project organization.

## 📊 Database Setup

### Local MongoDB Setup
1. Install MongoDB Community Edition
2. Create database and user:
   ```bash
   mongosh
   use codegen
   db.createUser({
     user: "codegen_user",
     pwd: "your_password",
     roles: ["readWrite"]
   })
   ```

### Migration
To migrate existing JSON data to MongoDB:
```bash
python scripts/migrate_to_mongodb