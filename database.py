from motor.motor_asyncio import AsyncIOMotorClient
import config

client = AsyncIOMotorClient(config.MONGO_URL)
db = client.autodel

users = db.users
groups = db.groups
gbans = db.gbans


async def add_user(user_id: int):
    user = await users.find_one({"user_id": user_id})
    if not user:
        return await users.insert_one({"user_id": user_id})


async def add_group(group_id: int):
    group = await groups.find_one({"group_id": group_id})
    if not group:
        return await groups.insert_one({"group_id": group_id, "timer": 0})


async def get_groups():
    groups_list = []
    async for group in groups.find():
        groups_list.append(int(group["group_id"]))
    return groups_list


async def get_users():
    users_list = []
    async for user in users.find():
        users_list.append(int(user["user_id"]))
    return users_list


async def get_timer(group_id: int):
    group = await groups.find_one({"group_id": group_id})
    if not group:
        return 0
    return group["timer"]


async def set_timer(group_id: int, timer: int):
    await groups.update_one({"group_id": group_id}, {"$set": {"timer": timer}}, upsert=True)


async def add_gban(user_id: int):
    user = await gbans.find_one({"user_id": user_id})
    if not user:
        return await gbans.insert_one({"user_id": user_id})


async def remove_gban(user_id: int):
    return await gbans.delete_one({"user_id": user_id})


async def get_gbans():
    banned_users = []
    async for user in gbans.find():
        banned_users.append(int(user["user_id"]))
    return banned_users


async def is_gbanned(user_id: int):
    user = await gbans.find_one({"user_id": user_id})
    return bool(user)
