#!/usr/bin/env python3
"""
Database fix script for relationship issues - handles circular dependencies
"""

from dotenv import load_dotenv
load_dotenv()

import os
import sys
from sqlalchemy import text, MetaData
# Import models at the module level
from app import create_app, db
from models.user import User
from models.subscription import MasterAccess, Subscription
from models.workplace import Workplace
from models.hall import Hall
from models.seat import Seat
from models.timeframe import TimeFrame
from models.booking import Booking
from models.attendance import Attendance

def test_mysql_connection():
    """Test MySQL connection before proceeding"""
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL not found in environment variables")
        return False
    
    try:
        import pymysql
        from sqlalchemy import create_engine
        
        # Parse database URL
        if 'mysql+pymysql://' in database_url:
            # Extract connection details
            url_parts = database_url.replace('mysql+pymysql://', '').split('/')
            credentials_host = url_parts[0]
            database_name = url_parts[1] if len(url_parts) > 1 else 'workplace_db'
            
            credentials, host_port = credentials_host.split('@')
            username, password = credentials.split(':')
            host = host_port.split(':')[0]
            port = int(host_port.split(':')[1]) if ':' in host_port else 3306
            
            print(f"🔗 Testing connection to MySQL:")
            print(f"   Host: {host}:{port}")
            print(f"   User: {username}")
            print(f"   Database: {database_name}")
            
            # Test connection
            engine = create_engine(database_url)
            with engine.connect() as connection:
                result = connection.execute(text('SELECT 1'))
                result.fetchone()
            
            print("✅ MySQL connection successful!")
            return True
        else:
            print("❌ Invalid database URL format")
            return False
            
    except ImportError:
        print("❌ PyMySQL not installed. Run: pip install PyMySQL")
        return False
    except Exception as e:
        print(f"❌ MySQL connection failed: {e}")
        print("\nTroubleshooting:")
        print("1. Check if MySQL is running: sudo systemctl status mysql")
        print("2. Start MySQL if needed: sudo systemctl start mysql")
        print("3. Check database exists:")
        print("   mysql -u workplace_user -p")
        print("   SHOW DATABASES;")
        print("   CREATE DATABASE IF NOT EXISTS workplace_db;")
        return False

def drop_tables_manually():
    """Manually drop tables in the correct order to avoid circular dependency"""
    try:
        with db.engine.connect() as connection:
            # Disable foreign key checks
            connection.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
            
            # Get all table names
            result = connection.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result.fetchall()]
            
            print(f"📋 Found {len(tables)} tables to drop")
            
            # Drop each table
            for table in tables:
                print(f"🗑️ Dropping table: {table}")
                connection.execute(text(f"DROP TABLE IF EXISTS `{table}`"))
            
            # Re-enable foreign key checks
            connection.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
            
            # Commit the transaction
            connection.commit()
            
            print("✅ All tables dropped successfully")
            return True
            
    except Exception as e:
        print(f"❌ Error dropping tables manually: {e}")
        return False

def fix_database():
    """Fix database relationships and recreate tables if needed"""
    if not test_mysql_connection():
        return False
    
    try:
        app = create_app()
        
        with app.app_context():
            print("🗄️ Fixing database...")
            
            # Try to drop tables manually first
            print("🔄 Dropping existing tables manually...")
            if not drop_tables_manually():
                print("❌ Failed to drop tables manually")
                return False
            
            # Recreate all tables with fixed relationships
            print("🔨 Creating tables with fixed relationships...")
            db.create_all()
            
            # Create default admin user
            print("👤 Creating default admin user...")
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
            
            # Commit admin user first
            db.session.commit()
            
            # Create a sample workplace
            print("🏢 Creating sample workplace...")
            workplace = Workplace(
                name='Sample Workplace',
                description='A sample workplace for testing the system',
                address='123 Sample Street, Sample City, Nigeria',
                contact_email='contact@sampleworkplace.com',
                phone='+2348012345678'
            )
            db.session.add(workplace)
            db.session.flush()  # Get the workplace ID
            
            # Now update the relationships
            workplace.owner_id = admin.id
            admin.workplace_id = workplace.id
            
            # Create a sample hall
            print("🏛️ Creating sample hall...")
            hall = Hall(
                name='Main Conference Hall',
                workplace_id=workplace.id,
                capacity=50,
                description='Main conference hall with modern facilities'
            )
            db.session.add(hall)
            db.session.flush()  # Get the hall ID
            
            # Create seats for the hall
            print("💺 Creating seats...")
            for i in range(1, 51):
                seat = Seat(
                    seat_number=f"S{i:03d}",
                    hall_id=hall.id,
                    position_x=(i % 10) * 60,  # Arrange in rows
                    position_y=(i // 10) * 60
                )
                db.session.add(seat)
            
            # Create sample timeframes
            print("⏰ Creating sample timeframes...")
            from datetime import date, time, timedelta
            
            # Today's sessions
            today = date.today()
            timeframes = [
                {
                    'name': 'Morning Session',
                    'start_time': time(9, 0),
                    'end_time': time(12, 0),
                    'date': today,
                    'max_users': 25
                },
                {
                    'name': 'Afternoon Session',
                    'start_time': time(14, 0),
                    'end_time': time(17, 0),
                    'date': today,
                    'max_users': 30
                },
                {
                    'name': 'Tomorrow Morning',
                    'start_time': time(9, 0),
                    'end_time': time(12, 0),
                    'date': today + timedelta(days=1),
                    'max_users': 40
                }
            ]
            
            for tf_data in timeframes:
                timeframe = TimeFrame(**tf_data)
                db.session.add(timeframe)
            
            # Commit all changes
            db.session.commit()
            
            print("✅ Database fixed successfully!")
            print("\n" + "="*50)
            print("🎉 SETUP COMPLETE!")
            print("="*50)
            print("\n📋 Default credentials:")
            print("  Username: admin")
            print("  Password: admin123")
            print("  Email: admin@workplace.com")
            print("\n🏢 Sample data created:")
            print("  - Sample Workplace")
            print("  - Main Conference Hall with 50 seats")
            print("  - 3 sample timeframes")
            print("\n🚀 Next steps:")
            print("  1. Run: python3 run.py")
            print("  2. Open: http://localhost:5000")
            print("  3. Login with admin credentials")
            print("  4. Explore the system!")
            
    except Exception as e:
        print(f"❌ Error fixing database: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def alternative_fix():
    """Alternative fix using raw SQL to handle circular dependencies"""
    print("\n🔄 Trying alternative fix method...")
    
    try:
        app = create_app()
        
        with app.app_context():
            with db.engine.connect() as connection:
                # Disable foreign key checks
                connection.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
                
                # Drop all tables
                result = connection.execute(text("SHOW TABLES"))
                tables = [row[0] for row in result.fetchall()]
                
                for table in tables:
                    connection.execute(text(f"DROP TABLE IF EXISTS `{table}`"))
                
                # Re-enable foreign key checks
                connection.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
                
                # Commit the changes
                connection.commit()
            
            # Now create tables
            db.create_all()
            
            print("✅ Alternative fix successful!")
            return True
            
    except Exception as e:
        print(f"❌ Alternative fix failed: {e}")
        return False

def main():
    print("=" * 60)
    print("🔧 WORKPLACE MANAGEMENT SYSTEM - DATABASE FIX")
    print("=" * 60)
    print("\nThis script will:")
    print("✓ Test database connection")
    print("✓ Drop and recreate all tables (handles circular dependencies)")
    print("✓ Create admin user and sample data")
    print("✓ Fix relationship issues")
    print("\n⚠️  WARNING: All existing data will be lost!")
    
    confirm = input("\nContinue? (yes/no): ").lower().strip()
    if confirm in ['yes', 'y']:
        print("\n🔄 Starting database fix...")
        
        if fix_database():
            print("\n🎉 Database fix completed successfully!")
            print("You can now run: python3 run.py")
        else:
            print("\n❌ Primary fix failed. Trying alternative method...")
            if alternative_fix():
                print("\n🎉 Alternative fix completed successfully!")
                print("You can now run: python3 run.py")
            else:
                print("\n❌ All fix methods failed. Please check the error messages above.")
                print("\nManual solution:")
                print("1. Connect to MySQL: mysql -u workplace_user -p")
                print("2. Drop database: DROP DATABASE workplace_db;")
                print("3. Create database: CREATE DATABASE workplace_db;")
                print("4. Run this script again")
    else:
        print("❌ Operation cancelled.")

if __name__ == '__main__':
    main()
