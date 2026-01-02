# ============================================================
# PythonAnywhere WSGI Configuration for isinanej.pythonanywhere.com
# This file should be located at: /var/www/isinanej_pythonanywhere_com_wsgi.py
# ============================================================

import os
import sys
import django

# Add the project directory to the path
path = '/home/isinanej/uni-path/backend'
if path not in sys.path:
    sys.path.insert(0, path)

# Set Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'unipath.settings'

# Setup Django
django.setup()

# Get the WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
 