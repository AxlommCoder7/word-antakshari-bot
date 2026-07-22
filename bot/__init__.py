"""
Bot package initialization
"""
from pyrogram import Client
from config import Config

# Global bot instance
bot = Client(
    name="word_antakshari_bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)
