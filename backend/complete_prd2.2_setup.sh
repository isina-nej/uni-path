#!/bin/bash
# Complete PRD 2.2 Setup Script for PythonAnywhere
# This script sets up all courses, chart schemas, and elective groups

cd ~/uni-path/backend

echo ""
echo "========================================================================"
echo "🎓 PRD 2.2 COMPLETE SETUP - PythonAnywhere"
echo "========================================================================"

echo ""
echo "Step 1: Creating 55 Computer Engineering Courses..."
echo "========================================================================"
python create_degree_chart_v2.py

if [ $? -eq 0 ]; then
    echo "✅ Courses created successfully"
else
    echo "❌ Failed to create courses"
    exit 1
fi

echo ""
echo "Step 2: Setting up Chart Schema with Electives..."
echo "========================================================================"
python setup_chart_schema.py

if [ $? -eq 0 ]; then
    echo "✅ Chart schema setup completed"
else
    echo "❌ Failed to setup chart schema"
    exit 1
fi

echo ""
echo "========================================================================"
echo "✅ PRD 2.2 SETUP COMPLETE!"
echo "========================================================================"
echo ""
echo "Next steps:"
echo "1. Go to PythonAnywhere Web app"
echo "2. Click 'Reload'" 
echo "3. Test in browser:"
echo "   https://isinanej.pythonanywhere.com/admin/courses/chartschema/"
echo ""
