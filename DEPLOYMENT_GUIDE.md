# Workplace Management System - Deployment Guide

## Table of Contents
1. [Local Development Setup](#local-development-setup)
2. [Database Configuration](#database-configuration)
3. [Environment Variables](#environment-variables)
4. [Running Locally](#running-locally)
5. [Deployment Options](#deployment-options)
6. [Post-Deployment Steps](#post-deployment-steps)
7. [Maintenance Tasks](#maintenance-tasks)
8. [Troubleshooting](#troubleshooting)
9. [Security Considerations](#security-considerations)

## Local Development Setup

### 1. Clone the Repository

\`\`\`bash
git clone <repository-url>
cd workplace-management-system
\`\`\`

### 2. Create a Virtual Environment

\`\`\`bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python -m venv venv
source venv/bin/activate
\`\`\`

### 3. Install Dependencies

\`\`\`bash
pip install -r requirements.txt
\`\`\`

## Database Configuration

### Option A: Using Neon PostgreSQL (Recommended)

1. **Create a Neon Account**:
   - Go to [neon.tech](https://neon.tech)
   - Sign up for a free account
   - Verify your email address

2. **Create a New Project**:
   - Click "Create Project"
   - Choose a project name
   - Select a region closest to your users

3. **Get Connection String**:
   - Go to your project dashboard
   - Click on "Connection Details"
   - Copy the connection string
   - It should look like: `postgresql://username:password@hostname:port/database_name`

### Option B: Using Local PostgreSQL

1. **Install PostgreSQL**:
   \`\`\`bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install postgresql postgresql-contrib
   
   # macOS (using Homebrew)
   brew install postgresql
   
   # Windows
   # Download from https://www.postgresql.org/download/windows/
   \`\`\`

2. **Create Database**:
   \`\`\`bash
   sudo -u postgres psql
   CREATE DATABASE workplace_management;
   CREATE USER workplace_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE workplace_management TO workplace_user;
   \q
   \`\`\`

### Option C: Using SQLite (Development Only)

For quick testing, you can use SQLite:
\`\`\`bash
# No setup required - just use this in your .env file:
DATABASE_URL=sqlite:///workplace_management.db
\`\`\`

## Environment Variables

Create a `.env` file in the root directory:

\`\`\`env
# Database Configuration
DATABASE_URL=postgresql://username:password@hostname:port/database_name

# Security
SECRET_KEY=your-very-secure-secret-key-change-this-in-production

# Email Configuration (for notifications)
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com

# Application Configuration
BASE_URL=http://localhost:5000
FLASK_ENV=development
\`\`\`

### Setting up Gmail for Email Notifications

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Select "Mail" and generate password
   - Use this password in `MAIL_PASSWORD`

## Running Locally

### 1. Initialize the Database

\`\`\`bash
# This will create tables and default admin user
python run.py
\`\`\`

### 2. Start the Application

\`\`\`bash
# Method 1: Using Flask CLI
flask run

# Method 2: Using Python directly
python run.py

# Method 3: With specific host and port
python run.py --host=0.0.0.0 --port=5000
\`\`\`

### 3. Access the Application

- Open your browser and go to `http://localhost:5000`
- **Default Admin Credentials**:
  - Username: `admin`
  - Password: `admin123`
  - Email: `admin@workplace.com`

## Deployment Options

### Option 1: Deploy to Vercel

1. **Install Vercel CLI**:
   \`\`\`bash
   npm install -g vercel
   \`\`\`

2. **Create vercel.json**:
   \`\`\`json
   {
     "version": 2,
     "builds": [
       {
         "src": "run.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "run.py"
       }
     ],
     "env": {
       "PYTHONPATH": "."
     }
   }
   \`\`\`

3. **Deploy**:
   \`\`\`bash
   vercel
   \`\`\`

4. **Set Environment Variables**:
   - Go to Vercel dashboard
   - Select your project
   - Go to Settings → Environment Variables
   - Add all variables from your `.env` file

### Option 2: Deploy to Heroku

1. **Install Heroku CLI**:
   \`\`\`bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   \`\`\`

2. **Create Procfile**:
   \`\`\`
   web: gunicorn run:app
   release: python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
   \`\`\`

3. **Add Gunicorn to requirements.txt**:
   \`\`\`
   gunicorn==20.1.0
   \`\`\`

4. **Deploy Steps**:
   \`\`\`bash
   # Initialize git (if not done)
   git init
   git add .
   git commit -m "Initial commit"
   
   # Create Heroku app
   heroku create your-app-name
   
   # Set environment variables
   heroku config:set SECRET_KEY=your-secure-secret-key
   heroku config:set DATABASE_URL=your-database-url
   heroku config:set MAIL_USERNAME=your-email@gmail.com
   heroku config:set MAIL_PASSWORD=your-app-password
   heroku config:set MAIL_DEFAULT_SENDER=your-email@gmail.com
   heroku config:set BASE_URL=https://your-app-name.herokuapp.com
   
   # Deploy
   git push heroku main
   \`\`\`

### Option 3: Deploy to Railway

1. **Create Railway Account**:
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Deploy from GitHub**:
   - Connect your GitHub repository
   - Railway will automatically detect it's a Python app
   - Add environment variables in the Railway dashboard

3. **Add Environment Variables**:
   - Go to your project dashboard
   - Click on "Variables"
   - Add all variables from your `.env` file

### Option 4: Deploy with Docker

1. **Create Dockerfile**:
   \`\`\`dockerfile
   FROM python:3.9-slim

   WORKDIR /app

   # Install system dependencies
   RUN apt-get update && apt-get install -y \
       gcc \
       default-libmysqlclient-dev \
       pkg-config \
       && rm -rf /var/lib/apt/lists/*

   # Copy requirements and install Python dependencies
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   # Copy application code
   COPY . .

   # Create uploads directory
   RUN mkdir -p static/uploads

   # Expose port
   EXPOSE 5000

   # Run the application
   CMD ["python", "run.py"]
   \`\`\`

2. **Create docker-compose.yml**:
   \`\`\`yaml
   version: '3.8'

   services:
     web:
       build: .
       ports:
         - "5000:5000"
       environment:
         - DATABASE_URL=postgresql://workplace_user:password@db:5432/workplace_db
         - SECRET_KEY=your-secure-secret-key
         - MAIL_USERNAME=your-email@gmail.com
         - MAIL_PASSWORD=your-app-password
         - MAIL_DEFAULT_SENDER=your-email@gmail.com
         - BASE_URL=http://localhost:5000
       depends_on:
         - db
       volumes:
         - ./static/uploads:/app/static/uploads

     db:
       image: postgres:13
       environment:
         - POSTGRES_USER=workplace_user
         - POSTGRES_PASSWORD=password
         - POSTGRES_DB=workplace_db
       ports:
         - "5432:5432"
       volumes:
         - postgres_data:/var/lib/postgresql/data

   volumes:
     postgres_data:
   \`\`\`

3. **Build and Run**:
   \`\`\`bash
   docker-compose up --build
   \`\`\`

### Option 5: Deploy to VPS/Cloud Server

1. **Server Setup** (Ubuntu example):
   \`\`\`bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python and dependencies
   sudo apt install python3 python3-pip python3-venv nginx supervisor -y
   
   # Install PostgreSQL
   sudo apt install postgresql postgresql-contrib -y
   \`\`\`

2. **Application Setup**:
   \`\`\`bash
   # Clone repository
   git clone <your-repo-url> /var/www/workplace-management
   cd /var/www/workplace-management
   
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   pip install gunicorn
   \`\`\`

3. **Configure Nginx**:
   ```nginx
   # /etc/nginx/sites-available/workplace-management
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }

       location /static {
           alias /var/www/workplace-management/static;
       }
   }
   \`\`\`

4. **Configure Supervisor**:
   \`\`\`ini
   # /etc/supervisor/conf.d/workplace-management.conf
   [program:workplace-management]
   command=/var/www/workplace-management/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 run:app
   directory=/var/www/workplace-management
   user=www-data
   autostart=true
   autorestart=true
   redirect_stderr=true
   stdout_logfile=/var/log/workplace-management.log
   \`\`\`

5. **Enable and Start Services**:
   \`\`\`bash
   # Enable Nginx site
   sudo ln -s /etc/nginx/sites-available/workplace-management /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl reload nginx
   
   # Start Supervisor
   sudo supervisorctl reread
   sudo supervisorctl update
   sudo supervisorctl start workplace-management
   \`\`\`

## Post-Deployment Steps

### 1. Change Default Admin Password

1. Log in with default credentials (`admin` / `admin123`)
2. Go to your profile or admin settings
3. Change password to a secure one
4. Update email address if needed

### 2. Create Initial Data

1. **Create Workplaces**:
   - Go to Admin Dashboard
   - Click "Workplaces" → "Add Workplace"
   - Fill in workplace details

2. **Create Halls**:
   - Go to "Halls" → "Add Hall"
   - Select workplace and set capacity
   - Seats will be automatically created

3. **Create Time Frames**:
   - Go to "Time Frames" → "Add Time Frame"
   - Set dates, times, and user limits

### 3. Test Core Functionality

1. **User Registration**:
   - Register a test user
   - Verify email notifications work

2. **Seat Booking**:
   - Book a seat as a regular user
   - Check booking confirmation email

3. **Admin Functions**:
   - View bookings in admin dashboard
   - Test user management features

### 4. Configure File Storage

\`\`\`bash
# Ensure upload directories exist and have proper permissions
mkdir -p static/uploads/workplace_logos
mkdir -p static/uploads/developer
chmod 755 static/uploads
chmod 755 static/uploads/workplace_logos
chmod 755 static/uploads/developer
\`\`\`

## Maintenance Tasks

### 1. Database Backups

#### For Neon PostgreSQL:
- Neon provides automatic backups
- You can also create manual backups from the dashboard

#### For Self-hosted PostgreSQL:
\`\`\`bash
# Create backup
pg_dump -h hostname -U username -d database_name > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore backup
psql -h hostname -U username -d database_name &lt; backup_file.sql

# Automated backup script
#!/bin/bash
BACKUP_DIR="/path/to/backups"
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -h localhost -U workplace_user workplace_db > $BACKUP_DIR/workplace_backup_$DATE.sql

# Keep only last 7 days of backups
find $BACKUP_DIR -name "workplace_backup_*.sql" -mtime +7 -delete
\`\`\`

### 2. Log Management

\`\`\`bash
# View application logs
tail -f /var/log/workplace-management.log

# Rotate logs (add to crontab)
0 0 * * * /usr/sbin/logrotate /etc/logrotate.d/workplace-management
\`\`\`

### 3. Update Dependencies

\`\`\`bash
# Check for outdated packages
pip list --outdated

# Update packages
pip install --upgrade package_name

# Update all packages (be careful in production)
pip freeze > requirements_old.txt
pip install --upgrade -r requirements.txt

# Test thoroughly after updates
python -m pytest  # if you have tests
\`\`\`

### 4. Monitor Performance

1. **Database Performance**:
   - Monitor query execution times
   - Check for slow queries
   - Optimize indexes if needed

2. **Application Performance**:
   - Monitor response times
   - Check memory usage
   - Monitor disk space

3. **Set up Monitoring** (optional):
   \`\`\`bash
   # Install monitoring tools
   pip install flask-monitoring-dashboard
   
   # Add to your app
   from flask_monitoringdashboard import bind
   bind(app)
   \`\`\`

## Troubleshooting

### Database Connection Issues

1. **Check Connection String**:
   ```python
   # Test database connection
   from sqlalchemy import create_engine
   engine = create_engine('your-database-url')
   connection = engine.connect()
   result = connection.execute('SELECT 1')
   print(result.fetchone())
   \`\`\`

2. **Common Issues**:
   - Incorrect hostname or port
   - Wrong username/password
   - Database doesn't exist
   - Network connectivity issues
   - SSL certificate problems

3. **Solutions**:
   \`\`\`bash
   # Test network connectivity
   ping your-database-host
   
   # Test port connectivity
   telnet your-database-host 5432
   
   # Check database exists
   psql -h hostname -U username -l
   \`\`\`

### Email Sending Failures

1. **Gmail Issues**:
   - Ensure 2FA is enabled
   - Use App Password, not regular password
   - Check "Less secure app access" settings

2. **SMTP Issues**:
   ```python
   # Test SMTP connection
   import smtplib
   server = smtplib.SMTP('smtp.gmail.com', 587)
   server.starttls()
   server.login('your-email@gmail.com', 'your-app-password')
   server.quit()
   \`\`\`

3. **Common Solutions**:
   - Verify SMTP settings
   - Check firewall rules
   - Test with different email provider

### File Upload Problems

1. **Permission Issues**:
   \`\`\`bash
   # Fix permissions
   sudo chown -R www-data:www-data static/uploads
   sudo chmod -R 755 static/uploads
   \`\`\`

2. **Directory Issues**:
   \`\`\`bash
   # Create missing directories
   mkdir -p static/uploads/workplace_logos
   mkdir -p static/uploads/developer
   \`\`\`

3. **Size Limits**:
   ```python
   # Check file size limits in config.py
   MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
   \`\`\`

### Application Errors

1. **Check Logs**:
   \`\`\`bash
   # Application logs
   tail -f /var/log/workplace-management.log
   
   # System logs
   sudo journalctl -u your-service-name -f
   
   # Nginx logs
   sudo tail -f /var/log/nginx/error.log
   \`\`\`

2. **Debug Mode**:
   ```python
   # Enable debug mode (development only)
   app.run(debug=True)
   \`\`\`

3. **Common Issues**:
   - Missing environment variables
   - Import errors
   - Database migration issues
   - Template not found errors

### Performance Issues

1. **Database Optimization**:
   \`\`\`sql
   -- Check slow queries
   SELECT query, mean_time, calls 
   FROM pg_stat_statements 
   ORDER BY mean_time DESC 
   LIMIT 10;
   
   -- Add indexes for frequently queried columns
   CREATE INDEX idx_bookings_user_id ON bookings(user_id);
   CREATE INDEX idx_bookings_timeframe_id ON bookings(timeframe_id);
   \`\`\`

2. **Application Optimization**:
   - Use database connection pooling
   - Implement caching for frequently accessed data
   - Optimize database queries
   - Use pagination for large datasets

## Security Considerations

### 1. Secure Your Secret Key

```python
# Generate a secure secret key
import secrets
secret_key = secrets.token_hex(32)
print(secret_key)
