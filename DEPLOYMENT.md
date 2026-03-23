# Deployment Guide

This guide covers deploying ShopVerse to production on various platforms.

## Pre-Deployment Checklist

- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Update MongoDB to MongoDB Atlas (cloud)
- [ ] Update all environment variables
- [ ] Update Google OAuth Credentials (authorized origins)
- [ ] Enable HTTPS/SSL
- [ ] Set proper CORS origins
- [ ] Add rate limiting
- [ ] Set up error logging
- [ ] Test authentication flows
- [ ] Test API endpoints

## Backend Deployment

### Option 1: Heroku (Easiest)

1. **Install Heroku CLI**
```bash
npm install -g heroku
heroku login
```

2. **Create Heroku App**
```bash
cd backend
heroku create your-app-name
```

3. **Set Environment Variables**
```bash
heroku config:set MONGODB_URL="your-mongodb-atlas-url"
heroku config:set SECRET_KEY="generate-a-strong-key"
heroku config:set GOOGLE_CLIENT_ID="your-google-client-id"
heroku config:set GOOGLE_CLIENT_SECRET="your-google-client-secret"
heroku config:set FRONTEND_URL="your-frontend-url"
```

4. **Create Procfile**
```
web: pip install -r requirements.txt && python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

5. **Deploy**
```bash
git push heroku main
```

### Option 2: Railway

1. **Install Railway CLI**
```bash
npm install -g @railway/cli
railway login
```

2. **Link MongoDB**
```bash
railway add
# Select MongoDB
```

3. **Set Environment Variables**
```bash
railway variables set SECRET_KEY="generate-a-strong-key"
railroad variables set GOOGLE_CLIENT_ID="your-google-client-id"
# ... etc
```

4. **Deploy**
```bash
railway up
```

### Option 3: Docker + VPS (AWS/DigitalOcean)

1. **Create Dockerfile**
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. **Create .dockerignore**
```
.git
.venv
__pycache__
*.pyc
.env
```

3. **Build and Push to Registry**
```bash
docker build -t shopverse-backend .
docker push your-registry/shopverse-backend
```

4. **Run on VPS**
```bash
docker run -p 8000:8000 \
  -e MONGODB_URL="..." \
  -e SECRET_KEY="..." \
  your-registry/shopverse-backend
```

## Frontend Deployment

### Option 1: Vercel (Recommended for Next.js, but works with Vite)

1. **Install Vercel CLI**
```bash
npm install -g vercel
```

2. **Deploy**
```bash
cd frontend
vercel
```

3. **Set Environment Variables**
```bash
vercel env add VITE_API_URL
vercel env add VITE_GOOGLE_CLIENT_ID
```

### Option 2: Netlify

1. **Build Frontend**
```bash
cd frontend
npm run build
```

2. **Deploy via Netlify**
```bash
npm install -g netlify-cli
netlify deploy --prod --dir=dist
```

3. **Set Environment Variables in Netlify Dashboard**
- `VITE_API_URL`
- `VITE_GOOGLE_CLIENT_ID`

### Option 3: GitHub Pages

1. **Deploy**
```bash
cd frontend
npm run build
git add dist
git commit -m "Deploy frontend"
git push
```

2. **Set up GitHub Pages**
- Go to repository Settings > Pages
- Set source to "gh-pages" branch

## Environment Variables

### Production Backend (.env)

```env
MONGODB_URL=mongodb+srv://user:pass@cluster.mongodb.net/shopverse_db?retryWrites=true&w=majority
DATABASE_NAME=shopverse_db
SECRET_KEY=your-super-secure-random-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
GOOGLE_CLIENT_ID=your-production-google-client-id
GOOGLE_CLIENT_SECRET=your-production-google-secret
GOOGLE_REDIRECT_URI=https://api.yourdomain.com/api/v1/auth/google/callback
FRONTEND_URL=https://yourdomain.com
API_V1_STR=/api/v1
```

### Production Frontend (.env)

```env
VITE_API_URL=https://api.yourdomain.com/api/v1
VITE_GOOGLE_CLIENT_ID=your-production-google-client-id
```

## MongoDB Atlas Setup

1. **Create Atlas Account**
   - Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
   - Create account

2. **Create Cluster**
   - Create M0 Free tier (good for testing)
   - Select region closest to users

3. **Get Connection String**
   - Cluster > Connect
   - Copy connection string
   - Add to backend `.env`

4. **Create Database User**
   - Database Access > Add Database User
   - Create username/password
   - Update connection string with credentials

## Google OAuth Production Setup

1. **Update Google Console**
   - Add production domain to authorized origins
   - Add production callback URL
   - Update `.env` with production Client ID

2. **OAuth Flows**
   - Authorized origins: `https://yourdomain.com`
   - Authorized redirect URIs: `https://api.yourdomain.com/api/v1/auth/google/callback`

## SSL/HTTPS Setup

### Using Let's Encrypt (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d yourdomain.com -d api.yourdomain.com
```

### Using Cloudflare

1. Add domain to Cloudflare
2. Enable SSL/TLS
3. Set SSL mode to "Full" or "Full (strict)"

## Database Backups

### MongoDB Atlas Backups
- Automatic daily backups included
- 7-day retention with M0/M2+ clusters
- Manual backups available

### Manual Backup
```bash
mongodump --uri="mongodb+srv://user:pass@cluster.mongodb.net/shopverse_db"
```

## Monitoring & Logging

### Application Monitoring
- Use Sentry for error tracking
- Use New Relic for performance monitoring
- Set up log aggregation (ELK, Datadog)

### Database Monitoring
- MongoDB Atlas provides built-in monitoring
- Set up alerts for high connection count
- Monitor memory usage

## Performance Optimization

1. **Database Indexes**
   - Ensure indexes on email field
   - Profile slow queries

2. **Caching**
   - Add Redis for session storage
   - Cache user data

3. **API Optimization**
   - Minimize response payload
   - Add gzip compression

4. **Frontend Optimization**
   - Enable code splitting
   - Lazy load routes
   - Optimize bundle size

## Rate Limiting

### Backend - Flask-Limiter or Slowapi

```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@router.post("/auth/login")
@limiter.limit("5/minute")
async def login(request: UserLoginRequest):
    ...
```

## CORS in Production

Update backend CORS settings:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

## Troubleshooting Production Issues

### CORS Errors
- Verify frontend URL in backend CORS settings
- Check if requests include credentials
- Verify Content-Type headers

### MongoDB Connection Fails
- Check IP whitelist in MongoDB Atlas
- Verify connection string credentials
- Ensure database is in same region as app

### Google OAuth Not Working
- Verify production Client ID
- Check authorized origins
- Ensure redirect URI matches exactly

### Slow Performance
- Check MongoDB indexes
- Monitor database connections
- Use APM tools (New Relic, Datadog)

## Setting Up CI/CD

### GitHub Actions Example

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy Backend
        run: |
          cd backend
          # Deploy commands here
      
      - name: Deploy Frontend
        run: |
          cd frontend
          npm run build
          # Deploy commands here
```

## Security Checklist

- [ ] Enable HTTPS only
- [ ] Set secure JWT_SECRET
- [ ] Implement rate limiting
- [ ] Add request validation
- [ ] Use environment variables for secrets
- [ ] Enable CORS only for frontend domain
- [ ] Set secure MongoDB authentication
- [ ] Implement error handling
- [ ] Add request logging
- [ ] Regular security updates

## Disaster Recovery

1. **Daily Backups**
   - MongoDB Atlas automatic backups
   - Code backup via Git

2. **Monitoring Alerts**
   - Alert on database connection failures
   - Alert on authentication errors
   - Alert on API errors

3. **Rollback Plan**
   - Keep previous version tagged in Git
   - Quick rollback procedure documented
   - Database migrations prepared

## Communication & Status Page

- Set up status page (StatusPage.io, Incident.io)
- Communicate maintenance windows
- Post-incident reports

## References

- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [MongoDB Atlas](https://docs.atlas.mongodb.com/)
- [Heroku Deployment](https://devcenter.heroku.com/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
