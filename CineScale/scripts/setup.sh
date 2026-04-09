#!/bin/bash

echo "🚀 CineScale Setup Script"
echo "=========================="

# Check Python version
echo "Checking Python version..."
python3 --version

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created. Please update with your configuration."
else
    echo "⚠️  .env file already exists. Skipping..."
fi

# Create storage directories
echo "Creating storage directories..."
mkdir -p storage/raw storage/output storage/thumbnails

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env file with your configuration"
echo "2. Start Redis: docker run -d -p 6379:6379 redis:7-alpine"
echo "3. Run the API: python run.py"
echo "4. Or use Docker: docker-compose up --build"
