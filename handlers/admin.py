from pyrogram import Client, filters
from pyrogram.types import Message
from config import OWNER_ID
from database import get_groups, get_users, add_sudo, add_user, add_group, add_gban, remove_gban, get_sudos
from utils.helpers import is_owner, is_sudo

@Client.on_message(filters.command("broadcast"))
async def broadcast_handler(client: Client, message: Message):
    if not await is_sudo(message.from_user.id):
        return
    if not message.reply_to_message:
        return await message.reply("❌ Reply to a message to broadcast it.")
    
    groups = await get_groups()
    users = await get_users()

    count = 0
    for chat in groups + users:
        try:
            cid = chat.get("chat_id") or chat.get("user_id")
            await message.reply_to_message.copy(cid)
            count += 1
        except: continue
    
    await message.reply(f"✅ Broadcasted to {count} chats.")

@Client.on_message(filters.command("stats"))
async def stats_handler(client: Client, message: Message):
    if not await is_sudo(message.from_user.id):
        return
    groups = await get_groups()
    users = await get_users()
    sudos = await get_sudos()
    gbans = await get_gbans()

    await message.reply_text(
        f"📊 **Bot Statistics:**\n"
        f"👥 Groups: `{len(groups)}`\n"
        f"👤 Users: `{len(users)}`\n"
        f"🔐 Sudo Users: `{len(sudos)}`\n"
        f"🚫 GBanned Users: `{len(gbans)}`"
    )

@Client.on_message(filters.command("sudo"))
async def sudo_add(client: Client, message: Message):
    if not await is_owner(message.from_user.id):
        return
    if not message.reply_to_message:
        return await message.reply("Reply to a user to make them sudo.")
    user_id = message.reply_to_message.from_user.id
    await add_sudo(user_id)
    await message.reply(f"✅ Added `{user_id}` as sudo user.")

@Client.on_message(filters.command("gban"))
async def gban_handler(client: Client, message: Message):
    if not await is_sudo(message.from_user.id):
        return
    if not message.reply_to_message:
        return await message.reply("Reply to user to gban.")
    user_id = message.reply_to_message.from_user.id
    await add_gban(user_id)
    await message.reply(f"✅ GBanned `{user_id}`. All their messages will be deleted.")

@Client.on_message(filters.command("ungban"))
async def ungban_handler(client: Client, message: Message):
    if not await is_sudo(message.from_user.id):
        return
    if not message.reply_to_message:
        return await message.reply("Reply to user to ungban.")
    user_id = message.reply_to_message.from_user.id
    await remove_gban(user_id)
    await message.reply(f"✅ Unbanned `{user_id}` from global ban.")
