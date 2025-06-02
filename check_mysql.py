#!/usr/bin/env python3
"""
MySQL connection checker and setup helper
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

def check_mysql_service():
    """Check if MySQL service is running"""
    try:
        import subprocess
        result = subprocess.run(['systemctl', 'is-active', 'mysql'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ MySQL service is running")
            return True
        else:
            print("❌ MySQL service is not running")
            print("Start it with: sudo systemctl start mysql")
            return False
    except Exception as e:
        print(f"❌ Could not check MySQL service: {e}")
        return False

def test_mysql_connection():
    """Test MySQL connection with current credentials"""
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL not found in .env file")
        return False
    
    try:
        import pymysql
        
        # Parse database URL
        if 'mysql+pymysql://' in database_url:
            url_parts = database_url.replace('mysql+pymysql://', '').split('/')
            credentials_host = url_parts[0]
            database_name = url_parts[1] if len(url_parts) > 1 else 'workplace_db'
            
            credentials, host_port = credentials_host.split('@')
            username, password = credentials.split(':')
            host = host_port.split(':')[0]
            port = int(host_port.split(':')[1]) if ':' in host_port else 3306
            
            print(f"🔗 Testing connection:")
            print(f"   Host: {host}:{port}")
            print(f"   User: {username}")
            print(f"   Database: {database_name}")
            
            # Test connection without database first
            connection = pymysql.connect(
                host=host,
                port=port,
                user=username,
                password=password
            )
            
            cursor = connection.cursor()
            
            # Check if database exists
            cursor.execute("SHOW DATABASES")
            databases = [db[0] for db in cursor.fetchall()]
            
            if database_name not in databases:
                print(f"⚠️  Database '{database_name}' does not exist")
                create_db = input(f"Create database '{database_name}'? (y/n): ").lower()
                if create_db in ['y', 'yes']:
                    cursor.execute(f"CREATE DATABASE {database_name}")
                    print(f"✅ Database '{database_name}' created")
                else:
                    connection.close()
                    return False
            else:
                print(f"✅ Database '{database_name}' exists")
            
            # Test connection to the specific database
            connection.close()
            connection = pymysql.connect(
                host=host,
                port=port,
                user=username,
                password=password,
                database=database_name
            )
            
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            
            connection.close()
            
            print("✅ MySQL connection successful!")
            return True
            
    except ImportError:
        print("❌ PyMySQL not installed")
        print("Install it with: pip install PyMySQL")
        return False
    except Exception as e:
        print(f"❌ MySQL connection failed: {e}")
        return False

def setup_mysql_user():
    """Help setup MySQL user and database"""
    print("\n🔧 MySQL Setup Helper")
    print("=" * 30)
    
    print("\n1. Connect to MySQL as root:")
    print("   mysql -u root -p")
    
    print("\n2. Create database:")
    print("   CREATE DATABASE workplace_db;")
    
    print("\n3. Create user:")
    print("   CREATE USER 'workplace_user'@'localhost' IDENTIFIED BY 'qwerty';")
    
    print("\n4. Grant permissions:")
    print("   GRANT ALL PRIVILEGES ON workplace_db.* TO 'workplace_user'@'localhost';")
    print("   FLUSH PRIVILEGES;")
    
    print("\n5. Exit MySQL:")
    print("   EXIT;")
    
    print("\n6. Test connection:")
    print("   mysql -u workplace_user -p workplace_db")

def main():
    print("🔍 MySQL Connection Checker")
    print("=" * 40)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        print("Create .env file with your database configuration")
        return
    
    # Check MySQL service
    print("\n1. Checking MySQL service...")
    if not check_mysql_service():
        return
    
    # Check connection
    print("\n2. Testing database connection...")
    if test_mysql_connection():
        print("\n✅ All checks passed!")
        print("You can now run: python3 run.py")
    else:
        print("\n❌ Connection failed")
        setup_mysql_user()

if __name__ == '__main__':
    main()
