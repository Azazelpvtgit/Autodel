from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InputMediaPhoto
from config import START_TEXT, START_IMAGE
from database import add_user, add_group
from utils.buttons import start_buttons, commands_panel, group_intro_buttons

@Client.on_message(filters.private & filters.command("start"))
async def start_pm(client: Client, message: Message):
    await add_user(message.from_user.id)
    await message.reply_photo(
        photo=START_IMAGE,
        caption=START_TEXT.format(user=message.from_user.mention),
        reply_markup=start_buttons()
    )

@Client.on_message(filters.group & filters.command("start"))
async def start_group(client: Client, message: Message):
    await add_group(message.chat.id, message.chat.title)
    await message.reply(
        text="👋 Hello! I'm active in this group to auto-delete messages based on your settings.",
        reply_markup=group_intro_buttons()
    )

@Client.on_callback_query(filters.regex("commands"))
async def commands_menu(client: Client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        "**📚 Bot Commands:**\n\n"
        "`/settings` – Configure message deletion\n"
        "`/auto [time]` – Set delete delay (e.g., /auto 5h)\n"
        "`/broadcast` – Owner/Sudo broadcast\n"
        "`/stats` – Show usage stats\n"
        "`/sudo` – Add sudo user (owner only)\n"
        "`/gban` / `/ungban` – Message deletion of banned users",
        reply_markup=commands_panel()
    )

@Client.on_callback_query(filters.regex("back"))
async def back_to_start(client: Client, callback_query: CallbackQuery):
    await callback_query.message.edit_media(
        media=InputMediaPhoto(
            media=START_IMAGE,
            caption=START_TEXT.format(user=callback_query.from_user.mention)
        ),
        reply_markup=start_buttons()
  )
