from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import SUPPORT_CHAT, UPDATES_CHANNEL

def start_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add Me To Your Group ➕", url="https://t.me/Autodeldronbot?startgroup=true")],
        [
            InlineKeyboardButton("📢 Updates", url=UPDATES_CHANNEL),
            InlineKeyboardButton("💬 Support", url=SUPPORT_CHAT)
        ],
        [InlineKeyboardButton("📚 Commands", callback_data="commands")]
    ])

def commands_panel():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back", callback_data="back")]
    ])

def group_intro_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📢 Updates", url=UPDATES_CHANNEL),
            InlineKeyboardButton("💬 Support", url=SUPPORT_CHAT)
        ],
        [InlineKeyboardButton("⚙️ Settings", callback_data="settings_main")]
    ])

def settings_main():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⏲ Del Timer", callback_data="del_timer"),
            InlineKeyboardButton("🧹 What to Del", callback_data="what_to_del")
        ],
        [InlineKeyboardButton("❌ Close", callback_data="close_settings")]
    ])

def del_timer_panel(chat_name):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("❌ Exit", callback_data="settings_main")]
    ])

def what_to_del_panel(pinned, posts, comments):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(f"Pinned Msgs {'✅' if pinned else '❌'}", callback_data="toggle_pinned"),
            InlineKeyboardButton(f"Channel Posts {'✅' if posts else '❌'}", callback_data="toggle_posts")
        ],
        [
            InlineKeyboardButton(f"Comments {'✅' if comments else '❌'}", callback_data="toggle_comments")
        ],
        [InlineKeyboardButton("🔙 Back", callback_data="settings_main")]
    ])
