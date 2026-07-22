"""
Main entry point - bot ko start karta hai
"""
import asyncio
import logging
import os
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
        # ═══════════════════════════════════════════
        # AUTO-DOWNLOAD WORD LIST (NEW!)
        # ═══════════════════════════════════════════
        await self._ensure_word_list()
        
        await super().start()
        logger.info(f"✅ {Config.BOT_NAME} started successfully!")
        logger.info(f"🤖 Bot Username: @{Config.BOT_USERNAME}")
    
    async def _ensure_word_list(self):
        """Check karta hai ki word list hai ya nahi, agar nahi hai toh download karta hai"""
        word_file = "data/english_words.txt"
        
        if not os.path.exists(word_file):
            logger.info("📥 Word list not found. Downloading comprehensive dictionary...")
            
            try:
                from download_words import download_word_list
                download_word_list()
                logger.info("✅ Word list downloaded successfully!")
            except Exception as e:
                logger.error(f"❌ Error downloading word list: {e}")
                logger.warning("⚠️ Bot will use NLTK dictionary only (236k words)")
        else:
            # Count words in file
            with open(word_file, 'r', encoding='utf-8') as f:
                word_count = sum(1 for line in f if line.strip())
            logger.info(f"✅ Word list found: {word_count} words")
    
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
