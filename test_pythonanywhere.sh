#!/bin/bash
# Test script for PythonAnywhere deployment

echo "======================================"
echo "Testing PythonAnywhere Deployment"
echo "======================================"

# 1. Check if backend folder exists
echo ""
echo "1️⃣ Checking backend folder..."
if [ -d "/home/isinanej/uni-path/backend" ]; then
    echo "✅ Backend folder found"
    ls -la /home/isinanej/uni-path/backend | head -10
else
    echo "❌ Backend folder NOT found"
    echo "Checking alternative paths..."
    find /home/isinanej -name "manage.py" 2>/dev/null
fi

# 2. Check virtualenv
echo ""
echo "2️⃣ Checking virtualenv..."
if [ -d "/home/isinanej/.virtualenvs/unipath" ]; then
    echo "✅ Virtualenv found"
else
    echo "❌ Virtualenv NOT found"
fi

# 3. Check Django settings
echo ""
echo "3️⃣ Checking Django settings..."
source /home/isinanej/.virtualenvs/unipath/bin/activate
cd /home/isinanej/uni-path/backend
python manage.py check

# 4. Test API endpoint
echo ""
echo "4️⃣ Testing API URL structure..."
python manage.py shell << 'EOF'
from django.urls import get_resolver
urls = get_resolver().url_patterns
print("\n📋 Available URL patterns:")
for pattern in urls:
    print(f"  • {pattern.pattern}")
EOF

echo ""
echo "======================================"
echo "Test Complete!"
echo "======================================"
