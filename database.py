from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL

mongo = AsyncIOMotorClient(MONGO_URL)
db = mongo.autodeletebot

groups_col = db.groups
users_col = db.users
gbans_col = db.gbans

async def add_group(chat_id, title):
    await groups_col.update_one({"chat_id": chat_id}, {"$set": {"title": title}}, upsert=True)

async def get_groups():
    return await groups_col.find().to_list(length=None)

async def add_user(user_id):
    await users_col.update_one({"user_id": user_id}, {"$set": {}}, upsert=True)

async def get_users():
    return await users_col.find().to_list(length=None)

async def set_timer(chat_id, hours):
    await groups_col.update_one({"chat_id": chat_id}, {"$set": {"timer": hours}}, upsert=True)

async def get_timer(chat_id):
    data = await groups_col.find_one({"chat_id": chat_id})
    return data.get("timer", None) if data else None

async def set_setting(chat_id, key, value):
    await groups_col.update_one({"chat_id": chat_id}, {"$set": {key: value}}, upsert=True)

async def get_setting(chat_id, key):
    data = await groups_col.find_one({"chat_id": chat_id})
    return data.get(key, False) if data else False

async def add_gban(user_id):
    await gbans_col.update_one({"user_id": user_id}, {"$set": {}}, upsert=True)

async def remove_gban(user_id):
    await gbans_col.delete_one({"user_id": user_id})

async def is_gbanned(user_id):
    return await gbans_col.find_one({"user_id": user_id}) is not None

async def add_sudo(user_id):
    await db.sudos.update_one({"user_id": user_id}, {"$set": {}}, upsert=True)

async def get_sudos():
    return [doc["user_id"] async for doc in db.sudos.find()]
  async def get_gbans():
    gbans = gbans_col.find()
    return [u async for u in gbans]
