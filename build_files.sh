#!/usr/bin/env bash
echo "🚀 Building Vercel Project..."
python3 --version
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
echo "📦 Collecting static files..."
python3 manage.py collectstatic --noinput --clear
echo "✅ Build Process Complete!"
