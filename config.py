"""
Configuration loader - environment variables ko load karta hai
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Telegram credentials
    API_ID = int(os.getenv("API_ID", "0"))
    API_HASH = os.getenv("API_HASH", "")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    OWNER_ID = int(os.getenv("OWNER_ID", "0"))
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "word_bot.db")
    
    # Game settings
    TURN_TIME_LIMIT = int(os.getenv("TURN_TIME_LIMIT", "60"))
    MIN_PLAYERS = int(os.getenv("MIN_PLAYERS", "2"))
    MAX_PLAYERS = int(os.getenv("MAX_PLAYERS", "20"))
    PASS_PENALTY = int(os.getenv("PASS_PENALTY", "5"))
    
    # Bot info
    BOT_USERNAME = "WordAntakshariBot"  # Apna username daal
    BOT_NAME = "Word Antakshari Bot"
