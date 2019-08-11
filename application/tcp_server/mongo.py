import motor.motor_asyncio

from application.db_config import MOTOR_ADDRESS, MOTOR_DATABASE


class MotorClient:
    def __init__(self, db_name=MOTOR_DATABASE, collection_name=None):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(MOTOR_ADDRESS[0], MOTOR_ADDRESS[1])
        self.db = self.client[db_name]
        if collection_name:
            self.collection = self.db[collection_name]

    def use_collection(self, collection_name):
        self.collection = collection_name

    async def insert_one(self, data: dict):
        result = await self.collection.insert_one(data)

    async def insert(self, data: list):
        result = await self.collection.insert_many(data)

    async def find(self, *args, **kwargs):
        cursor = self.collection.find(*args, **kwargs)
        return [document async for document in cursor if document.pop('_id', None) or 1]

    async def delete(self, *args, **kwargs):
        result = await self.collection.delete_many(*args, **kwargs)

    async def get_collections(self):
        response = await self.db.list_collection_names()
        return response
