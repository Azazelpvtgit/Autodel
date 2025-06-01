from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from database import get_setting, set_setting
from utils.buttons import settings_main, del_timer_panel, what_to_del_panel

@Client.on_message(filters.command("settings") & filters.group)
async def open_settings(client: Client, message: Message):
    await message.reply_text(
        f"🔧 **Settings of {message.chat.title}**",
        reply_markup=settings_main()
    )

@Client.on_callback_query(filters.regex("settings_main"))
async def main_settings_panel(client: Client, cq: CallbackQuery):
    await cq.message.edit_text(
        f"🔧 **Settings of {cq.message.chat.title}**",
        reply_markup=settings_main()
    )

@Client.on_callback_query(filters.regex("del_timer"))
async def del_timer_help(client: Client, cq: CallbackQuery):
    await cq.message.edit_text(
        f"⏲ To set auto-delete timer for {cq.message.chat.title}, send:\n\n"
        "`/auto 5h` → Deletes messages after 5 hours.\n\n"
        "✅ Format: `/auto 1h`, `/auto 30m`, `/auto 2d` etc.",
        reply_markup=del_timer_panel(cq.message.chat.title)
    )

@Client.on_callback_query(filters.regex("what_to_del"))
async def what_to_del_menu(client: Client, cq: CallbackQuery):
    chat_id = cq.message.chat.id
    pinned = await get_setting(chat_id, "del_pinned")
    posts = await get_setting(chat_id, "del_posts")
    comments = await get_setting(chat_id, "del_comments")
    await cq.message.edit_text(
        "**🧹 What do you want to delete?**",
        reply_markup=what_to_del_panel(pinned, posts, comments)
    )

@Client.on_callback_query(filters.regex("toggle_"))
async def toggle_options(client: Client, cq: CallbackQuery):
    chat_id = cq.message.chat.id
    key = cq.data.replace("toggle_", "")
    current = await get_setting(chat_id, f"del_{key}")
    await set_setting(chat_id, f"del_{key}", not current)
    pinned = await get_setting(chat_id, "del_pinned")
    posts = await get_setting(chat_id, "del_posts")
    comments = await get_setting(chat_id, "del_comments")
    await cq.message.edit_reply_markup(
        reply_markup=what_to_del_panel(pinned, posts, comments)
    )

@Client.on_callback_query(filters.regex("close_settings"))
async def close_settings(client: Client, cq: CallbackQuery):
    await cq.message.delete()
