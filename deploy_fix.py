#!/usr/bin/env python
"""
Deploy the email-to-username fix to PythonAnywhere
This script uploads the modified serializers.py to the server
"""

import subprocess
import sys

# The modified serializers.py content
serializers_content = open('backend/accounts/serializers.py', 'r', encoding='utf-8').read()

print("📤 Modified serializers.py is ready to deploy")
print(f"File size: {len(serializers_content)} bytes")
print("\nTo deploy, you need to:")
print("1. Log into PythonAnywhere web console")
print("2. Use Bash console to navigate to: /home/isinanej/uni-path/backend/accounts/")
print("3. Edit serializers.py with nano or vim")
print("4. Or use: curl -X POST https://www.pythonanywhere.com/api/v0/... (requires API token)")
print("\nAlternatively, copy the file content below and paste it into PythonAnywhere:")
print("\n" + "="*80)
print(serializers_content)
print("="*80)
