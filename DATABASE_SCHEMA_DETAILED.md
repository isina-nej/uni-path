# ساختار دیتابیس Unipath - توضیحات مفصل

## مقدمه
دیتابیس پروژه Unipath برای مدیریت نظام آموزشی دانشگاه طراحی شده است. این سیستم شامل کاربران با نقش‌های مختلف، برنامه‌های درجه (رشته‌های تحصیلی)، دوره‌ها و مسیر تحصیلی دانشجویان است.

**موتور دیتابیس:** SQLite3  
**نسخه Django:** 6.0  
**مکان فایل:** `backend/db.sqlite3`

---

## جداول Accounts (سیستم احراز هویت و کاربران)

### 1. جدول `accounts_user`
**نوع:** کاربر سفارشی (Custom User Model)

#### ساختار:
```
┌─────────────────────────────────────────┐
│         accounts_user                   │
├─────────────────────────────────────────┤
│ id (PK)                                 │
│ username (VARCHAR, UNIQUE)              │
│ email (VARCHAR, UNIQUE)                 │
│ first_name (VARCHAR)                    │
│ last_name (VARCHAR)                     │
│ password (VARCHAR)                      │
│ role* (VARCHAR) → student/professor/... │
│ is_active (BOOLEAN)                     │
│ is_staff (BOOLEAN)                      │
│ is_superuser (BOOLEAN)                  │
│ last_login (DATETIME)                   │
│ date_joined (DATETIME)                  │
│ created_at (DATETIME)                   │
│ updated_at (DATETIME)                   │
└─────────────────────────────────────────┘
```

#### فیلدهای اصلی:
| فیلد | نوع | توضیح |
|------|------|-------|
| `id` | PrimaryKey | شناسه منحصر به‌فرد |
| `username` | CharField | نام کاربری (UNIQUE) |
| `email` | EmailField | پست الکترونیکی |
| `first_name` | CharField | نام |
| `last_name` | CharField | نام خانوادگی |
| `password` | CharField | رمز عبور (هش شده) |
| **`role`** ⭐ | CharField | نقش کاربر: `student`, `professor`, `admin`, `hod` |
| `is_active` | BooleanField | آیا فعال است؟ (برای حذف نرم) |
| `is_staff` | BooleanField | دسترسی به پنل مدیریت Django |
| `is_superuser` | BooleanField | مجوز کامل سیستم |
| `created_at` | DateTimeField | تاریخ ایجاد |
| `updated_at` | DateTimeField | تاریخ آخرین به‌روزرسانی |

#### چرا ایجاد شد؟
Django یک مدل User پیش‌فرض دارد اما نیاز بود **نقش‌های مختلف** (student/professor/admin/hod) را تمیز کنند. این مدل سفارشی اجازه می‌دهد:
- تفریق بین انواع کاربران
- تنیین دسترسی‌های متفاوت برای هر نقش
- ذخیره اطلاعات خاص کاربر

#### کجا به کار می‌رود:
- ✅ احراز هویت و ورود (Login)
- ✅ سیستم JWT (TokenAuthentication)
- ✅ مجوزها (Permissions) - هر نقش دسترسی متفاوت دارد
- ✅ تاریخچه کوئری‌ها (آن query‌ها فیلتر می‌شوند برای کاربر)
- ✅ نمایش پروفایل

---

### 2. جدول `accounts_profile`
**نوع:** پروفایل توسیع‌شده (OneToOneField با User)

#### ساختار:
```
┌──────────────────────────────────────────┐
│      accounts_profile                    │
├──────────────────────────────────────────┤
│ id (PK)                                  │
│ user_id (FK) → accounts_user [UNIQUE]    │
│ student_number (VARCHAR) [UNIQUE]        │
│ phone (VARCHAR)                          │
│ bio (TEXT)                               │
│ avatar (ImageField)                      │
│ major_id (FK) → courses_degreechart      │
│ department (VARCHAR)                     │
│ created_at (DATETIME)                    │
│ updated_at (DATETIME)                    │
└──────────────────────────────────────────┘
```

#### فیلدهای اصلی:
| فیلد | نوع | توضیح |
|------|------|-------|
| `id` | PrimaryKey | شناسه |
| **`user_id`** ⭐ | OneToOneField | اتصال یکتا به جدول accounts_user (هر کاربر فقط یک پروفایل دارد) |
| `student_number` | CharField | شماره دانشجویی (UNIQUE برای دانشجویان) |
| `phone` | CharField | شماره تلفن |
| `bio` | TextField | درباره‌ای / بیوگرافی |
| `avatar` | ImageField | تصویر پروفایل (`avatars/` فولدر) |
| **`major_id`** ⭐ | ForeignKey | رشته تحصیلی (FK → DegreeChart) - فقط برای دانشجویان |
| `department` | CharField | بخش (برای اساتید) |
| `created_at` | DateTimeField | تاریخ ایجاد |
| `updated_at` | DateTimeField | تاریخ آخرین ویرایش |

#### چرا ایجاد شد؟
جدول User از Django پایه‌ای است و فیلدهای مینیمالی دارد. Profile برای اضافه کردن اطلاعات خاص‌تر ایجاد شد:
- شماره دانشجویی
- رشته تحصیلی
- تصویر و اطلاعات شخصی

#### کجا به کار می‌رود:
- ✅ نمایش اطلاعات مفصل کاربر
- ✅ فیلتر دانشجویان برحسب رشته
- ✅ بخش‌ها برای اساتید
- ✅ نوار جانبی (Sidebar) برنامه

---

## جداول Courses (دوره‌ها و برنامه‌های درجه)

### 3. جدول `courses_degreechart`
**نوع:** برنامه درجه (رشته تحصیلی)

#### ساختار:
```
┌──────────────────────────────────────────┐
│     courses_degreechart                  │
├──────────────────────────────────────────┤
│ id (PK)                                  │
│ name (VARCHAR)                           │
│ code (VARCHAR) [UNIQUE]                  │
│ description (TEXT)                       │
│ department (VARCHAR)                     │
│ total_credits (INT)                      │
│ created_at (DATETIME)                    │
│ updated_at (DATETIME)                    │
└──────────────────────────────────────────┘
```

#### فیلدهای اصلی:
| فیلد | نوع | توضیح |
|------|------|-------|
| `id` | PrimaryKey | شناسه |
| `name` | CharField | نام رشته (مثلاً "کامپیوتر") |
| **`code`** ⭐ | CharField | کد یکتا (مثلاً "CS01") |
| `description` | TextField | توضیح رشته و اهداف آن |
| `department` | CharField | نام بخش (مثلاً "دانشکده مهندسی") |
| **`total_credits`** ⭐ | IntegerField | تعداد واحدهای لازم برای فارغ‌التحصیلی (مثلاً 120) |
| `created_at` | DateTimeField | تاریخ ایجاد |
| `updated_at` | DateTimeField | تاریخ آخرین ویرایش |

#### محدودیت‌ها:
- `total_credits` باید بین 30 و 200 باشد

#### چرا ایجاد شد؟
برنامه درجه (Degree Chart) نقالق ساختار تمام دوره‌های یک رشته را نشان می‌دهد. هر رشته:
- دوره‌های مختلفی دارد
- واحدهای مختلفی نیاز است
- پیش‌نیازی‌های مختلفی دارد

#### کجا به کار می‌رود:
- ✅ انتخاب رشته برای دانشجوی جدید
- ✅ مسیر توصیاتی (پیشنهاد دوره‌های بعدی)
- ✅ محاسبه سطح پیشرفت دانشجو
- ✅ نمایش تمام دوره‌های یک رشته

---

### 4. جدول `courses_course`
**نوع:** دوره / درس

#### ساختار:
```
┌──────────────────────────────────────────────┐
│         courses_course                       │
├──────────────────────────────────────────────┤
│ id (PK)                                      │
│ name (VARCHAR)                               │
│ code (VARCHAR) [UNIQUE]                      │
│ description (TEXT)                           │
│ credits (INT)                                │
│ unit_type (VARCHAR) → theory/practical/both  │
│ theoretical_units (INT)                      │
│ practical_units (INT)                        │
│ day_of_week (VARCHAR)                        │
│ start_time (TIME)                            │
│ end_time (TIME)                              │
│ semester (INT)                               │
│ is_mandatory (BOOLEAN)                       │
│ is_offered (BOOLEAN)                         │
│ instructor (VARCHAR)                         │
│ capacity (INT)                               │
│ created_at (DATETIME)                        │
│ updated_at (DATETIME)                        │
└──────────────────────────────────────────────┘
```

#### فیلدهای اصلی:
| فیلد | نوع | توضیح |
|------|------|-------|
| `id` | PrimaryKey | شناسه |
| `name` | CharField | نام دوره (مثلاً "ریاضیات عمومی 1") |
| **`code`** ⭐ | CharField | کد دوره (مثلاً "MATH101") |
| `description` | TextField | توضیح محتوای دوره |
| **`credits`** ⭐ | IntegerField | تعداد واحد (1-6) |
| `unit_type` | CharField | نوع دوره: `theory` / `practical` / `both` |
| `theoretical_units` | IntegerField | ساعت درس تئوری در هفته |
| `practical_units` | IntegerField | ساعت آزمایشگاه/عملی در هفته |
| `day_of_week` | CharField | روز برگزاری (sat/sun/mon/...) |
| `start_time` | TimeField | ساعت شروع (مثلاً 08:00) |
| `end_time` | TimeField | ساعت پایان (مثلاً 10:00) |
| `semester` | IntegerField | ترم توصیه‌شده (1-8) |
| **`is_mandatory`** ⭐ | BooleanField | آیا الزامی است یا انتخابی؟ |
| **`is_offered`** ⭐ | BooleanField | آیا این ترم ارائه شده است؟ |
| `instructor` | CharField | نام استاد |
| `capacity` | IntegerField | ظرفیت کلاس (تعداد دانشجویانی که می‌تواند شرکت کند) |
| `created_at` | DateTimeField | تاریخ ایجاد |
| `updated_at` | DateTimeField | تاریخ آخرین ویرایش |

#### محدودیت‌ها:
- `credits` باید بین 1 و 6 باشد
- `semester` باید بین 1 و 8 باشد

#### چرا ایجاد شد؟
هر دوره‌ای که در دانشگاه ارائه می‌شود نیاز به:
- نام و کد یکتا
- توضیح محتوا
- تعداد واحد (برای محاسبه GPA)
- برنامه زمانی (زمان و مکان)
- نام استاد

#### کجا به کار می‌رود:
- ✅ انتخاب درس توسط دانشجو
- ✅ برنامه‌ریزی درس (زمان‌بندی کلاس)
- ✅ محاسبه بار تحصیلی دانشجو
- ✅ نمایش پیش‌نیازی‌ها و هم‌نیازی‌ها
- ✅ جستجو و فیلترکردن دروس

---

### 5. جدول `courses_chartcourse`
**نوع:** ارتباط دوره با برنامه درجه (Many-to-Many با اطلاعات اضافی)

#### ساختار:
```
┌────────────────────────────────────────┐
│      courses_chartcourse               │
├────────────────────────────────────────┤
│ id (PK)                                │
│ degree_chart_id (FK) →                 │
│   courses_degreechart [COMPOSITE_KEY]  │
│ course_id (FK) →                       │
│   courses_course [COMPOSITE_KEY]       │
│ is_mandatory (BOOLEAN)                 │
│ recommended_semester (INT)             │
│ importance_score (FLOAT)               │
│ created_at (DATETIME)                  │
│ updated_at (DATETIME)                  │
└────────────────────────────────────────┘
```

#### فیلدهای اصلی:
| فیلد | نوع | توضیح |
|------|------|-------|
| `id` | PrimaryKey | شناسه |
| **`degree_chart_id`** ⭐ | ForeignKey | رشته تحصیلی (FK → DegreeChart) |
| **`course_id`** ⭐ | ForeignKey | دوره (FK → Course) |
| `is_mandatory` | BooleanField | آیا برای این رشته الزامی است؟ |
| `recommended_semester` | IntegerField | ترم توصیه‌شده برای این رشته (1-8) |
| **`importance_score`** ⭐ | FloatField | امتیاز اهمیت (تعداد دروس وابسته) |
| `created_at` | DateTimeField | تاریخ ایجاد |
| `updated_at` | DateTimeField | تاریخ آخرین ویرایش |

#### محدودیت‌ها:
- **Unique Constraint:** `(degree_chart_id, course_id)` - هر دوره فقط یک بار برای هر رشته می‌تواند تعریف شود
- **Unique Constraint:** `recommended_semester` باید بین 1 و 8 باشد

#### چرا ایجاد شد؟
یک دوره می‌تواند در چندین رشته استفاده شود، اما:
- برای رشته A الزامی است ولی برای رشته B انتخابی
- ترم توصیه‌شده برای هر رشته متفاوت است
- اهمیت دوره نسبت به رشته متفاوت است

**مثال:**
- دوره "ریاضیات عمومی" برای کامپیوتر الزامی است اما برای علوم اجتماعی انتخابی
- برای کامپیوتر ترم 1 توصیه می‌شود اما برای مهندسی شیمی ترم 2

#### کجا به کار می‌رود:
- ✅ مسیر توصیاتی (گفتن به دانشجو "شما بعد از یا دوره X دوره Y بگیرید")
- ✅ محاسبه سطح پیشرفت برحسب رشته
- ✅ نمایش دروس الزامی و انتخابی
- ✅ الگوریتم توصیه دروس

---

### 6. جدول `courses_prerequisite`
**نوع:** پیش‌نیازی‌ها

#### ساختار:
```
┌──────────────────────────────────────────────┐
│       courses_prerequisite                   │
├──────────────────────────────────────────────┤
│ id (PK)                                      │
│ course_id (FK) → courses_course              │
│   [درسی که نیاز دارد]                       │
│ prerequisite_course_id (FK) → courses_course │
│   [درسی که اول باید انجام شود]             │
│ is_corequisite (BOOLEAN)                     │
│ min_grade (VARCHAR)                          │
│ created_at (DATETIME)                        │
└──────────────────────────────────────────────┘
```

#### فیلدهای اصلی:
| فیلد | نوع | توضیح |
|------|------|-------|
| `id` | PrimaryKey | شناسه |
| **`course_id`** ⭐ | ForeignKey | دروسی که نیاز دارد (FK → Course) |
| **`prerequisite_course_id`** ⭐ | ForeignKey | پیش‌نیاز (درسی که باید اول انجام شود) |
| `is_corequisite` | BooleanField | آیا هم‌نیاز است؟ (می‌تواند همزمان انجام شود) |
| `min_grade` | CharField | حداقل نمره مورد نیاز (A, B, C, D) |
| `created_at` | DateTimeField | تاریخ ایجاد |

#### محدودیت‌ها:
- **Unique Constraint:** `(course_id, prerequisite_course_id)` - یک پیش‌نیاز فقط یک بار می‌تواند تعریف شود

#### چرا ایجاد شد؟
بسیاری از دروس نیاز به پیش‌دانش دارند:
- ریاضیات عمومی 2 نیاز به ریاضیات عمومی 1 دارد
- فیزیک 2 نیاز به فیزیک 1 دارد
- بعضی دروس باید همزمان انجام شوند

#### کجا به کار می‌رود:
- ✅ اعتبارسنجی انتخاب درس (جلوگیری از انتخاب درسی که پیش‌نیاز ندارد)
- ✅ نمایش پیش‌نیازی‌ها برای دانشجو
- ✅ توصیه ترتیب دروس
- ✅ تشخیص درس‌های قابل انجام

---

### 7. جدول `courses_corequisite`
**نوع:** دروس هم‌نیاز

#### ساختار:
```
┌──────────────────────────────────────────────┐
│        courses_corequisite                   │
├──────────────────────────────────────────────┤
│ id (PK)                                      │
│ course_id (FK) → courses_course              │
│   [درسی که نیاز به هم‌نیاز دارد]            │
│ corequisite_course_id (FK) → courses_course  │
│   [درسی که باید همزمان انجام شود]          │
│ created_at (DATETIME)                        │
└──────────────────────────────────────────────┘
```

#### فیلدهای اصلی:
| فیلد | نوع | توضیح |
|------|------|-------|
| `id` | PrimaryKey | شناسه |
| **`course_id`** ⭐ | ForeignKey | درسی که نیاز دارد |
| **`corequisite_course_id`** ⭐ | ForeignKey | درسی که باید همزمان انجام شود |
| `created_at` | DateTimeField | تاریخ ایجاد |

#### محدودیت‌ها:
- **Unique Constraint:** `(course_id, corequisite_course_id)`

#### چرا ایجاد شد؟
بعضی دروس باید **همزمان** انجام شوند:
- **مثال:** درس "شیمی عملی" باید همزمان با "شیمی تئوری" انجام شود
- درس "آزمایشگاه فیزیک" باید همزمان با "فیزیک" انجام شود

#### کجا به کار می‌رود:
- ✅ اعتبارسنجی انتخاب درس
- ✅ اطلاع دانشجو که دروس باید همزمان انجام شوند
- ✅ جلوگیری از انتخاب درس بدون هم‌نیاز

---

## جداول Students (مسیر تحصیلی دانشجویان)

### 8. جدول `students_studentcoursehistory`
**نوع:** تاریخچه دروس گذرانده‌شده

#### ساختار:
```
┌───────────────────────────────────────────┐
│   students_studentcoursehistory           │
├───────────────────────────────────────────┤
│ id (PK)                                   │
│ student_id (FK) → accounts_user           │
│ course_id (FK) → courses_course           │
│ grade (VARCHAR)                           │
│ grade_points (FLOAT)                      │
│ semester (VARCHAR)                        │
│ credits_earned (INT)                      │
│ is_passed (BOOLEAN)                       │
│ notes (TEXT)                              │
│ created_at (DATETIME)                     │
│ updated_at (DATETIME)                     │
└───────────────────────────────────────────┘
```

#### فیلدهای اصلی:
| فیلد | نوع | توضیح |
|------|------|-------|
| `id` | PrimaryKey | شناسه |
| **`student_id`** ⭐ | ForeignKey | دانشجو (FK → User) |
| **`course_id`** ⭐ | ForeignKey | دوره (FK → Course) |
| **`grade`** ⭐ | CharField | نمره: A, A-, B+, B, B-, C+, C, D, F, W (Withdrawal) |
| **`grade_points`** ⭐ | FloatField | نمره عددی (0.0-4.0) |
| **`semester`** ⭐ | CharField | ترمی که انجام شد (مثلاً "Spring 1402") |
| **`credits_earned`** ⭐ | IntegerField | واحدهای کسب‌شده (0 اگر ریپیت شود) |
| `is_passed` | BooleanField | آیا درس پاس شد؟ |
| `notes` | TextField | توضیحات اضافی |
| `created_at` | DateTimeField | تاریخ ایجاد رکورد |
| `updated_at` | DateTimeField | تاریخ آخرین ویرایش |

#### محدودیت‌ها:
- `grade_points` بین 0.0 و 4.0
- `credits_earned` بین 0 و 6
- **Unique Constraint:** `(student_id, course_id, semester)` - یک دانشجو نمی‌تواند یک درس را دو بار در یک ترم بگیرد

#### چرا ایجاد شد؟
این جدول **سجل تحصیلی** دانشجو است:
- کدام دروس را در کدام ترم گذرانده است
- نمره هر درس
- آیا پاس کرده است یا نه

#### کجا به کار می‌رود:
- ✅ نمایش سابقه تحصیلی / کارنامه
- ✅ محاسبه GPA (معدل)
- ✅ محاسبه تعداد واحدهای کسب‌شده
- ✅ بررسی پیش‌نیازی‌ها (آیا دانشجو یک درس پیش‌نیاز را پاس کرده؟)
- ✅ توصیه دروس بعدی بر اساس دروس کسب‌شده
- ✅ اعتبارسنجی تکرار درس

---

### 9. جدول `students_studentselection`
**نوع:** انتخاب درس برای ترم آینده

#### ساختار:
```
┌────────────────────────────────────────────┐
│     students_studentselection              │
├────────────────────────────────────────────┤
│ id (PK)                                    │
│ student_id (FK) → accounts_user            │
│ course_id (FK) → courses_course            │
│ semester (VARCHAR)                         │
│ selected_at (DATETIME)                     │
│ is_confirmed (BOOLEAN)                     │
│ confirmed_at (DATETIME)                    │
│ notes (TEXT)                               │
│ created_at (DATETIME)                      │
│ updated_at (DATETIME)                      │
└────────────────────────────────────────────┘
```

#### فیلدهای اصلی:
| فیلد | نوع | توضیح |
|------|------|-------|
| `id` | PrimaryKey | شناسه |
| **`student_id`** ⭐ | ForeignKey | دانشجو |
| **`course_id`** ⭐ | ForeignKey | درسی که انتخاب کرده |
| **`semester`** ⭐ | CharField | ترم انتخاب (مثلاً "Spring 1403") |
| `selected_at` | DateTimeField | تاریخ انتخاب |
| **`is_confirmed`** ⭐ | BooleanField | آیا انتخاب تایید شده است؟ |
| `confirmed_at` | DateTimeField | تاریخ تایید |
| `notes` | TextField | یادداشت‌های دانشجو |
| `created_at` | DateTimeField | تاریخ ایجاد |
| `updated_at` | DateTimeField | تاریخ آخرین ویرایش |

#### محدودیت‌ها:
- **Unique Constraint:** `(student_id, course_id, semester)`

#### چرا ایجاد شد؟
دانشجویان برای هر ترم باید دروسی را **انتخاب کنند**. این انتخاب‌ها:
- باید اعتبارسنجی شوند (پیش‌نیازها و هم‌نیازها)
- قبل از تایید می‌تواند تغییر کند
- برای محاسبه بار تحصیلی استفاده می‌شود

#### کجا به کار می‌رود:
- ✅ فرآیند انتخاب درس
- ✅ اعتبارسنجی انتخاب (پیش‌نیازها)
- ✅ محاسبه بار تحصیلی
- ✅ برنامه‌ریزی کلاس‌ها
- ✅ نمایش درس‌های انتخاب‌شده و تایید نشده
- ✅ تولید برنامه دانشجو

---

### 10. جدول `students_schedule`
**نوع:** برنامه هفتگی دانشجو

#### ساختار:
```
┌──────────────────────────────────────────┐
│        students_schedule                 │
├──────────────────────────────────────────┤
│ id (PK)                                  │
│ student_id (FK) → accounts_user          │
│ course_id (FK) → courses_course          │
│ day_of_week (VARCHAR)                    │
│ start_time (TIME)                        │
│ end_time (TIME)                          │
│ location (VARCHAR)                       │
│ semester (VARCHAR)                       │
│ created_at (DATETIME)                    │
│ updated_at (DATETIME)                    │
└──────────────────────────────────────────┘
```

#### فیلدهای اصلی:
| فیلد | نوع | توضیح |
|------|------|-------|
| `id` | PrimaryKey | شناسه |
| **`student_id`** ⭐ | ForeignKey | دانشجو |
| **`course_id`** ⭐ | ForeignKey | درس |
| **`day_of_week`** ⭐ | CharField | روز هفته: sat, sun, mon, tue, wed, thu, fri |
| **`start_time`** ⭐ | TimeField | ساعت شروع |
| **`end_time`** ⭐ | TimeField | ساعت پایان |
| `location` | CharField | مکان کلاس (سالن/کلاس) |
| **`semester`** ⭐ | CharField | ترم |
| `created_at` | DateTimeField | تاریخ ایجاد |
| `updated_at` | DateTimeField | تاریخ آخرین ویرایش |

#### محدودیت‌ها:
- `start_time` باید کمتر از `end_time` باشد
- مدل یک **Property** `has_conflict` دارد که بررسی می‌کند آیا این کلاس با کلاس دیگری تداخل دارد

#### چرا ایجاد شد؟
از انتخاب دروس نمی‌تواند برنامه ایجاد شود، زیرا:
- زمان کلاس‌های مختلف متفاوت است
- ممکن است تداخل زمانی داشته باشند
- دانشجو می‌خواهد برنامه‌اش را ببیند

#### کجا به کار می‌رود:
- ✅ نمایش برنامه هفتگی دانشجو
- ✅ اعتبارسنجی برنامه (بدون تداخل زمانی)
- ✅ توصیه دروس بر اساس عدم تداخل
- ✅ نمایش نقشه گرافیکی برنامه
- ✅ اخطار تداخل‌های زمانی

---

## خلاصه ارتباطات و روابط

### نمودار ارتباطات (ERD)

```
                         accounts_user ⭐ (جدول اصلی کاربران)
                         │
                    ┌────┼────┐
                    │    │    │
                    ▼    ▼    ▼
        accounts_   stud  students_    courses_
        profile     ents  schedule   prerequisite
        (OneToOne) (FK)  (FK)       (FK)
         │          │     │          │
         │     ┌────┴─────┘     ┌────┴────┐
         │     │                 │         │
         ▼     ▼                 ▼         ▼
    courses_  students_      courses_  courses_
    degree    student        course    course
    chart     history        (both     (both
    │         (History of    sides)    sides)
    │         passed courses)
    ▼
courses_chart    courses_co
course           requisite
(Link)
```

### روابط کلیدی:
```
User (accounts_user)
├── Profile (1:1) → accounts_profile
│   └── major (FK) → courses_degreechart
├── StudentCourseHistory (1:N) → students_studentcoursehistory
│   └── course (FK) → courses_course
├── StudentSelection (1:N) → students_studentselection
│   └── course (FK) → courses_course
└── Schedule (1:N) → students_schedule
    └── course (FK) → courses_course

DegreeChart (courses_degreechart)
├── ChartCourse (1:N) → courses_chartcourse
│   └── course (FK) → courses_course
└── Profile (1:N) ← accounts_profile [reverse]

Course (courses_course)
├── Prerequisites (1:N) → courses_prerequisite
│   ├── course (FK) → courses_course [self]
│   └── prerequisite_course (FK) → courses_course [self]
├── CoRequisites (1:N) → courses_corequisite
│   ├── course (FK) → courses_course [self]
│   └── corequisite_course (FK) → courses_course [self]
├── ChartCourse (1:N) ← courses_chartcourse [reverse]
├── StudentCourseHistory (1:N) ← students_studentcoursehistory [reverse]
├── StudentSelection (1:N) ← students_studentselection [reverse]
└── Schedule (1:N) ← students_schedule [reverse]
```

---

## جداول Django پیش‌فرض (برای مرجع)

| نام جدول | توضیح |
|----------|-------|
| `auth_user` | کاربران Django پیش‌فرض (ما از `accounts_user` استفاده می‌کنیم) |
| `auth_group` | گروه‌های مجوز |
| `auth_permission` | تعریف مجوزها |
| `django_migrations` | تاریخچه تغییرات دیتابیس |
| `django_session` | سشن کاربران |
| `django_content_type` | نوع محتوای مدل‌ها |

---

## آمار و اطلاعات کلی

### تعداد جداول:
- **مدل‌های سفارشی:** 10 جدول
- **جداول Django پیش‌فرض:** 6 جدول (تقریبی)
- **جمع:** ~16 جدول

### اندازه تقریبی دیتابیس:
```
با 500 دانشجو:
- accounts_user: 500 سطر
- accounts_profile: 500 سطر
- courses_course: 100 سطر
- courses_degreechart: 5 سطر
- students_studentcoursehistory: 50,000 سطر (500 × 100)
- students_studentselection: 5,000 سطر (500 × 10)
- students_schedule: 5,000 سطر (500 × 10)
```

### نکات مهم:
- ✅ تمام تاریخ‌ها و زمان‌ها در منطقه زمانی تهران ذخیره می‌شوند
- ✅ پشتیبانی از اطلاعات فارسی (UTF-8)
- ✅ ارتباطات رابط کاسکادی (`CASCADE`) - حذف کاربر تمام رکوردهایش را حذف می‌کند
- ✅ استفاده از `Soft Delete` برای کاربران (`is_active = False`)
- ✅ ایندکس‌های خودکار روی کلیدهای خارجی

---

## استفاده عملی - مثال‌ها

### مثال 1: نمایش کارنامه دانشجو
```python
# کاربر را پیدا کن
user = User.objects.get(username='student1')

# تمام دروس گذرانده‌شده را بگیر
history = StudentCourseHistory.objects.filter(
    student=user
).select_related('course')

# برای نمایش:
# دوره، نمره، ترم، واحد
for record in history:
    print(f"{record.course.code}: {record.grade} ({record.semester})")
```

### مثال 2: توصیه دروس بعدی
```python
# دروس رشته دانشجو
degree = user.profile.major  # DegreeChart
chart_courses = ChartCourse.objects.filter(
    degree_chart=degree
).select_related('course')

# دروس گذرانده‌شده
passed_courses = StudentCourseHistory.objects.filter(
    student=user,
    is_passed=True
).values_list('course_id', flat=True)

# دروس قابل انتخاب = دروسی که:
# 1. بخشی از رشته هستند
# 2. پیش‌نیازی‌های آن‌ها گذرانده شده‌اند
# 3. هنوز انتخاب نشده‌اند
```

### مثال 3: اعتبارسنجی انتخاب درس
```python
course = Course.objects.get(code='CS201')

# پیش‌نیازی‌های درس
prerequisites = Prerequisite.objects.filter(
    course=course
).select_related('prerequisite_course')

for prereq in prerequisites:
    if not StudentCourseHistory.objects.filter(
        student=student,
        course=prereq.prerequisite_course,
        is_passed=True
    ).exists():
        return "شما پیش‌نیاز را گذرانده نیستید!"
```

---

## نتیجه‌گیری

این ساختار دیتابیس به‌طور کامل برای **سیستم مدیریت آموزشی** طراحی شده است و شامل:
- ✅ مدیریت کاربران با نقش‌های مختلف
- ✅ برنامه‌های درجه (رشته‌های تحصیلی)
- ✅ مدیریت دروس و پیش‌نیازی‌ها
- ✅ تاریخچه تحصیلی دانشجویان
- ✅ انتخاب درس و برنامه‌ریزی
- ✅ محاسبات آکادمیک (GPA، واحد، معدل)
