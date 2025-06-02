#!/usr/bin/env python3
"""
Simple database fix script - drops database and recreates everything
"""

from dotenv import load_dotenv
load_dotenv()

import os
import sys

def simple_database_fix():
    """Simple fix: drop and recreate the entire database"""
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL not found in environment variables")
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
            
            print(f"🔗 Connecting to MySQL:")
            print(f"   Host: {host}:{port}")
            print(f"   User: {username}")
            print(f"   Database: {database_name}")
            
            # Connect without specifying database
            connection = pymysql.connect(
                host=host,
                port=port,
                user=username,
                password=password
            )
            
            cursor = connection.cursor()
            
            # Drop and recreate database
            print(f"🗑️ Dropping database '{database_name}'...")
            cursor.execute(f"DROP DATABASE IF EXISTS {database_name}")
            
            print(f"🔨 Creating database '{database_name}'...")
            cursor.execute(f"CREATE DATABASE {database_name}")
            
            connection.commit()
            connection.close()
            
            print("✅ Database recreated successfully!")
            
            # Now create tables and sample data
            from app import create_app, db
            from models.user import User
            from models.subscription import MasterAccess
            from models.workplace import Workplace
            from models.hall import Hall
            from models.seat import Seat
            from models.timeframe import TimeFrame
            
            app = create_app()
            
            with app.app_context():
                print("🔨 Creating tables...")
                db.create_all()
                
                print("👤 Creating admin user...")
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
                
                print("🏢 Creating sample workplace...")
                workplace = Workplace(
                    name='Sample Workplace',
                    description='A sample workplace for testing the system',
                    address='123 Sample Street, Sample City, Nigeria',
                    contact_email='contact@sampleworkplace.com',
                    phone='+2348012345678'
                )
                db.session.add(workplace)
                db.session.flush()
                
                # Set relationships
                workplace.owner_id = admin.id
                admin.workplace_id = workplace.id
                
                print("🏛️ Creating sample hall...")
                hall = Hall(
                    name='Main Conference Hall',
                    workplace_id=workplace.id,
                    capacity=50,
                    description='Main conference hall with modern facilities'
                )
                db.session.add(hall)
                db.session.flush()
                
                print("💺 Creating seats...")
                for i in range(1, 51):
                    seat = Seat(
                        seat_number=f"S{i:03d}",
                        hall_id=hall.id,
                        position_x=(i % 10) * 60,
                        position_y=(i // 10) * 60
                    )
                    db.session.add(seat)
                
                print("⏰ Creating sample timeframes...")
                from datetime import date, time, timedelta
                
                today = date.today()
                timeframes = [
                    TimeFrame(
                        name='Morning Session',
                        start_time=time(9, 0),
                        end_time=time(12, 0),
                        date=today,
                        max_users=25
                    ),
                    TimeFrame(
                        name='Afternoon Session',
                        start_time=time(14, 0),
                        end_time=time(17, 0),
                        date=today,
                        max_users=30
                    ),
                    TimeFrame(
                        name='Tomorrow Morning',
                        start_time=time(9, 0),
                        end_time=time(12, 0),
                        date=today + timedelta(days=1),
                        max_users=40
                    )
                ]
                
                for timeframe in timeframes:
                    db.session.add(timeframe)
                
                db.session.commit()
                
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
                
                return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("🔧 SIMPLE DATABASE FIX")
    print("=" * 60)
    print("\nThis script will:")
    print("✓ Drop the entire database")
    print("✓ Recreate the database")
    print("✓ Create all tables")
    print("✓ Add sample data")
    print("\n⚠️  WARNING: All existing data will be lost!")
    
    confirm = input("\nContinue? (yes/no): ").lower().strip()
    if confirm in ['yes', 'y']:
        print("\n🔄 Starting simple database fix...")
        if simple_database_fix():
            print("\n🎉 Database fix completed successfully!")
            print("You can now run: python3 run.py")
        else:
            print("\n❌ Database fix failed.")
    else:
        print("❌ Operation cancelled.")

if __name__ == '__main__':
    main()
