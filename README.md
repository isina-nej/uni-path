# UniPath - Academic Course Selection & Recommendation System

سیستم هوشمند انتخاب و توصیه واحدهای درسی دانشگاهی

## 📋 نمای کلی

UniPath یک پلتفرم جامع برای ساده‌سازی فرآیند انتخاب واحدهای درسی دانشجویان است. این سیستم:
- ✅ **بررسی خودکار پیش‌نیازها** - اطمینان از رعایت شرایط
- 📊 **الگوریتم امتیازبندی هوشمند** - اولویت‌بندی بر اساس اهمیت درس
- 📅 **برنامه‌ریزی هفتگی** - مشاهده و بررسی برخورد ساعات درسی
- 👥 **مدیریت نقش‌های مختلف** - دانشجو، استاد، ادمین، مدیر گروه
- 🔔 **سیستم اعلان‌ها** - اطلاع‌رسانی به موقع

## 🏗️ معماری پروژه

پروژه شامل دو قسمت اصلی است:

```
unipath/
├── frontend/                # Flutter Mobile App
│   ├── unipath/             # Flutter project root
│   │   ├── lib/             # Dart source code
│   │   ├── pubspec.yaml      # Flutter dependencies
│   │   └── README.md
│   └── README.md
│
├── backend/                 # Django REST API
│   ├── unipath/             # Project settings
│   ├── students/            # Students app
│   ├── courses/             # Courses app
│   ├── manage.py
│   ├── requirements.txt
│   └── README.md
│
├── openspec/                # OpenSpec Documentation
│   ├── AGENTS.md            # AI Assistant guidelines
│   ├── project.md           # Project specs
│   ├── changes/             # Change proposals
│   │   └── init-unipath-project/
│   │       ├── proposal.md
│   │       └── tasks.md
│   └── specs/               # Feature specifications
│
├── prd/                     # Product Requirements
│   └── prd1.1.md            # Main PRD
│
├── AGENTS.md                # OpenSpec instructions
├── architecture.md          # System architecture
├── rules.md                 # Project rules
└── README.md                # This file
```

## 🚀 شروع سریع

### 📱 Frontend (Flutter)

```bash
cd frontend/unipath

# Install dependencies
flutter pub get

# Run app on web
flutter run -d chrome

# Or on Android emulator
flutter run -d emulator-5554

# Or on iOS (macOS only)
flutter run -d iPhone
```

**See [frontend/README.md](frontend/README.md) for detailed setup instructions.**

### 🔙 Backend (Django)

```bash
cd backend

# Virtual environment is already created at .venv
# Activate it:

# Windows:
.venv\Scripts\activate

# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

Server runs at: **http://localhost:8000/**
Admin panel: **http://localhost:8000/admin/**

**See [backend/README.md](backend/README.md) for detailed setup instructions.**

## 📱 رابط‌های API

### احراز هویت
```
POST /api/v1/token/              - دریافت توکن
POST /api/v1/token/refresh/      - تجدید توکن
```

### دروس
```
GET /api/v1/courses/             - لیست دروس
GET /api/v1/courses/{id}/        - جزئیات درس
GET /api/v1/courses/{id}/prerequisites/
```

### انتخاب واحد
```
GET /api/v1/selections/          - درس‌های انتخابی فعلی
POST /api/v1/selections/         - انتخاب درس جدید
DELETE /api/v1/selections/{id}/  - حذف انتخاب
```

### تاریخ درسی
```
GET /api/v1/course-history/      - تاریخ درسی دانشجو
GET /api/v1/course-history/passed-courses/
```

### برنامه درسی
```
GET /api/v1/degree-charts/       - لیست برنامه‌های درسی
GET /api/v1/degree-charts/{id}/courses/
```

### اعلان‌ها
```
GET /api/v1/notifications/       - اعلان‌های کاربر
GET /api/v1/notifications/unread/
POST /api/v1/notifications/{id}/mark-as-read/
```

## 👥 نقش‌های کاربران

| نقش | توصیف | دسترسی |
|-----|------|--------|
| **دانشجو** | انتخاب واحد و مشاهده توصیه | مشاهده دروس، انتخاب، تاریخچه |
| **استاد** | مدیریت پیش‌نیازها و نمرات | تعریف پیش‌نیازها، ثبت نمرات |
| **ادمین** | مدیریت سیستم | تمام دسترسی‌ها |
| **مدیر گروه** | مدیریت برنامه درسی | مدیریت برنامه رشته |

## 📊 مدل‌های پایگاه داده

### UserProfile
پروفایل تعمیم‌یافته کاربر با اطلاعات نقش و بخش

### Course
اطلاعات درس شامل کد، نام، تعداد واحد و امتیاز اهمیت

### Prerequisite
وابستگی‌های درسی (پیش‌نیاز و هم‌نیاز)

### StudentCourseHistory
تاریخ درسی و نمرات دانشجویان

### StudentSelection
انتخاب‌های فعلی درس‌های دانشجو

### DegreeChart
ساختار برنامه درسی رشته‌ها

### ChartCourse
دروس موجود در برنامه درسی

### Notification
سیستم اعلان‌ها برای کاربران

## ⚙️ تنظیمات محیط

### متغیرهای محیطی (.env)

```env
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=unipath_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# Redis/Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

## 🧪 تست و توسعه

### اجرای تست‌ها
```bash
python manage.py test
```

### ایجاد Migration
```bash
python manage.py makemigrations
python manage.py migrate
```

### رابط ادمین
```
http://localhost:8000/admin/
```

## 📚 OpenSpec Workflow

این پروژه از OpenSpec برای مدیریت تغییرات استفاده می‌کند:

- **Specs** (`openspec/specs/`) - مشخصات فعلی سیستم
- **Changes** (`openspec/changes/`) - پیشنهادات تغییر
- **Archive** (`openspec/changes/archive/`) - تغییرات تکمیل‌شده

### ایجاد تغییر جدید

```bash
openspec list              # مشاهده تغییرات فعلی
openspec spec list --long  # مشاهده مشخصات
```

## 🔧 نیازمندی‌های فناوری

### Frontend
- Flutter 3.0+
- Dart 3.0+
- HTTP, Provider, Shared Preferences

### Backend
- Python 3.9+
- Django 4.2+
- PostgreSQL 12+
- Redis (اختیاری)
- DRF, CORS, Celery

## 📝 مستندات اضافی

- [Frontend README](./unipath-frontend/unipath/README.md)
- [Backend README](./unipath-backend/README.md)
- [Product Requirements](./prd/prd1.1.md)
- [Architecture](./architecture.md)
- [Rules](./rules.md)
- [User Cases (فارسی)](./use-cast.md)

## 🤝 مشارکت

برای مشارکت در پروژه:

1. یک Proposal ایجاد کنید (`openspec` workflow)
2. پس از تایید، تغییرات را پیاده‌سازی کنید
3. کد را تست کنید
4. PR ارسال کنید

## 📄 لایسنس

UniPath © 2024 - تمام حقوق محفوظ است

---

**آخرین بروزرسانی:** 27 دسامبر 2024
