# Workplace Management System - Premium Setup Guide

## Overview
This is a comprehensive workplace management system with premium features including:
- Multi-tier subscription plans (Basic, Professional, Enterprise, Ultimate)
- Payment processing with Paystack
- AI chatbot assistant
- Task management and scheduling
- Workplace chat system
- Library management
- Custom email settings per workplace
- Password reset functionality
- Multi-tenancy with unique workplace URLs

## Prerequisites

1. **Python 3.8+**
2. **MySQL or PostgreSQL database**
3. **Paystack account** (for payments)
4. **OpenAI API key** (for AI chatbot)
5. **Gmail account** (for email notifications)

## Step-by-Step Setup

### 1. Environment Setup

\`\`\`bash
# Create project directory
mkdir workplace-management-premium
cd workplace-management-premium

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
\`\`\`

### 2. Database Configuration

#### Option A: Local MySQL
\`\`\`bash
# Install MySQL and create database
mysql -u root -p
CREATE DATABASE workplace_premium_db;
EXIT;
\`\`\`

#### Option B: Remote Database (Railway/Neon)
- Sign up for Railway or Neon
- Create a new database
- Copy the connection string

### 3. Environment Variables

Create a `.env` file:

\`\`\`env
# Database
DATABASE_URL=mysql+pymysql://username:password@host:port/database_name

# Security
SECRET_KEY=your-very-secure-secret-key-here

# Email Configuration
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password

# Payment Configuration (Paystack)
PAYSTACK_SECRET_KEY=sk_test_your_paystack_secret_key
PAYSTACK_PUBLIC_KEY=pk_test_your_paystack_public_key

# AI Configuration
OPENAI_API_KEY=your-openai-api-key

# Application
BASE_URL=http://localhost:5000
\`\`\`

### 4. Paystack Setup

1. **Create Paystack Account**:
   - Go to https://paystack.com
   - Sign up and verify your account
   - Get your test keys from the dashboard

2. **Configure Webhook** (Optional):
   - Set webhook URL to: `your-domain.com/premium/payment/callback`

### 5. OpenAI Setup

1. **Get API Key**:
   - Go to https://platform.openai.com
   - Create an account and get your API key
   - Add it to your .env file

### 6. Gmail App Password

1. **Enable 2FA** on your Gmail account
2. **Generate App Password**:
   - Google Account → Security → 2-Step Verification → App passwords
   - Select "Mail" and generate password
   - Use this password in MAIL_PASSWORD

### 7. Run the Application

\`\`\`bash
# First run (creates tables and admin user)
python run.py
\`\`\`

Default admin credentials:
- Username: `admin`
- Password: `admin123`
- Email: `admin@workplace.com`

### 8. Initial Configuration

1. **Login as admin**
2. **Create your first workplace**
3. **Set yourself as master admin**:
   - Go to Master Access
   - Grant access to your email
4. **Create subscription plans**
5. **Test payment flow**

## Master Admin Configuration

### Setting Up Master Access

1. **Login as admin**
2. **Go to Premium → Master Access**
3. **Grant access to emails/phones** that can purchase premium plans
4. **Only users with master access can process payments**

### Payment Credentials Setup

The system owner (you) needs to:

1. **Set up Paystack account** with your business details
2. **Configure webhook endpoints** for payment verification
3. **Test payment flow** with test cards
4. **Switch to live keys** for production

## Premium Features by Tier

### Basic (₦5,000/month)
- Seat booking
- Basic attendance
- Limited email notifications (50/month)
- Basic reporting

### Professional (₦15,000/month)
- Everything in Basic
- Unlimited email notifications
- Advanced reporting
- Task scheduling
- Analytics dashboard

### Enterprise (₦35,000/month)
- Everything in Professional
- Task management
- Workplace chat
- Hall-specific chat
- Advanced notifications
- Custom email sender

### Ultimate (₦75,000/month)
- Everything in Enterprise
- Group chat creation
- Chat rooms
- Library management
- AI chatbot assistant
- Advanced reminders
- Priority support

## Multi-Tenancy Features

### Unique Workplace URLs

Each workplace gets a unique registration URL:
- Format: `your-domain.com/register/abc12345`
- Users register directly for that workplace
- Workplace admins can manage their users

### Custom Email Settings

Workplaces can configure their own email sender:
- Custom "From" address for notifications
- Branded email communications
- Workplace-specific email templates

## Security Features

### Password Reset
- Secure token-based password reset
- Email verification required
- Tokens expire after 1 hour

### Access Control
- Master admin controls premium access
- Workplace-level admin permissions
- Feature-based access control

### Payment Security
- Paystack handles all payment processing
- No card details stored locally
- Webhook verification for payments

## Deployment Options

### Option 1: Railway
\`\`\`bash
# Push to GitHub
git init
git add .
git commit -m "Initial commit"
git push origin main

# Deploy on Railway
# Connect GitHub repo
# Add environment variables
# Deploy
\`\`\`

### Option 2: Heroku
\`\`\`bash
# Install Heroku CLI
# Create Heroku app
heroku create your-app-name

# Add environment variables
heroku config:set DATABASE_URL=your-db-url
heroku config:set SECRET_KEY=your-secret-key
# ... add all other env vars

# Deploy
git push heroku main
\`\`\`

### Option 3: VPS/Cloud Server
\`\`\`bash
# Use Docker
docker-compose up --build

# Or manual deployment
# Install dependencies
# Configure nginx
# Set up SSL certificate
# Configure systemd service
\`\`\`

## Testing the System

### 1. Basic Functionality
- User registration and login
- Workplace creation
- Seat booking
- Email notifications

### 2. Premium Features
- Subscription purchase flow
- Payment processing
- Feature access control
- AI chatbot functionality

### 3. Multi-tenancy
- Unique workplace URLs
- Workplace-specific user registration
- Custom email settings

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check DATABASE_URL format
   - Verify database server is running
   - Check credentials

2. **Email Not Sending**
   - Verify Gmail app password
   - Check SMTP settings
   - Test with simple email

3. **Payment Issues**
   - Verify Paystack keys
   - Check webhook configuration
   - Test with Paystack test cards

4. **AI Chatbot Not Working**
   - Verify OpenAI API key
   - Check API quota/billing
   - Test API connection

### Support

For technical support:
- Email: support@workplacemanagement.com
- Documentation: Check the code comments
- Issues: Create GitHub issues

## Production Checklist

- [ ] Change default admin password
- [ ] Use production database
- [ ] Configure SSL certificate
- [ ] Set up monitoring
- [ ] Configure backups
- [ ] Test payment flow
- [ ] Set up domain name
- [ ] Configure email settings
- [ ] Test all premium features
- [ ] Set up error tracking

## Maintenance

### Regular Tasks
- Monitor payment transactions
- Check system performance
- Update dependencies
- Backup database
- Review error logs

### Updates
- Pull latest code changes
- Run database migrations
- Restart application
- Test functionality

This system is now ready for production use with all premium features enabled!
\`\`\`

## Summary

I've successfully upgraded your workplace management system with comprehensive premium features:

### 🎯 **Key Premium Features Added:**

1. **4-Tier Subscription System** (₦5K - ₦75K/month)
2. **Paystack Payment Integration** 
3. **AI Chatbot Assistant** (OpenAI powered)
4. **Multi-tenancy** with unique workplace URLs
5. **Advanced Chat System** (workplace, hall, group chats)
6. **Task Management & Scheduling**
7. **Library Management System**
8. **Password Reset Functionality**
9. **Custom Email Settings** per workplace
10. **Master Admin Access Control**

### 🔐 **Security & Access:**
- Only you (master admin) can grant premium access
- Users must have master access to process payments
- Secure payment processing through Paystack
- Token-based password reset system

### 🎨 **UI/UX Improvements:**
- Fixed text color contrast for dark/light themes
- Premium badges and navigation
- Responsive design improvements
- Better visual hierarchy

### 🚀 **To Run the System:**

1. **Install dependencies:**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

2. **Configure .env file:**
   \`\`\`env
   DATABASE_URL=your-database-url
   SECRET_KEY=your-secret-key
   PAYSTACK_SECRET_KEY=your-paystack-secret
   PAYSTACK_PUBLIC_KEY=your-paystack-public
   OPENAI_API_KEY=your-openai-key
   MAIL_USERNAME=your-email
   MAIL_PASSWORD=your-app-password
   \`\`\`

3. **Run the application:**
   \`\`\`bash
   python run.py
   \`\`\`

4. **Initial setup:**
   - Login as admin (admin/admin123)
   - Go to Master Access and grant yourself premium access
   - Create workplaces and test premium features

### 💳 **Payment Configuration:**
- Get Paystack keys from your dashboard
- Configure webhook URL for payment verification
- Test with Paystack test cards before going live

The system now supports everything you requested - from basic seat booking to advanced AI chatbot assistance, all with proper payment processing and multi-tenant architecture!
