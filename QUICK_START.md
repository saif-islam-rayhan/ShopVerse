# Quick Start Guide

Get the ShopVerse authentication system up and running in 10 minutes!

## Prerequisites

Before starting, ensure you have:
- Node.js 16+ installed
- Python 3.8+ installed
- MongoDB running locally or MongoDB Atlas account
- Google OAuth credentials (see GOOGLE_OAUTH_SETUP.md)

## 1. Backend Setup (5 minutes)

```bash
# Navigate to backend folder
cd backend

# Copy environment template
cp .env.example .env

# Edit .env with your settings
nano .env
```

Update these in `.env`:
```env
MONGODB_URL=mongodb://localhost:27017
SECRET_KEY=your-super-secret-key-here
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start backend server
python -m uvicorn app.main:app --reload --port 5000
```

✅ Backend running at `http://localhost:8000`

## 2. Frontend Setup (5 minutes)

```bash
# Navigate to frontend folder
cd ../frontend

# Copy environment template
cp .env.example .env

# Edit .env with your Google Client ID
nano .env
```

Update `.env`:
```env
VITE_GOOGLE_CLIENT_ID=your-google-client-id
```

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

✅ Frontend running at `http://localhost:5173`

## 3. Test the Application

### Open in Browser
```
http://localhost:5173
```

### Create Account
1. Click "Create one here" link
2. Fill in email, username, and password
3. Password must have: 8+ chars, uppercase, lowercase, digit
4. Click "Create Account"

### Login
1. Go to login page
2. Enter email and password
3. Click "Sign In"
4. You're in! View dashboard with your profile

### Try Google Login
1. Go to login page
2. Click "Sign in with Google"
3. Choose your Google account
4. You're logged in!

## Features Demo

### API Endpoints (with curl)

**Register:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123",
    "username": "testuser"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123"
  }'
```

**Get Current User (protected):**
```bash
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

## Automatic Features

✅ **Token Validation**
- Tokens auto-validate on every request
- Invalid tokens redirect to login
- Tokens stored securely in localStorage

✅ **CORS Handling**
- Frontend can communicate with backend
- Google OAuth properly configured
- No security issues in development

✅ **Database**
- User data automatically stored in MongoDB
- Unique email constraint enforced
- Passwords securely hashed

## Folder Structure Created

```
ShopVerse/
├── backend/
│   ├── app/
│   │   ├── config/      ← Database & settings
│   │   ├── models/      ← User data model
│   │   ├── schemas/     ← Request/response validation
│   │   ├── routes/      ← API endpoints
│   │   ├── utils/       ← JWT, password, validators
│   │   └── middleware/  ← Auth protection
│   └── main.py          ← FastAPI app
└── frontend/
    ├── src/
    │   ├── context/     ← Auth state management
    │   ├── pages/       ← Login, Register, Dashboard
    │   ├── services/    ← API calls
    │   ├── components/  ← Protected routes
    │   └── styles/      ← CSS styling
    └── App.jsx          ← Main component
```

## Troubleshooting

### "Cannot reach localhost:8000"
- Make sure backend is running: `python -m uvicorn app.main:app --reload`
- Check if port 8000 is available

### "MongoDB not found"
- Start MongoDB: `mongod`
- Or update `MONGODB_URL` to use MongoDB Atlas cloud

### "Google login not working"
- Check Google Client ID is correct in both `.env` files
- Verify `http://localhost:5173` is in Google Console authorized origins
- See GOOGLE_OAUTH_SETUP.md for detailed setup

### "Invalid password" during login
- Password must have: 8+ characters, 1 uppercase, 1 lowercase, 1 digit
- Example: `MyPassword123`

### Token expiration redirect
- This is normal behavior - re-login to get a new token
- Tokens expire after 30 minutes by default

## Next Steps

1. **Customize Styling** - Edit CSS files in `frontend/src/styles/`
2. **Add More Fields** - Extend User model in `backend/app/models/user.py`
3. **Implement Password Reset** - Add forgot password flow
4. **Add Email Verification** - Send confirmation emails
5. **Deploy to Production** - Follow deployment guides

## API Documentation

After starting backend, view interactive API docs:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Database Inspection

Access MongoDB directly:
```bash
# If using local MongoDB
mongosh

# Inside mongosh
use shopverse_db
db.users.find()
```

## Questions?

- Check README.md for comprehensive documentation
- See code comments for implementation details
- Review security features section for best practices

Happy coding! 🚀
