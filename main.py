"""
Main entry point - bot ko start karta hai
"""
import asyncio
import logging
from pyrogram import Client
from config import Config

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WordBot(Client):
    def __init__(self):
        super().__init__(
            name="word_antakshari_bot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            plugins=dict(root="bot/handlers"),
            workers=20
        )
    
    async def start(self):
        await super().start()
        logger.info(f"✅ {Config.BOT_NAME} started successfully!")
        logger.info(f"🤖 Bot Username: @{Config.BOT_USERNAME}")
    
    async def stop(self):
        await super().stop()
        logger.info("❌ Bot stopped.")


async def main():
    bot = WordBot()
    try:
        await bot.start()
        # Bot ko chalu rakhne ke liye idle
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        logger.info("Bot manually stopped by user")
    finally:
        await bot.stop()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped.")
