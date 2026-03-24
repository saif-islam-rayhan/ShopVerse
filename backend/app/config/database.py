"""MongoDB database connection and initialization."""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from .settings import settings
import logging

logger = logging.getLogger(__name__)

# Global database instance
db: AsyncIOMotorDatabase = None


async def connect_to_mongo():
    """Connect to MongoDB."""
    global db
    try:
        client = AsyncIOMotorClient(settings.mongodb_url)
        # Verify connection
        await client.admin.command("ping")
        db = client[settings.database_name]
        logger.info("Connected to MongoDB successfully")
        
        # Create indexes for performance
        await create_indexes()
        return db
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise


async def close_mongo_connection():
    """Close MongoDB connection."""
    global db
    if db is not None:
        db.client.close()
        logger.info("Disconnected from MongoDB")


async def create_indexes():
    """Create indexes for collections."""
    # Create unique index on email for users collection
    users_collection = db["users"]
    await users_collection.create_index("email", unique=True)
    logger.info("Created database indexes")


def get_database() -> AsyncIOMotorDatabase:
    """Get database instance."""
    if db is None:
        raise RuntimeError("Database connection not initialized")
    return db
