import logging
import motor.motor_asyncio

from config import settings

MONGO_DETAILS = settings.DATABASE_URL

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
print('Connected to MongoDB...')

db = client[settings.MONGO_INITDB_DATABASE]




