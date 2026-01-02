# Creating Test Data on PythonAnywhere Server

The Flutter app is working and can call the API, but test users need to exist on the **PythonAnywhere server database** (not the local one).

## Quick Steps

### Option 1: Use PythonAnywhere Bash Console (Easiest)

1. Log in to [PythonAnywhere Dashboard](https://www.pythonanywhere.com)
2. Go to **Consoles** → Click **Bash** (Create a new one if needed)
3. Run these commands:

```bash
cd /home/isinanej/uni-path/backend
source /home/isinanej/.virtualenvs/unipath/bin/activate
python create_test_data.py
```

4. You should see output like:
```
✅ داده‌های تست ایجاد شد!
```

### Option 2: Run via Django Management Command

```bash
cd /home/isinanej/uni-path/backend
source /home/isinanej/.virtualenvs/unipath/bin/activate
python manage.py shell < create_test_data.py
```

---

## Test Login Credentials (After Running Script)

| Username | Email | Password | Role |
|----------|-------|----------|------|
| student1 | student1@unipath.ir | Student@123456 | Student |
| student2 | student2@unipath.ir | Student@123456 | Student |
| professor1 | professor1@unipath.ir | Professor@123456 | Professor |

---

## Verify Test Data on Server

To verify users were created, from the Bash console:

```bash
python manage.py shell
```

Then in the Python shell:

```python
from accounts.models import User
for u in User.objects.all():
    print(f"{u.username} - {u.email}")
```

---

## If Users Still Fail to Login

If credentials still don't work after creating users:

1. **Reset a user's password** (from Django shell):
   ```python
   from accounts.models import User
   u = User.objects.get(username='student1')
   u.set_password('Student@123456')
   u.save()
   print("Password updated")
   ```

2. **Verify the password hashing**:
   ```python
   u = User.objects.get(username='student1')
   print(u.check_password('Student@123456'))  # Should print True
   ```

3. **Test login manually from bash**:
   ```bash
   curl -X POST https://isinanej.pythonanywhere.com/api/auth/login/ \
     -H "Content-Type: application/json" \
     -d '{"username":"student1","password":"Student@123456"}'
   ```

---

## Flutter App Login

Once test users exist on the server, in the Flutter app login screen enter:

- **Email**: `student1@unipath.ir`
- **Password**: `Student@123456`

(Or use the generated credentials from the table above.)

Then tap **ورود** (Login button).
