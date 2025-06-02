#!/usr/bin/env python3
"""
Database setup script for Workplace Management System
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_sqlite():
    """Setup SQLite database (for development)"""
    print("Setting up SQLite database...")
    
    # Create .env file if it doesn't exist
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write("""# Workplace Management System Configuration
DATABASE_URL=sqlite:///workplace_management.db
SECRET_KEY=dev-secret-key-change-in-production
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
PAYSTACK_SECRET_KEY=sk_test_your_key
PAYSTACK_PUBLIC_KEY=pk_test_your_key
OPENAI_API_KEY=your-openai-key
BASE_URL=http://localhost:5000
""")
        print("Created .env file with default values")
        print("Please edit .env file with your actual credentials")
    
    # Import and create app
    from app import create_app, db
    from models.user import User
    from models.subscription import MasterAccess
    
    app = create_app()
    
    with app.app_context():
        # Create all tables
        print("Creating database tables...")
        db.create_all()
        
        # Create default admin user
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@workplace.com',
                full_name='System Administrator',
                phone_number='+2348012345678',
                is_admin=True,
                is_master_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            
            # Grant master access to admin
            master_access = MasterAccess(
                email='admin@workplace.com',
                phone='+2348012345678',
                created_by='system'
            )
            db.session.add(master_access)
            
            db.session.commit()
            print("Created default admin user:")
            print("  Username: admin")
            print("  Password: admin123")
            print("  Email: admin@workplace.com")
        else:
            print("Admin user already exists")
    
    print("SQLite database setup complete!")
    print("Database file: workplace_management.db")

def setup_mysql():
    """Setup MySQL database"""
    print("Setting up MySQL database...")
    
    # Check if MySQL is installed
    try:
        import pymysql
    except ImportError:
        print("PyMySQL not installed. Installing...")
        os.system("pip install PyMySQL")
    
    # Get MySQL credentials
    host = input("MySQL Host (default: localhost): ") or "localhost"
    port = input("MySQL Port (default: 3306): ") or "3306"
    username = input("MySQL Username: ")
    password = input("MySQL Password: ")
    database = input("Database Name (default: workplace_db): ") or "workplace_db"
    
    # Create database URL
    database_url = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
    
    # Test connection
    try:
        import pymysql
        connection = pymysql.connect(
            host=host,
            port=int(port),
            user=username,
            password=password
        )
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
        connection.commit()
        connection.close()
        print(f"Database '{database}' created successfully!")
    except Exception as e:
        print(f"Error creating database: {e}")
        return False
    
    # Update .env file
    env_content = f"""DATABASE_URL={database_url}
SECRET_KEY=your-secret-key-change-in-production
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
PAYSTACK_SECRET_KEY=sk_test_your_key
PAYSTACK_PUBLIC_KEY=pk_test_your_key
OPENAI_API_KEY=your-openai-key
BASE_URL=http://localhost:5000
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("MySQL database setup complete!")
    return True

def setup_neon():
    """Setup Neon PostgreSQL database"""
    print("Setting up Neon PostgreSQL database...")
    
    print("1. Go to https://neon.tech")
    print("2. Create a free account")
    print("3. Create a new project")
    print("4. Copy the connection string")
    
    database_url = input("Enter your Neon database URL: ")
    
    if not database_url:
        print("Database URL is required!")
        return False
    
    # Update .env file
    env_content = f"""DATABASE_URL={database_url}
SECRET_KEY=your-secret-key-change-in-production
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
PAYSTACK_SECRET_KEY=sk_test_your_key
PAYSTACK_PUBLIC_KEY=pk_test_your_key
OPENAI_API_KEY=your-openai-key
BASE_URL=http://localhost:5000
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("Neon PostgreSQL setup complete!")
    return True

def main():
    print("=== Workplace Management System Database Setup ===")
    print()
    print("Choose your database option:")
    print("1. SQLite (Recommended for development/testing)")
    print("2. MySQL (Local installation)")
    print("3. Neon PostgreSQL (Cloud database)")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ")
    
    if choice == '1':
        setup_sqlite()
    elif choice == '2':
        if setup_mysql():
            print("\nNow run: python3 run.py")
    elif choice == '3':
        if setup_neon():
            print("\nNow run: python3 run.py")
    elif choice == '4':
        print("Exiting...")
        sys.exit(0)
    else:
        print("Invalid choice!")
        main()

if __name__ == '__main__':
    main()
