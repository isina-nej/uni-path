# PythonAnywhere Deployment Instructions

## Problem Fixed
The backend now accepts **email addresses** as login identifiers instead of just usernames. This allows users to login with:
- Email: `student1@unipath.ir` ✅
- Username: `student1` ✅

## How to Deploy

### Option 1: Using Bash Console (Recommended)

1. Log into https://www.pythonanywhere.com
2. Go to **Consoles** → **Bash console**
3. Run these commands:

```bash
cd /home/isinanej/uni-path/backend/accounts/
nano serializers.py
```

4. The file will open in nano editor
5. Go to line 88 (where `class CustomTokenObtainPairSerializer` starts)
6. Delete the old `validate()` method (lines that start after `def validate(self, attrs):`)
7. Replace with:

```python
    def validate(self, attrs):
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
        
        return data
```

8. Save: Press `Ctrl+O`, then `Enter`, then `Ctrl+X`

### Option 2: Using File Upload

1. In PythonAnywhere, go to **Files** section
2. Navigate to `/home/isinanej/uni-path/backend/accounts/`
3. Click **Upload** and select the modified `serializers.py` file from your local machine

### Option 3: Copy-Paste into Web Editor

1. In PythonAnywhere, go to **Files** section
2. Click on `serializers.py` at `/home/isinanej/uni-path/backend/accounts/serializers.py`
3. The file will open in the web editor
4. Find line 88 where `class CustomTokenObtainPairSerializer` starts
5. Find the `def validate(self, attrs):` method
6. Replace its content with the code from Option 1 above
7. Click **Save** at the top

## After Deployment

The Django app will automatically reload. Test the fix:

```bash
# In PythonAnywhere Bash Console:
curl -X POST https://isinanej.pythonanywhere.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"student1@unipath.ir","password":"Student@123456"}'
```

Expected response: JWT tokens + user data ✅

## Testing in Flutter App

Once deployed, try logging in with:
- **Username/Email:** `student1@unipath.ir`
- **Password:** `Student@123456`

The app should now successfully authenticate!
