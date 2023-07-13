from bson.objectid import ObjectId
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from motor.motor_asyncio import AsyncIOMotorCollection

class CRUDBase():
    def __init__(self, collection: Type[AsyncIOMotorCollection]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `collection`: An AsyncIOMotorCollection model class
        * `helper`: Function to help read and create an obj
        """
        self.collection = collection

    async def get_multi(self):
        objs = []
        async for obj in self.collection.find({}, {"_id": 0}):
            objs.append(obj)
        return objs


    # Add a new obj into to the database

    async def create(self, data: dict) -> dict:
        obj = await self.collection.insert_one(data)
        new_obj = await self.collection.find_one({"_id": obj.inserted_id})
        del new_obj["_id"]
        return new_obj


    # Retrieve a obj with a matching ID

    async def get(self, id: str) -> dict:
        obj = await self.collection.find_one({"_id": ObjectId(id)})
        if obj:
            del obj["_id"]
            return obj

    # Update an obj with a matching ID
    async def update(self, id: str, data: dict):
        # Return false if an empty request body is sent.
        if len(data) < 1:
            return False
        obj = await self.collection.find_one({"_id": ObjectId(id)})
        if obj:
            updated_obj = await self.collection.update_one(
                {"_id": ObjectId(id)}, {"$set": data}
            )
            if updated_obj:
                return True
            return False

    # Delete an obj from the database
    async def remove(self, id: str):
        obj = await self.collection.find_one({"_id": ObjectId(id)})
        if obj:
            await self.collection.delete_one({"_id": ObjectId(id)})
            return True