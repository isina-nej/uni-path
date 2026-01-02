#!/usr/bin/env python
"""
Automatic deployment script for PythonAnywhere
Run this in the PythonAnywhere Bash console to apply the email-to-username fix
"""

import os
import sys

# Change to the correct directory
os.chdir('/home/isinanej/uni-path/backend/accounts')

# Read the current serializers.py
with open('serializers.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Create backup
with open('serializers.py.backup', 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ Backup created: serializers.py.backup")

# Define the old validate method (to find and replace)
old_validate = '''    def validate(self, attrs):
        """
        Validate credentials and return user info along with token.
        """
        data = super().validate(attrs)
        
        # Add user information to response
        user = self.user
        data['user'] = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        
        return data'''

# Define the new validate method with email support
new_validate = '''    def validate(self, attrs):
        """
        Validate credentials and return user info along with token.
        Converts email input to username automatically.
        """
        # If 'username' field contains an email, try to find user by email first
        username_input = attrs.get('username', '')
        if '@' in username_input:
            try:
                user = User.objects.get(email=username_input)
                attrs['username'] = user.username
            except User.DoesNotExist:
                pass  # Fall back to normal validation
        
        data = super().validate(attrs)
        
        # Add user information to response
        user = self.user
        data['user'] = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        
        return data'''

# Apply the fix
if old_validate in content:
    content = content.replace(old_validate, new_validate)
    with open('serializers.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Serializers.py updated successfully!")
    print("\n📧 Email-to-username fix applied!")
    print("   Users can now login with: email@domain.com")
else:
    print("❌ Could not find the old validate method")
    print("This might mean the file has already been updated or has a different format")
    sys.exit(1)

print("\n🔄 Reloading Django app...")
# Reload the web app
try:
    import urllib.request
    urllib.request.urlopen('https://www.pythonanywhere.com/api/v0/user/isinanej/webapps/isinanej.pythonanywhere.com/reload/', timeout=5)
    print("✅ App reload triggered!")
except Exception as e:
    print(f"ℹ️  Could not auto-reload via API. Please manually reload in PythonAnywhere web interface.")
    print(f"   Go to: https://www.pythonanywhere.com/user/isinanej/webapps/")

print("\n✨ Deployment complete! Test with:")
print("   curl -X POST https://isinanej.pythonanywhere.com/api/auth/login/ \\")
print("     -H 'Content-Type: application/json' \\")
print("     -d '{\"username\":\"student1@unipath.ir\",\"password\":\"Student@123456\"}'")
