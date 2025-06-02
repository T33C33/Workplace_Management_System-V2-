#!/bin/bash

echo "=== Workplace Management System Installation ==="
echo

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install basic requirements
echo "📥 Installing basic requirements..."
pip install Flask Flask-SQLAlchemy Flask-Login Flask-Mail python-dotenv Werkzeug cryptography APScheduler requests

# Install database driver based on choice
echo
echo "Choose database driver:"
echo "1. SQLite (default, no additional driver needed)"
echo "2. MySQL (installs PyMySQL)"
echo "3. PostgreSQL (installs psycopg2-binary)"
read -p "Enter choice (1-3, default: 1): " db_choice

case $db_choice in
    2)
        echo "📥 Installing MySQL driver..."
        pip install PyMySQL
        ;;
    3)
        echo "📥 Installing PostgreSQL driver..."
        pip install psycopg2-binary
        ;;
    *)
        echo "📥 Using SQLite (no additional driver needed)"
        ;;
esac

# Ask about optional features
echo
read -p "Install AI chatbot support? (y/N): " install_ai
if [[ $install_ai =~ ^[Yy]$ ]]; then
    echo "📥 Installing OpenAI..."
    pip install openai
fi

read -p "Install real-time chat support? (y/N): " install_socketio
if [[ $install_socketio =~ ^[Yy]$ ]]; then
    echo "📥 Installing SocketIO..."
    pip install flask-socketio python-socketio
fi

# Create directories
echo "📁 Creating directories..."
mkdir -p static/uploads/workplace_logos
mkdir -p static/uploads/developer
mkdir -p static/uploads/library
mkdir -p static/uploads/chat_files

# Set up database
echo
echo "🗄️ Setting up database..."
python3 setup_database.py

echo
echo "✅ Installation complete!"
echo
echo "To start the application:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Run the application: python3 run.py"
echo
echo "Default admin credentials:"
echo "  Username: admin"
echo "  Password: admin123"
echo "  URL: http://localhost:5000"
