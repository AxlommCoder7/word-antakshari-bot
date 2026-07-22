"""
/start command - Welcome message with colored buttons
"""
from pyrogram import Client, filters
from pyrogram.types import (
    Message, 
    ReplyKeyboardMarkup, 
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from pyrogram.enums import ButtonStyle, ParseMode
from config import Config


WELCOME_TEXT = """
🎮 **Welcome to {bot_name}!** 🎮

━━━━━━━━━━━━━━━━━━━━━
✨ **Game Kya Hai?** ✨
━━━━━━━━━━━━━━━━━━━━━

Yeh ek **Word Chain Game** hai jisme:
• Ek word bolo (e.g., "apple")
• Next player ko **last letter** se word bolna hoga (e.g., "e" → "elephant")
• Word ka **meaning** hona chahiye (dictionary mein hona chahiye)
• Jo word nahi de paya → **OUT!** ❌

━━━━━━━━━━━━━━━━━━━━━
🎯 **Features:**
━━━━━━━━━━━━━━━━━━━━━
✅ Multiplayer Support (2-20 players)
✅ Real Dictionary Validation
✅ Points System
✅ Pass & Leave Options
✅ Turn-based Gameplay
✅ Colored Buttons 🎨

━━━━━━━━━━━━━━━━━━━━━
👇 **Neeche buttons se choose karo:** 👇
""".format(bot_name=Config.BOT_NAME)


@Client.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    """Private chat mein /start command handle karta hai"""
    
    # Reply keyboard with colored buttons (Pyrogram ButtonStyle)
    reply_keyboard = ReplyKeyboardMarkup(
        [
            [KeyboardButton("🎮 Start Game", style=ButtonStyle.SUCCESS)],  # Green
            [
                KeyboardButton("➕ Add to Group", style=ButtonStyle.PRIMARY),  # Blue
                KeyboardButton("❓ Help", style=ButtonStyle.PRIMARY)  # Grey
            ],
            [KeyboardButton("📊 My Stats", style=ButtonStyle.DANGER)]  # Red
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    
    await message.reply_text(
        WELCOME_TEXT,
        reply_markup=reply_keyboard,
        parse_mode=ParseMode.MARKDOWN
    )


@Client.on_message(filters.command("start") & filters.group)
async def start_group(client: Client, message: Message):
    """Group mein /start command handle karta hai"""
    
    inline_keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎮 Start New Game", callback_data="start_new_game"),
            InlineKeyboardButton("❓ How to Play", callback_data="how_to_play")
        ],
        [
            InlineKeyboardButton("➕ Add Me to Group", url=f"https://t.me/{Config.BOT_USERNAME}?startgroup=true")
        ]
    ])
    
    await message.reply_text(
        f"👋 **Hello {message.chat.title}!**\n\n"
        f"Main hoon **{Config.BOT_NAME}** - Word Chain Game khelne ke liye!\n\n"
        f"Game start karne ke liye neeche button dabao 👇",
        reply_markup=inline_keyboard,
        parse_mode=ParseMode.MARKDOWN
    )
