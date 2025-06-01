from pyrogram import Client
import config
import logging
import sys
from handlers import start, settings, admin, autodelete

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("bot.log")  # Optional: saves logs to file
    ]
)

logger = logging.getLogger(__name__)

plugins = dict(root="handlers")

app = Client(
    "AutoDeleteBot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins=plugins
)

@app.on_start()
async def notify_startup(client, *args):
    logger.info("✅ Bot started successfully by t.me/theodron")

# Run the bot with error handling
if __name__ == "__main__":
    try:
        app.run()
    except Exception as e:
        logger.exception("❌ An error occurred during bot startup:")
