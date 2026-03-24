# Architecture & Design Decisions

This document explains the architectural choices and design patterns used in ShopVerse.

## Overview

ShopVerse uses a **clean architecture** pattern with clear separation of concerns:

```
Client Layer (React)
        ↓
API Client Layer (Axios)
        ↓
FastAPI Backend
        ↓
Business Logic (Routes, Services)
        ↓
Data Access Layer (MongoDB)
```

## Backend Architecture

### Layer Structure

**1. Routes Layer** (`app/routes/`)
- Handles HTTP requests
- Validates input with Pydantic schemas
- Returns JSON responses
- Applies middleware/decorators

**2. Models Layer** (`app/models/`)
- Defines database schema
- Uses PyMongo conventions
- Handles ObjectId conversions
- Validates data types

**3. Schemas Layer** (`app/schemas/`)
- Request/response validation
- Type hints with Pydantic
- Automatic documentation
- JSON schema generation

**4. Utils Layer** (`app/utils/`)
- Reusable functions
- JWT token generation/verification
- Password hashing and verification
- Input validation

**5. Middleware Layer** (`app/middleware/`)
- JWT token extraction
- User authentication
- Error handling
- Request/response intercepting

**6. Config Layer** (`app/config/`)
- Environment variables
- Database connection
- Settings management
- Initialization logic

### Technology Choices

**FastAPI** (Framework)
- ✅ Async support for concurrent requests
- ✅ Automatic OpenAPI documentation
- ✅ Built-in data validation with Pydantic
- ✅ High performance (comparable to NodeJS)
- ✅ Easy to learn and use

**Motor** (MongoDB Async Driver)
- ✅ Asynchronous MongoDB operations
- ✅ Non-blocking database calls
- ✅ Better performance for I/O
- ✅ Compatible with FastAPI

**PyJWT** (JWT Implementation)
- ✅ Standard JWT library
- ✅ Supports HS256 signing
- ✅ Easy token verification
- ✅ Configurable expiration

**Bcrypt** (Password Hashing)
- ✅ Industry standard algorithm
- ✅ Slow-by-design (prevents brute force)
- ✅ Salt generation included
- ✅ Proven secure for decades

## Frontend Architecture

### Component Structure

**Pages** (`src/pages/`)
- Full-page components
- Route-level views
- Handle complex logic
- Examples: LoginPage, RegisterPage

**Components** (`src/components/`)
- Reusable UI pieces
- Stateless or minimal state
- Examples: ProtectedRoute, Button, Form

**Context** (`src/context/`)
- Global state management
- Authentication state
- User data sharing
- Avoids prop drilling

**Services** (`src/services/`)
- API communication
- Axios instance setup
- API function wrappers
- Request/response handling

**Styles** (`src/styles/`)
- CSS files
- Component-specific styles
- Global styles
- Responsive design

### Technology Choices

**React 18**
- ✅ Latest features and improvements
- ✅ Concurrent rendering
- ✅ Automatic batching
- ✅ Strict mode for development

**Vite**
- ✅ Lightning fast development
- ✅ Native ES modules
- ✅ Instant HMR (Hot Module Reload)
- ✅ Optimized production build

**React Router v6**
- ✅ Client-side routing
- ✅ Protected routes
- ✅ Nested routing support
- ✅ Modern hook-based API

**Context API**
- ✅ No additional dependencies
- ✅ Perfect for auth state
- ✅ Performance with custom hooks
- ✅ Suitable for small to medium apps

**Axios**
- ✅ Request/response interceptors
- ✅ Automatic JSON serialization
- ✅ Request cancellation support
- ✅ More features than fetch

## Security Architecture

### Password Security
```
User Password
    ↓
Validation (min 8 chars, uppercase, lowercase, digit)
    ↓
Bcrypt Hashing (12 rounds)
    ↓
Store in Database
```

### Authentication Flow
```
POST /auth/login
    ↓
Find user by email
    ↓
Verify password vs hash
    ↓
Create JWT token: {sub: user_id, exp: now + 30min}
    ↓
Sign with SECRET_KEY
    ↓
Return token to client
```

### Protected Route Flow
```
GET /api/v1/auth/me
    ↓
Extract token from Authorization header
    ↓
Verify JWT signature with SECRET_KEY
    ↓
Check token expiration
    ↓
Extract user_id from token
    ↓
Return user data
```

## Data Flow

### Registration
```
Frontend (RegisterPage)
    ↓
User fills form, clicks "Register"
    ↓
Frontend validates password strength
    ↓
POST /auth/register {email, password, username}
    ↓
Backend validates input
    ↓
Backend checks email uniqueness
    ↓
Backend hashes password
    ↓
Backend inserts user into MongoDB
    ↓
Backend creates JWT token
    ↓
Backend returns {user, token}
    ↓
Frontend stores token in localStorage
    ↓
Frontend redirects to /dashboard
```

### Login
```
Frontend (LoginPage)
    ↓
User enters email/password
    ↓
POST /auth/login {email, password}
    ↓
Backend finds user by email
    ↓
Backend verifies password
    ↓
Backend creates JWT token
    ↓
Backend returns {user, token}
    ↓
Frontend stores token
    ↓
Frontend calls /auth/me to get user
    ↓
Frontend updates auth context
    ↓
Frontend navigates to /dashboard
```

### Protected Route Access
```
Frontend navigates to /dashboard
    ↓
ProtectedRoute component checks isAuthenticated
    ↓
If false, redirect to /login
    ↓
If true, render DashboardPage
    ↓
DashboardPage uses useAuth hook
    ↓
Displays user information from context
```

## Database Schema

### Users Collection
```javascript
{
  _id: ObjectId,                    // Auto-generated
  email: String,                    // Unique index
  username: String,
  password: String,                 // Bcrypt hash
  auth_provider: String,            // "local" or "google"
  provider_id: String,              // Google ID if OAuth
  created_at: ISODate,              // Auto-set
  updated_at: ISODate,              // Auto-set
  is_active: Boolean                // Default: true
}
```

**Indexes:**
- `email`: Unique index (prevents duplicate registrations)

**Future Indexes:**
- `provider_id`: For OAuth lookups
- `created_at`: For user analytics

## Error Handling

### Backend Errors
```
HTTP Exception
    ↓
Status Code + Detail Message
    ↓
JSON Response to Frontend
```

Examples:
- 400: Bad Request (invalid input)
- 401: Unauthorized (invalid credentials)
- 403: Forbidden (inactive user)
- 404: Not Found (user doesn't exist)
- 500: Server Error (unexpected error)

### Frontend Errors
```
API Error
    ↓
Caught in catch block
    ↓
Display error message to user
    ↓
If 401: Redirect to login
```

## Scalability Considerations

### Current State
- ✅ Handles 1,000-5,000 concurrent users
- ✅ Single MongoDB instance
- ✅ Single backend server

### For 10,000+ Users

1. **Database**
   - Use MongoDB Atlas (cloud)
   - Enable replication
   - Add read replicas

2. **Backend**
   - Deploy multiple FastAPI instances
   - Use load balancer (Nginx, Docker Swarm)
   - Add caching layer (Redis)

3. **Frontend**
   - CDN for static files
   - Optimize bundle size
   - Code splitting

### Future Enhancements

1. **Refresh Tokens**
   - Implement token refresh endpoint
   - Store refresh tokens in Redis
   - Auto-refresh expiring tokens

2. **Email Verification**
   - Send verification email
   - Mark user as verified
   - Resend verification link

3. **Password Reset**
   - Generate reset token
   - Send reset email
   - Validate token on reset

4. **Two-Factor Authentication**
   - TOTP support
   - SMS verification
   - Backup codes

5. **Rate Limiting**
   - Login attempts limiting
   - API rate limiting
   - DDoS protection

## Testing Strategy

### Unit Tests (Backend)
- Test JWT functions
- Test password utilities
- Test validators

### Integration Tests (Backend)
- Test auth endpoints
- Test database operations
- Test CORS

### E2E Tests (Frontend)
- Test registration flow
- Test login flow
- Test protected routes
- Test Google OAuth

### Manual Testing
- Test with different browsers
- Test on mobile devices
- Test error scenarios
- Test network timeouts

## Deployment Strategy

### Development
- Local MongoDB
 - Local backend on port 5000
- Local frontend on port 5173
- Hot reloading enabled

### Production
- MongoDB Atlas (cloud)
- Multiple backend instances
- CDN for frontend
- HTTPS enforcement
- Environment-specific configs

## References

- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)
- [API Design Best Practices](https://restfulapi.net/)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
