from motor.motor_asyncio import AsyncIOMotorClient

from preview.internal import secrets

client = AsyncIOMotorClient(secrets.MONGODB_URI)
cluster = client.Cluster0
chat_logs = cluster.chat_logs

async def ping_server():
    try:
        await client.admin.command('ping')
        print('Ping success!')
    except Exception as e:
        print(e)
