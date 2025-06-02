from dotenv import load_dotenv
load_dotenv()

import os
import sys

def check_database_connection():
    """Check if database connection works"""
    try:
        from app import create_app, db
        from sqlalchemy import text
        
        app = create_app()
        with app.app_context():
            # Try a simple query to test connection using the new SQLAlchemy syntax
            with db.engine.connect() as connection:
                result = connection.execute(text('SELECT 1'))
                result.fetchone()
        return True
    except Exception as e:
        print(f"Database connection error: {e}")
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    missing_deps = []
    
    try:
        import flask
    except ImportError:
        missing_deps.append('Flask')
    
    try:
        import flask_sqlalchemy
    except ImportError:
        missing_deps.append('Flask-SQLAlchemy')
    
    try:
        import flask_login
    except ImportError:
        missing_deps.append('Flask-Login')
    
    try:
        import pymysql
    except ImportError:
        missing_deps.append('PyMySQL')
    
    if missing_deps:
        print("❌ Missing dependencies:")
        for dep in missing_deps:
            print(f"  - {dep}")
        print("\nPlease install them with:")
        print("pip install -r requirements.txt")
        return False
    
    return True

def main():
    print("🚀 Starting Workplace Management System...")
    
    # Check dependencies first
    if not check_dependencies():
        sys.exit(1)
    
    # Check if database is configured
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ Database not configured!")
        print("Please set DATABASE_URL in your .env file")
        print("\nExample for MySQL:")
        print("DATABASE_URL=mysql+pymysql://username:password@localhost:3306/database_name")
        sys.exit(1)
    
    print(f"🔗 Database URL: {database_url.split('@')[1] if '@' in database_url else database_url}")
    
    # Check database connection
    print("🔍 Testing database connection...")
    if not check_database_connection():
        print("❌ Cannot connect to database!")
        print("\nTroubleshooting steps:")
        print("1. Check if MySQL server is running:")
        print("   sudo systemctl status mysql")
        print("   sudo systemctl start mysql")
        print("\n2. Check if database exists:")
        print("   mysql -u workplace_user -p")
        print("   SHOW DATABASES;")
        print("   CREATE DATABASE IF NOT EXISTS workplace_db;")
        print("\n3. Check user permissions:")
        print("   GRANT ALL PRIVILEGES ON workplace_db.* TO 'workplace_user'@'localhost';")
        print("   FLUSH PRIVILEGES;")
        print("\n4. Or run the database fix script:")
        print("   python3 fix_database.py")
        sys.exit(1)
    
    print("✅ Database connection successful!")
    
    # Import app after connection check
    try:
        from app import create_app, db
        from models.user import User
        from models.subscription import MasterAccess
        from models.workplace import Workplace
    except Exception as e:
        print(f"❌ Import error: {e}")
        print("This might be a relationship issue. Try running: python3 fix_database.py")
        sys.exit(1)
    
    app = create_app()
    
    with app.app_context():
        try:
            print("🗄️ Setting up database tables...")
            # Create all database tables
            db.create_all()
            
            # Create default admin user if it doesn't exist
            admin = User.query.filter_by(username='admin').first()
            if not admin:
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
                
                db.session.commit()
                print("✅ Default admin user created:")
                print("  Username: admin")
                print("  Password: admin123")
                print("  Email: admin@workplace.com")
            else:
                print("✅ Admin user already exists")
        
        except Exception as e:
            print(f"❌ Database setup error: {e}")
            print("Try running: python3 fix_database.py")
            sys.exit(1)
    
    # Run the application
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print(f"\n🎉 Application ready!")
    print(f"📍 URL: http://localhost:{port}")
    print(f"👤 Admin Login: admin / admin123")
    print(f"🔧 Debug Mode: {debug}")
    print("=" * 50)
    
    try:
        app.run(host='0.0.0.0', port=port, debug=debug)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Application error: {e}")

if __name__ == '__main__':
    main()
