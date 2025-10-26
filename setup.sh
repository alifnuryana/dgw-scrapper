#!/bin/bash

# DGW Scrapper Setup Script
# This script helps you set up the DGW Scrapper environment

echo "🚀 DGW Scrapper Setup Script"
echo "=============================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.8"

if [ -z "$python_version" ]; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python $python_version found"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists. Skipping..."
else
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip
echo ""

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Install Playwright browsers
echo "🌐 Installing Playwright browsers..."
playwright install chromium
echo "✅ Playwright browsers installed"
echo ""

# Create output directory
echo "📁 Creating output directory..."
mkdir -p output
echo "✅ Output directory created"
echo ""

# Setup complete
echo "✨ Setup complete! ✨"
echo ""
echo "To use DGW Scrapper:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the scraper: python main.py --email YOUR_EMAIL --password YOUR_PASSWORD --from_date DD/MM/YYYY --to_date DD/MM/YYYY"
echo ""
echo "Example:"
echo "python main.py --email user@example.com --password pass123 --from_date 01/01/2024 --to_date 31/01/2024"
echo ""
echo "For more information, see README.md"
