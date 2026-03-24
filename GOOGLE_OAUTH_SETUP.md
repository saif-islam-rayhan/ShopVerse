# Google OAuth Configuration Guide

This guide walks you through setting up Google OAuth 2.0 for the ShopVerse authentication system.

## Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click on the project dropdown in the top left
3. Click "NEW PROJECT"
4. Enter project name: "ShopVerse" (or your preferred name)
5. Click "CREATE"
6. Wait for the project to be created

## Step 2: Enable Google+ API

1. In the Google Cloud Console, go to the "APIs & Services" page
2. Click "+ ENABLE APIS AND SERVICES"
3. Search for "Google+ API"
4. Click on it and then "ENABLE"

## Step 3: Create OAuth 2.0 Client ID

1. Go to "APIs & Services" > "Credentials"
2. Click "+ CREATE CREDENTIALS"
3. Select "OAuth client ID"
4. If prompted to create a consent screen first:
   - Click "CREATE CONSENT SCREEN"
   - Select "External" user type
   - Fill in required fields:
     - App name: "ShopVerse"
     - User support email: your-email@example.com
     - Developer contact: your-email@example.com
   - Click "SAVE AND CONTINUE"
   - Skip scopes by clicking "SAVE AND CONTINUE"
   - Add test users if needed, click "SAVE AND CONTINUE"
   - Click "BACK TO DASHBOARD"

5. Now create OAuth client ID again:
   - Click "+ CREATE CREDENTIALS" > "OAuth client ID"
   - Application type: "Web application"
   - Name: "ShopVerse Web Client"

## Step 4: Configure OAuth Client

1. Under "Authorized origins (URIs)" add:
   - `http://localhost:5173` (for local development)
   - `http://127.0.0.1:5173` (recommended to add both)
   - `http://localhost:3000` (if using different port)
   - Your production domain (e.g., `https://shopverse.com`)
   - **Note:** Do not add a trailing slash (e.g., `http://localhost:5173/` is invalid for origins).

2. Under "Authorized redirect URIs" add:
   - `http://localhost:5000/api/v1/auth/google/callback` (for local development)
   - `http://localhost:5173/auth/google/callback` (alternative)
   - Your production redirect URI

3. Click "CREATE"

## Step 5: Copy Credentials

1. You'll see a dialog with your credentials
2. Copy the "Client ID" and "Client Secret"
3. Save them safely (you'll need them next)

## Step 6: Add to Backend `.env`

In `/backend/.env`:
```env
GOOGLE_CLIENT_ID=your-copied-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-copied-client-secret
GOOGLE_REDIRECT_URI=http://localhost:5000/api/v1/auth/google/callback
```

## Step 7: Add to Frontend `.env`

In `/frontend/.env`:
```env
VITE_GOOGLE_CLIENT_ID=your-copied-client-id.apps.googleusercontent.com
```

## Step 8: Test Google Login

1. Start the backend:
```bash
cd backend
python -m uvicorn app.main:app --reload
```

2. Start the frontend:
```bash
cd frontend
npm run dev
```

3. Go to `http://localhost:5173/login`
4. Click "Sign in with Google"
5. You should be redirected to Google login

## Step 9: Troubleshooting

### Issue: "Authorization failed" or redirect_uri mismatch
- Make sure redirect URI in Google Console matches exactly
- Check for trailing slashes
- Verify both backend and frontend origins are added

### Issue: Client ID is incorrect
- Double-check you copied the ID correctly
- Ensure no extra spaces
- Verify it's in `.env` files with correct variable names

### Issue: CORS error when testing Google login
- Make sure frontend and backend URLs are in CORS settings
- Check backend `settings.py` CORS configuration
- Verify `FRONTEND_URL` in backend `.env`

## For Production

When deploying to production:

1. Update Google Console credentials with production URLs:
   - Authorized origins: `https://yourdomain.com`
   - Authorized redirect URIs: `https://api.yourdomain.com/api/v1/auth/google/callback`

2. Update environment variables:
   - Backend: Update `GOOGLE_REDIRECT_URI` and `FRONTEND_URL`
   - Frontend: Update `VITE_GOOGLE_CLIENT_ID` (same ID for both dev and prod)

3. Keep `GOOGLE_CLIENT_SECRET` secure (never expose in frontend code)

## References

- [Google OAuth 2.0 Documentation](https://developers.google.com/identity/protocols/oauth2)
- [Google Cloud Console](https://console.cloud.google.com/)
- [react-oauth/google Documentation](https://github.com/react-oauth/react-oauth.github.io)
