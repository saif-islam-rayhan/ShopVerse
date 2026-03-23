# ShopVerse - Full Stack E-commerce Application

A complete authentication system for a full-stack e-commerce application with FastAPI backend, React frontend, and MongoDB database.

## Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: MongoDB with Motor (async driver)
- **Authentication**: JWT + bcrypt
- **Python Version**: 3.8+

### Frontend
- **Framework**: React 18 with Vite
- **State Management**: React Context API
- **Routing**: React Router v6
- **API Client**: Axios
- **OAuth**: Google OAuth via @react-oauth/google

## Project Structure

```
ShopVerse/
├── backend/
│   ├── app/
│   │   ├── config/
│   │   │   ├── __init__.py
│   │   │   ├── settings.py         # Configuration and environment variables
│   │   │   └── database.py         # MongoDB connection setup
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── user.py             # User database model
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── auth.py             # Pydantic request/response schemas
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   └── auth.py             # Authentication endpoints
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── jwt.py              # JWT token utilities
│   │   │   ├── password.py         # Password hashing utilities
│   │   │   └── validators.py       # Input validators
│   │   ├── middleware/
│   │   │   ├── __init__.py
│   │   │   └── jwt.py              # JWT verification middleware
│   │   ├── main.py                 # FastAPI app initialization
│   │   └── __init__.py
│   ├── requirements.txt            # Python dependencies
│   ├── .env.example                # Environment variables template
│   └── .gitignore
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── ProtectedRoute.jsx  # Route protection wrapper
│   │   ├── context/
│   │   │   └── AuthContext.jsx     # Auth state management
│   │   ├── pages/
│   │   │   ├── LoginPage.jsx
│   │   │   ├── RegisterPage.jsx
│   │   │   └── DashboardPage.jsx
│   │   ├── services/
│   │   │   ├── apiClient.js        # Axios instance with interceptors
│   │   │   └── authService.js      # API integration functions
│   │   ├── config/
│   │   │   └── api.js              # API configuration
│   │   ├── styles/
│   │   │   ├── index.css           # Global styles
│   │   │   ├── auth.css            # Auth pages styles
│   │   │   └── dashboard.css       # Dashboard styles
│   │   ├── App.jsx                 # Main app component
│   │   └── main.jsx                # React entry point
│   ├── package.json
│   ├── vite.config.js              # Vite configuration
│   ├── index.html                  # HTML entry point
│   ├── .env.example                # Environment variables template
│   └── .gitignore
└── README.md                       # This file
```

## Installation & Setup

### Prerequisites
- Node.js 16+
- Python 3.8+
- MongoDB (local or cloud)
- Google OAuth credentials

### Backend Setup

1. **Create `.env` file in backend folder:**
```bash
cd backend
cp .env.example .env
```

2. **Edit `.env` with your MongoDB URL and Google credentials:**
```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=shopverse_db
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret
FRONTEND_URL=http://localhost:5173
```

3. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. **Install dependencies:**
```bash
pip install -r requirements.txt
```

5. **Start MongoDB:**
```bash
# Local MongoDB
mongod

# Or use MongoDB Atlas (cloud) - update MONGODB_URL in .env
```

6. **Run backend server:**
```bash
python -m uvicorn app.main:app --reload
```

Backend will run at `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Frontend Setup

1. **Create `.env` file in frontend folder:**
```bash
cd frontend
cp .env.example .env
```

2. **Edit `.env` with Google Client ID:**
```env
VITE_API_URL=http://localhost:8000/api/v1
VITE_GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
```

3. **Install dependencies:**
```bash
npm install
```

4. **Start development server:**
```bash
npm run dev
```

Frontend will run at `http://localhost:5173`

## Features

### Authentication Features

1. **Email/Password Registration**
   - Email validation
   - Strong password requirements (8+ chars, uppercase, lowercase, digit)
   - Secure bcrypt hashing
   - Unique email constraint

2. **Email/Password Login**
   - JWT token generation
   - Automatic token storage
   - Auto-logout on token expiration

3. **Google OAuth Login**
   - One-click Google authentication
   - Automatic user creation
   - Account linking if email exists

4. **Protected Routes**
   - React Router protection
   - JWT token verification
   - Automatic redirect to login
   - Token refresh handling

### API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/auth/register` | Register new user | No |
| POST | `/api/v1/auth/login` | Login with email/password | No |
| POST | `/api/v1/auth/google` | Google OAuth login | No |
| GET | `/api/v1/auth/me` | Get current user info | Yes |

## Google OAuth Setup

### 1. Create Google OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Google+ API
4. Create OAuth 2.0 Client ID:
   - Application type: Web application
   - Authorized origins: `http://localhost:5173`
   - Authorized redirect URIs: `http://localhost:8000/api/v1/auth/google/callback`

### 2. Add Credentials to `.env` Files

**Backend (.env):**
```env
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
```

**Frontend (.env):**
```env
VITE_GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
```

### 3. Update production URLs when deploying

## API Response Examples

### Successful Registration/Login
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

### Error Response
```json
{
  "detail": "Invalid email or password",
  "status_code": 401
}
```

## Security Features

1. **Password Security**
   - Bcrypt hashing with 12 salt rounds
   - Strong password validation
   - Never stored in plain text

2. **JWT Security**
   - HS256 algorithm
   - Configurable expiration time
   - Token verified on every protected request

3. **API Security**
   - CORS configured for frontend only
   - Bearer token authentication
   - Request validation with Pydantic

4. **Data Protection**
   - MongoDB unique indexes on email
   - No sensitive data in JWT payload
   - Secure token storage in localStorage

## Usage Examples

### Register New User
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123",
    "username": "john_doe"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123"
  }'
```

### Get Current User
```bash
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Frontend Usage

### Using Auth Context
```jsx
import { useAuth } from './context/AuthContext';

export const MyComponent = () => {
  const { user, isAuthenticated, logout } = useAuth();
  
  if (!isAuthenticated) {
    return <div>Please login</div>;
  }
  
  return (
    <div>
      <h1>Welcome, {user.username}!</h1>
      <button onClick={logout}>Logout</button>
    </div>
  );
};
```

### Calling API
```jsx
import { loginUser } from './services/authService';
import { useAuth } from './context/AuthContext';

export const LoginForm = () => {
  const { storeAuth } = useAuth();
  
  const handleLogin = async () => {
    const authResponse = await loginUser('user@example.com', 'password');
    storeAuth(authResponse);
  };
  
  return <button onClick={handleLogin}>Login</button>;
};
```

## Environment Variables

### Backend (.env)
- `MONGODB_URL` - MongoDB connection string
- `DATABASE_NAME` - Database name
- `SECRET_KEY` - JWT signing secret (change in production!)
- `ALGORITHM` - JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time
- `GOOGLE_CLIENT_ID` - Google OAuth Client ID
- `GOOGLE_CLIENT_SECRET` - Google OAuth Client Secret
- `FRONTEND_URL` - Frontend URL for CORS

### Frontend (.env)
- `VITE_API_URL` - Backend API base URL
- `VITE_GOOGLE_CLIENT_ID` - Google OAuth Client ID

## Production Checklist

- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Update MongoDB to use MongoDB Atlas
- [ ] Update CORS origins to production domain
- [ ] Update Google OAuth redirect URIs
- [ ] Enable HTTPS
- [ ] Set secure cookie attributes
- [ ] Add rate limiting
- [ ] Set up error logging
- [ ] Add email verification
- [ ] Implement password reset
- [ ] Add refresh token mechanism
- [ ] Enable request signing/verification

## Troubleshooting

### MongoDB Connection Error
- Ensure MongoDB is running: `mongod`
- Check connection string in `.env`
- Verify MongoDB credentials if using remote

### CORS Error
- Check frontend URL in backend `.env` CORS settings
- Ensure credentials are sent in requests

### Google OAuth Error
- Verify Client ID and Secret in `.env`
- Check authorized origins/redirect URIs
- Ensure token endpoint is configured

### JWT Token Invalid
- Check `SECRET_KEY` matches between issues
- Verify ALGORITHM setting
- Check token expiration time

## Next Steps

1. Add email verification
2. Implement password reset flow
3. Add refresh token mechanism
4. Implement user profile management
5. Add payment integration
6. Build product catalog
7. Implement shopping cart
8. Add order management

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [JWT.io](https://jwt.io/)
- [Google OAuth Documentation](https://developers.google.com/identity/protocols/oauth2)

## License

MIT License - feel free to use for your projects!
