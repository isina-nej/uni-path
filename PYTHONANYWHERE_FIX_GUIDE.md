# 📋 راهنمای رفع مشکل PythonAnywhere

## مشکل:
- سرور 404 Not Found میده
- `/api/` endpoint پیدا نمی‌شود

## دلیل:
- WSGI file احتمالاً نادرست است یا
- Django تنظیمات اشتباه است یا
- Static files مسئله دارند

---

## ✅ راه‌حل (مرحله به مرحله):

### 1️⃣ وارد PythonAnywhere شو:
```
https://www.pythonanywhere.com/
```

### 2️⃣ رفتن به Bash Console:
```
Click: Consoles → New Console → Bash
```

### 3️⃣ چک کردن مسیر پروژه:
```bash
ls -la /home/isinanej/uni-path/
ls -la /home/isinanej/uni-path/backend/manage.py
```

### 4️⃣ فعال کردن virtualenv و چک Django:
```bash
source /home/isinanej/.virtualenvs/unipath/bin/activate
cd /home/isinanej/uni-path/backend
python manage.py check
```

### 5️⃣ Collect Static Files:
```bash
python manage.py collectstatic --noinput
```

### 6️⃣ بررسی WSGI File:
- رفتن به **Web** tab
- پیدا کردن **WSGI configuration file** (معمولاً `/var/www/isinanej_pythonanywhere_com_wsgi.py`)
- محتوای آن را باید به این صورت باشد:

```python
import os
import sys
import django

path = '/home/isinanej/uni-path/backend'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'unipath.settings'
django.setup()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### 7️⃣ Reload Web App:
- **Web** tab میں سبز **Reload** button کلیک کن
- یا Bash میں:
```bash
touch /var/www/isinanej_pythonanywhere_com_wsgi.py
```

### 8️⃣ تست کردن:
```bash
curl https://isinanej.pythonanywhere.com/api/
```

اگر درست شد، باید JSON response دیدی (نه 404)

---

## اگر هنوز 404 است:

### 🔍 Error Log را چک کن:
1. **Web** tab → **Error log**
2. آخرین خطا ها رو دیدی
3. بگو مشکل چیه!

### 🛠️ اگر مشکل import است:
```bash
cd /home/isinanej/uni-path/backend
python -c "import unipath.settings"
```

### 🛠️ اگر مشکل database است:
```bash
python manage.py migrate
```

---

## 📞 اگر کمک نشد:

بگو:
1. `ls -la /home/isinanej/` (مسیرهای موجود)
2. WSGI file محتویات
3. Error log از PythonAnywhere
