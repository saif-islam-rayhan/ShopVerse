#!/bin/bash

echo "🚀 Starting ShopVerse Setup..."

# Function to kill processes on exit (Ctrl+C)
cleanup() {
    echo "🛑 Stopping servers..."
    kill $(jobs -p) 2>/dev/null
    exit
}
trap cleanup SIGINT SIGTERM

# 1. Kill old processes on ALL ports (8000, 5000, 5173) to avoid conflicts
echo "🧹 Cleaning up old processes..."
fuser -k 5173/tcp > /dev/null 2>&1
fuser -k 8000/tcp > /dev/null 2>&1
fuser -k 5000/tcp > /dev/null 2>&1

# Check for backend .env
if [ ! -f backend/.env ]; then
    echo "⚠️  backend/.env not found! Creating from example..."
    cp backend/.env.example backend/.env
fi

# 2. Fix Frontend Configuration
echo "⚙️  Configuring Frontend Environment..."

# Preserve Google Client ID if it exists
GOOGLE_ID=""
if [ -f frontend/.env.local ] && grep -q "VITE_GOOGLE_CLIENT_ID" frontend/.env.local; then
    GOOGLE_ID=$(grep "VITE_GOOGLE_CLIENT_ID" frontend/.env.local | cut -d '=' -f2)
elif [ -f frontend/.env ] && grep -q "VITE_GOOGLE_CLIENT_ID" frontend/.env; then
    GOOGLE_ID=$(grep "VITE_GOOGLE_CLIENT_ID" frontend/.env | cut -d '=' -f2)
fi

# Remove old config files that might force port 5000
rm -f frontend/.env frontend/.env.local frontend/.env.development frontend/.env.production

# Re-create frontend/.env cleanly to ensure connection works
cat > frontend/.env.local << EOL
VITE_API_URL=http://localhost:5000/api/v1
VITE_GOOGLE_CLIENT_ID=$GOOGLE_ID
EOL

# Start Backend
cd backend
source venv/bin/activate
echo "🔥 Starting Backend on http://localhost:5000..."
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 5000 &
BACKEND_PID=$!

# 4. Wait for Backend to be ready
echo "⏳ Waiting for Backend to start..."
sleep 5

# 5. Start Frontend
cd ../frontend
echo "🎨 Starting Frontend on http://localhost:5173..."
# Force VITE_API_URL to port 5000
VITE_API_URL="http://localhost:5000/api/v1" npm run dev -- --host &

# Keep script running
wait