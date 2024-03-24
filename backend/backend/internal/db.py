from backend.internal import secrets

from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient(secrets.MONGODB_URI)
cluster = client.Cluster0
articles = cluster.articles
