from backend.internal import secrets

from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient(secrets.MONGODB_URI)
db = client.Cluster0
