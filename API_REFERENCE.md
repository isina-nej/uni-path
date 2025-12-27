# Backend API Quick Reference

## Base URL
```
http://localhost:8000/api
```

## Authentication
All requests (except auth endpoints) must include:
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

---

## 📝 Endpoints

### 1. User Registration
```http
POST /auth/register
Content-Type: application/json

{
  "username": "student123",
  "email": "student@university.edu",
  "password": "SecurePass123!",
  "password2": "SecurePass123!",
  "first_name": "علی",
  "last_name": "محمدی",
  "role": "student"
}
```

**Success Response (201):**
```json
{
  "id": 1,
  "username": "student123",
  "email": "student@university.edu",
  "first_name": "علی",
  "last_name": "محمدی",
  "role": "student"
}
```

**Error Responses:**
- `400 Bad Request` - Validation errors
  - `{"username": ["This field may not be blank."]}` 
  - `{"email": ["این ایمیل قبلاً استفاده شده است"]}`
  - `{"password": ["رمز عبور ضعیف است"]}`

---

### 2. Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "student@university.edu",
  "password": "SecurePass123!"
}
```

**Success Response (200):**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "student123",
    "email": "student@university.edu",
    "first_name": "علی",
    "last_name": "محمدی",
    "role": "student"
  }
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid credentials
  ```json
  {"detail": "ایمیل یا رمز عبور نادرست است"}
  ```
- `400 Bad Request` - Missing fields

---

### 3. Refresh Token
```http
POST /auth/refresh
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Success Response (200):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid or expired refresh token

---

### 4. Logout
```http
POST /auth/logout
Authorization: Bearer <access_token>
Content-Type: application/json

{}
```

**Success Response (200):**
```json
{
  "message": "خروج موفق"
}
```

---

### 5. Change Password
```http
POST /user/change-password
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "old_password": "OldPass123!",
  "new_password": "NewPass456!",
  "new_password2": "NewPass456!"
}
```

**Success Response (200):**
```json
{
  "message": "رمز عبور تغییر کرد"
}
```

**Error Responses:**
- `400 Bad Request` - Old password is wrong
- `401 Unauthorized` - Not authenticated

---

### 6. Get User Profile
```http
GET /user/profile
Authorization: Bearer <access_token>
```

**Success Response (200):**
```json
{
  "id": 1,
  "user": {
    "id": 1,
    "username": "student123",
    "email": "student@university.edu",
    "first_name": "علی",
    "last_name": "محمدی",
    "role": "student",
    "is_active": true
  },
  "student_number": "9812345",
  "phone": "09121234567",
  "bio": "علاقه‌مند به برنامه‌نویسی",
  "avatar": "https://...",
  "major": "مهندسی نرم‌افزار",
  "department": "علوم کامپیوتر"
}
```

**Error Responses:**
- `401 Unauthorized` - Not authenticated
- `404 Not Found` - Profile not found

---

### 7. Update User Profile
```http
PUT /user/profile
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "first_name": "احمد",
  "last_name": "علوی",
  "phone": "09129876543",
  "bio": "متخصص در برنامه‌نویسی وب",
  "student_number": "9812346",
  "major": "مهندسی نرم‌افزار",
  "department": "فن‌آوری اطلاعات"
}
```

**Success Response (200):**
```json
{
  "id": 1,
  "user": {...},
  "student_number": "9812346",
  "phone": "09129876543",
  "bio": "متخصص در برنامه‌نویسی وب",
  "avatar": "https://...",
  "major": "مهندسی نرم‌افزار",
  "department": "فن‌آوری اطلاعات"
}
```

**Error Responses:**
- `400 Bad Request` - Validation errors
- `401 Unauthorized` - Not authenticated

---

## 🔐 User Roles

| Role | Permissions |
|------|-------------|
| `student` | View own profile, courses, schedule |
| `professor` | Enter grades, view student grades |
| `admin` | Full system access |
| `hod` | Head of Department access |

---

## 🔑 JWT Token Structure

**Access Token (5 minutes):**
```json
{
  "user_id": 1,
  "username": "student123",
  "email": "student@university.edu",
  "role": "student",
  "first_name": "علی",
  "last_name": "محمدی",
  "exp": 1703076845,
  "iat": 1703076545
}
```

**Refresh Token (24 hours):**
- Longer expiry for token refresh
- Never include in API requests
- Store securely on client

---

## 📊 Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request (validation error) |
| 401 | Unauthorized (not authenticated) |
| 403 | Forbidden (no permission) |
| 404 | Not Found |
| 500 | Server Error |

---

## 🧪 Testing with cURL

### 1. Register
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test123",
    "email": "test@university.edu",
    "password": "TestPass123!",
    "password2": "TestPass123!",
    "role": "student"
  }'
```

### 2. Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@university.edu",
    "password": "TestPass123!"
  }'
```

### 3. Get Profile (with token)
```bash
curl -X GET http://localhost:8000/api/user/profile \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 4. Update Profile
```bash
curl -X PUT http://localhost:8000/api/user/profile \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "09121234567",
    "bio": "Updated bio"
  }'
```

---

## 🔄 Token Refresh Flow

1. **Initial Login**: Get `access` and `refresh` tokens
2. **Use Access Token**: For all API requests (expires in 5 minutes)
3. **Token Expires**: Receive 401 Unauthorized
4. **Refresh Token**: Use `refresh` token to get new `access` token
5. **Continue**: Use new `access` token for requests

```
Login → Get Tokens → Use Access Token → Expires
                                           ↓
                                     Refresh Token
                                           ↓
                                      Get New Access
                                           ↓
                                      Continue
```

---

## 💡 Error Handling

### Common Errors

**Invalid Email Format:**
```json
{
  "email": ["ایمیل نامعتبر است"]
}
```

**Weak Password:**
```json
{
  "password": ["رمز عبور ضعیف است"]
}
```

**Duplicate Email:**
```json
{
  "email": ["این ایمیل قبلاً استفاده شده است"]
}
```

**Unauthorized:**
```json
{
  "detail": "ایمیل یا رمز عبور نادرست است"
}
```

---

## 📱 Frontend Integration

See [Frontend Auth Integration Guide](PHASE_7_COMPLETE.md) for Flutter integration details.

---

## 🚀 Deployment

For production deployment, update:
1. Base URL to HTTPS
2. CORS allowed origins
3. Database credentials
4. Secret key
5. Email backend

See `backend/unipath/settings.py` for configuration.

---

## 📞 Support

For issues or questions:
1. Check error message carefully
2. Verify token is valid (not expired)
3. Check request format (JSON)
4. Review user role permissions
5. Check server logs

---

**Last Updated:** 2024-12-19  
**Version:** 1.0
