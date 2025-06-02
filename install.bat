@echo off
echo === Workplace Management System Installation ===
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip

REM Install basic requirements
echo 📥 Installing basic requirements...
pip install Flask Flask-SQLAlchemy Flask-Login Flask-Mail python-dotenv Werkzeug cryptography APScheduler requests

REM Install database driver
echo.
echo Choose database driver:
echo 1. SQLite (default)
echo 2. MySQL
echo 3. PostgreSQL
set /p db_choice="Enter choice (1-3, default: 1): "

if "%db_choice%"=="2" (
    echo 📥 Installing MySQL driver...
    pip install PyMySQL
) else if "%db_choice%"=="3" (
    echo 📥 Installing PostgreSQL driver...
    pip install psycopg2-binary
) else (
    echo 📥 Using SQLite
)

REM Create directories
echo 📁 Creating directories...
mkdir static\uploads\workplace_logos 2>nul
mkdir static\uploads\developer 2>nul
mkdir static\uploads\library 2>nul
mkdir static\uploads\chat_files 2>nul

REM Set up database
echo.
echo 🗄️ Setting up database...
python setup_database.py

echo.
echo ✅ Installation complete!
echo.
echo To start the application:
echo 1. Activate virtual environment: venv\Scripts\activate.bat
echo 2. Run the application: python run.py
echo.
echo Default admin credentials:
echo   Username: admin
echo   Password: admin123
echo   URL: http://localhost:5000
pause
