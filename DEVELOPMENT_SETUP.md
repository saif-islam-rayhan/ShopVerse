# Development Setup

Complete guide for setting up the development environment.

## System Requirements

- **OS**: Windows, macOS, or Linux
- **Node.js**: v16+ ([Download](https://nodejs.org/))
- **Python**: v3.8+ ([Download](https://www.python.org/))
- **MongoDB**: Local or Atlas account ([Download](https://www.mongodb.com/try/download/community) or [Atlas](https://www.mongodb.com/cloud/atlas))
- **Git**: ([Download](https://git-scm.com/))

## 1. Clone Repository

```bash
git clone https://github.com/your-username/ShopVerse.git
cd ShopVerse
```

## 2. Backend Setup

### macOS / Linux

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Copy environment template
cp .env.example .env

# Edit .env file
nano .env

# Install dependencies
pip install -r requirements.txt

# Start MongoDB (in another terminal)
mongod

# Run backend server
python -m uvicorn app.main:app --reload
```

### Windows (PowerShell)

```powershell
cd backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Copy environment template
Copy-Item .env.example -Destination .env

# Edit .env file
notepad .env

# Install dependencies
pip install -r requirements.txt

# Start MongoDB (if installed locally)
mongod

# Run backend server
python -m uvicorn app.main:app --reload
```

## 3. Frontend Setup

### macOS / Linux / Windows

```bash
cd frontend

# Install dependencies
npm install

# Copy environment template
cp .env.example .env

# Edit .env file
nano .env  # or code .env

# Start development server
npm run dev
```

## 4. Verify Installation

### Backend
- Open http://localhost:8000
- Should see: `{"message": "Welcome to ShopVerse API"}`
- API Docs: http://localhost:8000/docs

### Frontend
- Open http://localhost:5173
- Should see login page with "Create one here" link

### Database
```bash
# macOS / Linux
mongosh

# Windows
mongosh

# In mongosh shell
use shopverse_db
db.users.find()
```

## 5. IDE Setup (VS Code Recommended)

### Extensions to Install

1. **Python**
   - ms-python.python
   - ms-python.vscode-pylance

2. **Frontend**
   - dbaeumer.vscode-eslint
   - esbenp.prettier-vscode

3. **Productivity**
   - GitLens
   - Thunder Client (API testing)
   - Prettier - Code formatter

### VS Code Settings

Create `.vscode/settings.json`:
```json
{
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "[python]": {
    "editor.defaultFormatter": "ms-python.python",
    "editor.formatOnSave": true
  },
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true
  }
}
```

## 6. Database Setup

### Local MongoDB

1. **Install MongoDB Community Edition**
   - [Windows](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/)
   - [macOS](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/)
   - [Linux](https://docs.mongodb.com/manual/administration/install-on-linux/)

2. **Start MongoDB**
   ```bash
   mongod
   ```

3. **Verify Connection**
   ```bash
   mongosh
   ```

### MongoDB Atlas (Cloud)

1. **Create Account**
   - Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
   - Sign up for free account

2. **Create Cluster**
   - Select M0 Free tier
   - Choose region
   - Click "Create"

3. **Get Connection String**
   - Click "Connect"
   - Select "Drivers"
   - Copy connection string
   - Update backend `.env`:
     ```env
     MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/shopverse_db?retryWrites=true&w=majority
     ```

## 7. Environment Variables

### Backend (.env)

```env
# Required
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=shopverse_db
SECRET_KEY=your-secret-key-here
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Optional (defaults provided)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
FRONTEND_URL=http://localhost:5173
API_V1_STR=/api/v1
```

### Frontend (.env)

```env
VITE_API_URL=http://localhost:8000/api/v1
VITE_GOOGLE_CLIENT_ID=your-google-client-id
```

## 8. Google OAuth Setup

See [GOOGLE_OAUTH_SETUP.md](GOOGLE_OAUTH_SETUP.md) for detailed instructions.

For development, use:
- Authorized origins: `http://localhost:5173`
- Authorized redirect: `http://localhost:8000/api/v1/auth/google/callback`

## 9. Testing the App

### Create Account
1. Go to http://localhost:5173
2. Click "Create one here"
3. Fill in form with:
   - Email: user@example.com
   - Username: testuser
   - Password: TestPass123 (must have uppercase, lowercase, digit)
4. Click "Create Account"
5. You should be on dashboard

### Test Google Login
1. Go to login page
2. Click "Sign in with Google"
3. Follow Google authentication flow

### Test API with cURL
```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123",
    "username": "testuser"
  }'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123"
  }'
```

## 10. File Structure

After setup, your file structure should look like:

```
ShopVerse/
├── backend/
│   ├── app/
│   ├── venv/                 # Virtual environment
│   ├── requirements.txt
│   ├── .env                  # ← Create this
│   └── .env.example
├── frontend/
│   ├── src/
│   ├── node_modules/         # Created after npm install
│   ├── package.json
│   ├── .env                  # ← Create this
│   └── .env.example
├── README.md
└── .git/
```

## 11. Common Issues & Solutions

### Issue: MongoDB Connection Failed
```
Error: connect ECONNREFUSED 127.0.0.1:27017
```
**Solution**: Start MongoDB with `mongod`

### Issue: Port Already in Use
```
Address already in use :::8000
```
**Solution**: Kill process using port or change port:
```bash
python -m uvicorn app.main:app --reload --port 8001
```

### Issue: Module Not Found (Backend)
```
ModuleNotFoundError: No module named 'fastapi'
```
**Solution**: Activate virtual environment:
```bash
source venv/bin/activate  # macOS/Linux
.\venv\Scripts\Activate.ps1  # Windows
```

### Issue: npm ERR (Frontend)
```
npm ERR! code ERESOLVE
```
**Solution**: Clear npm cache:
```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### Issue: Google Login Not Working
- Check `VITE_GOOGLE_CLIENT_ID` is correct
- Verify `http://localhost:5173` is in Google Console origins
- Check browser console for errors

## 12. Development Workflow

### Before Committing

1. **Backend**
   ```bash
   cd backend
   # Run linter
   python -m pylint app/
   # Run formatter
   python -m black app/
   ```

2. **Frontend**
   ```bash
   cd frontend
   # Run eslint
   npm run lint
   # Format code
   npm run format
   ```

3. **Git**
   ```bash
   git add .
   git commit -m "Descriptive message"
   git push
   ```

### Debugging

**Backend**
- Add breakpoints in VS Code
- Use `print()` for quick debugging
- Check logs in terminal

**Frontend**
- Use React Developer Tools extension
- Browser DevTools Console
- VS Code debugger

### Database Inspection

```bash
# Connect to MongoDB
mongosh

# Switch to database
use shopverse_db

# View collections
show collections

# Find all users
db.users.find()

# Find specific user
db.users.findOne({ email: "user@example.com" })

# Update user
db.users.updateOne(
  { email: "user@example.com" },
  { $set: { is_active: false } }
)

# Delete user
db.users.deleteOne({ email: "user@example.com" })
```

## 13. Hot Reload Development

Both backend and frontend support hot reload:

- **Backend**: Changes to Python files auto-reload
- **Frontend**: Changes to React files auto-refresh browser

Just save and see immediate updates!

## 14. Tips & Best Practices

- Always activate virtual environment before working on backend
- Keep both backend and frontend servers running in separate terminals
- Use `.env` for sensitive data, never commit to git
- Follow existing code style
- Add meaningful commit messages
- Test changes before pushing

## 15. Helpful Commands

```bash
# Backend
python -m uvicorn app.main:app --reload --port 8000  # Start server
python -m pytest                                      # Run tests
pip freeze                                            # Show installed packages

# Frontend
npm run dev                                           # Start dev server
npm run build                                         # Build for production
npm run preview                                       # Preview production build

# Git
git status                                            # Check status
git log --oneline                                     # View commit history
git branch -v                                         # View branches
```

## Getting Help

- Check existing errors in console logs
- Read error messages carefully
- Search GitHub issues
- Check documentation files
- Ask questions in discussions

Happy developing! 🚀
