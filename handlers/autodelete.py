from pyrogram import Client, filters
from pyrogram.types import Message
from database import set_timer, get_timer, is_gbanned, get_setting
from datetime import datetime, timedelta
import asyncio

@Client.on_message(filters.command("auto") & filters.group)
async def set_autodelete(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Usage: /auto 5h or /auto 30m")
    
    value = message.command[1]
    try:
        if value.endswith("h"):
            hours = int(value.replace("h", ""))
            secs = hours * 3600
        elif value.endswith("m"):
            mins = int(value.replace("m", ""))
            secs = mins * 60
        elif value.endswith("d"):
            days = int(value.replace("d", ""))
            secs = days * 86400
        else:
            return await message.reply_text("❌ Invalid format. Use 5h, 30m, or 2d.")
        
        await set_timer(message.chat.id, secs)
        await message.reply_text(f"✅ Messages will now be auto-deleted after {value}.")
    except:
        await message.reply_text("❌ Invalid value. Try again.")

@Client.on_message(filters.group & ~filters.service)
async def auto_delete_handler(client: Client, message: Message):
    if await is_gbanned(message.from_user.id):
        try:
            await message.delete()
        except: pass

    timer = await get_timer(message.chat.id)
    if not timer:
        return

    # Check for specific settings
    if message.pinned_message and not await get_setting(message.chat.id, "del_pinned"):
        return
    if message.sender_chat and not await get_setting(message.chat.id, "del_posts"):
        return
    if message.reply_to_message and message.reply_to_message.sender_chat and not await get_setting(message.chat.id, "del_comments"):
        return

    try:
        await asyncio.sleep(timer)
        await message.delete()
    except: pass
