import os
import sys
import django
from django.conf import settings
from django.contrib.wsgi import get_wsgi_application

# PythonAnywhere WSGI Configuration
path = '/home/yourusername/unipath/backend'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'unipath.settings'
django.setup()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
