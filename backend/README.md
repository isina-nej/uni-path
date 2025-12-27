# Backend - Unipath

## Overview

Unipath Backend is a Django REST API for the university course selection system. It provides endpoints for:

- User authentication and authorization (Student, Admin, Professor, HOD)
- Curriculum (Chart) management
- Course prerequisites and co-requisites
- Student progress tracking
- Recommendation engine
- Grade management

## Tech Stack

- **Framework:** Django 4.2
- **API:** Django REST Framework
- **Database:** PostgreSQL
- **Python:** 3.10+

## Setup Instructions

### 1. Create Virtual Environment

```bash
python -m venv venv
```

### 2. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost:5432/unipath
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
```

### 5. Database Migration

```bash
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```

Server will be available at `http://localhost:8000/`

## Project Structure

```
backend/
├── unipath/              # Project settings
│   ├── settings.py      # Django settings
│   ├── urls.py          # URL configuration
│   └── wsgi.py          # WSGI configuration
├── students/            # Student app
│   ├── models.py        # Student models
│   ├── views.py         # Student views
│   └── urls.py          # Student URLs
├── courses/             # Courses app
│   ├── models.py        # Course models
│   ├── views.py         # Course views
│   └── urls.py          # Course URLs
├── manage.py            # Django management script
└── requirements.txt     # Python dependencies
```

## API Endpoints

- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `GET /api/courses/` - List all courses
- `GET /api/chart/<major_id>/` - Get curriculum chart
- `GET /api/student/progress/` - Get student progress
- `GET /api/recommendations/` - Get course recommendations

## Admin Panel

Access Django admin at `http://localhost:8000/admin/`

## Testing

```bash
python manage.py test
```

## Deployment

See deployment documentation for production setup with Gunicorn and Nginx.
