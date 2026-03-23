# API Documentation

Complete reference for all ShopVerse authentication API endpoints.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

All endpoints that require authentication use Bearer tokens in the Authorization header:

```
Authorization: Bearer YOUR_JWT_TOKEN
```

## Endpoints

### 1. Register User

Create a new user account with email and password.

```
POST /auth/register
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123",
  "username": "john_doe"
}
```

**Request Headers:**
```
Content-Type: application/json
```

**Success Response (201):**
```json
{
  "user": {
    "_id": "507f1f77bcf86cd799439011",
    "email": "user@example.com",
    "username": "john_doe",
    "created_at": "2024-01-01T12:00:00",
    "auth_provider": "local"
  },
  "token": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 1800
  }
}
```

**Error Response (400):**
```json
{
  "detail": "Email already registered"
}
```

**Validation Rules:**
- Email must be valid format
- Password must be 8+ characters
- Password must contain uppercase, lowercase, and digit
- Username must be 3-50 characters

---

### 2. Login User

Authenticate user with email and password.

```
POST /auth/login
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Success Response (200):**
```json
{
  "user": {
    "_id": "507f1f77bcf86cd799439011",
    "email": "user@example.com",
    "username": "john_doe",
    "created_at": "2024-01-01T12:00:00",
    "auth_provider": "local"
  },
  "token": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 1800
  }
}
```

**Error Response (401):**
```json
{
  "detail": "Invalid email or password"
}
```

---

### 3. Google OAuth Login

Authenticate using Google OAuth token.

```
POST /auth/google
```

**Request Body:**
```json
{
  "token": "google_oauth_token_here"
}
```

**Success Response (200):**
```json
{
  "user": {
    "_id": "507f1f77bcf86cd799439012",
    "email": "user@gmail.com",
    "username": "john_doe",
    "created_at": "2024-01-01T12:00:00",
    "auth_provider": "google"
  },
  "token": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 1800
  }
}
```

**Error Response (401):**
```json
{
  "detail": "Invalid Google token"
}
```

**Note:** If email already exists, the Google account will be linked to the existing user.

---

### 4. Get Current User

Retrieve current authenticated user information.

```
GET /auth/me
```

**Request Headers:**
```
Authorization: Bearer YOUR_JWT_TOKEN
```

**Success Response (200):**
```json
{
  "_id": "507f1f77bcf86cd799439011",
  "email": "user@example.com",
  "username": "john_doe",
  "created_at": "2024-01-01T12:00:00",
  "auth_provider": "local"
}
```

**Error Response (401):**
```json
{
  "detail": "Invalid or expired token"
}
```

**Error Response (404):**
```json
{
  "detail": "User not found"
}
```

---

## HTTP Status Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Successful request |
| 201 | Created | User successfully registered |
| 400 | Bad Request | Invalid input data |
| 401 | Unauthorized | Missing or invalid token |
| 403 | Forbidden | User account inactive |
| 404 | Not Found | Resource not found |
| 500 | Server Error | Internal server error |

---

## Example cURL Requests

### Register
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123",
    "username": "testuser"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123"
  }'
```

### Get Current User
```bash
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

## Token Format

JWT tokens contain three parts separated by dots:
```
header.payload.signature
```

**Payload decoded example:**
```json
{
  "sub": "507f1f77bcf86cd799439011",
  "exp": 1234567890,
  "iat": 1234567800
}
```

- `sub`: User ID
- `exp`: Expiration timestamp
- `iat`: Issued at timestamp

---

## Rate Limiting

Currently, no rate limiting is implemented. In production, add:
- 10 requests/minute per IP for `/auth/login`
- 5 requests/minute per IP for `/auth/register`
- 100 requests/minute per user for authenticated endpoints

---

## CORS Headers

Requests from allowed origins receive CORS headers:

```
Access-Control-Allow-Origin: http://localhost:5173
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
```

---

## Token Refresh

Tokens expire after 30 minutes. After expiration:
1. Frontend attempts API call with expired token
2. Backend returns 401 Unauthorized
3. Frontend redirects to login page
4. User must login again

**To implement refresh tokens** (future enhancement):
- Add `refresh_token` endpoint
- Store refresh tokens in database or Redis
- Allow token refresh without re-login

---

## Testing with Postman

1. Import these URLs into Postman
2. Set up environment variables:
   - `base_url`: http://localhost:8000/api/v1
   - `token`: Your JWT token
3. Create requests for each endpoint
4. Use "Tests" tab to automatically set token after login

---

## Common Errors

### Invalid Credentials
```json
{
  "detail": "Invalid email or password"
}
```
**Solution:** Verify email and password are correct

### Token Expired
```json
{
  "detail": "Invalid or expired token"
}
```
**Solution:** Login again to get a new token

### Email Already Registered
```json
{
  "detail": "Email already registered"
}
```
**Solution:** Use a different email or login with existing account

### Weak Password
```json
{
  "detail": "Password must contain at least one uppercase letter"
}
```
**Solution:** Create a stronger password with uppercase, lowercase, and digits

---

## References

- [OpenAPI/Swagger Docs](http://localhost:8000/docs)
- [JSON Web Tokens](https://jwt.io/)
- [Bearer Token Usage](https://tools.ietf.org/html/rfc6750)
