import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext

# কনফিগারেশন
MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "shopverse_db"
TARGET_EMAIL = "saifislamrayhan2@gmail.com"
NEW_PASSWORD = "TestPass123"

# পাসওয়ার্ড হ্যাশ করার সেটআপ
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def reset_password():
    print(f"Connecting to MongoDB...")
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    # নতুন পাসওয়ার্ড হ্যাশ তৈরি করা
    hashed_password = pwd_context.hash(NEW_PASSWORD)
    
    # ডাটাবেস আপডেট করা
    result = await db.users.update_one(
        {"email": TARGET_EMAIL},
        {"$set": {"password": hashed_password}}
    )
    
    if result.modified_count > 0:
        print(f"✅ Success! Password for {TARGET_EMAIL} is now: {NEW_PASSWORD}")
    else:
        print(f"❌ Error: User with email {TARGET_EMAIL} not found.")

if __name__ == "__main__":
    asyncio.run(reset_password())