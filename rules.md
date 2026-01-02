# قوانین پروژه UniPath

## قوانین کدنویسی

### Frontend (Flutter)
- استفاده از Provider برای State Management
- نام‌گذاری Widgets با camelCase
- جداسازی UI، Business Logic و Models
- استفاده از GetIt برای Dependency Injection

### Backend (Django)
- استفاده از Django REST Framework
- PEP 8 استاندارد Python
- نام‌گذاری Models به صورت singular
- استفاده از Serializers برای تبدیل

## قوانین Git

- Branch Naming: `feature/`, `bugfix/`, `hotfix/`
- Commit Message: انگلیسی، فعل در حال
- Pull Request: توضیح تغییرات و لینک Issue

## قوانین Database

- استفاده از PostgreSQL
- هر جدول برای یک Entity
- استفاده از Foreign Key برای Relationships
- Index بر روی جداول بزرگ

## قوانین API

- Versioning: `/api/v1/`
- HTTP Methods: GET, POST, PUT, DELETE
- Response Format: JSON
- Error Handling: HTTP Status Codes

## قوانین امنیتی

- HTTPS برای تمام Requests
- Token Expiration: 24 ساعت
- Rate Limiting برای API
- Validation تمام Inputs
- CORS Configuration

## قوانین توسعه

- Testing: حداقل 70% Code Coverage
- Documentation: Docstrings برای تمام Functions
- Code Review: الزامی قبل از Merge
- Performance: API Response Time < 2 Seconds
