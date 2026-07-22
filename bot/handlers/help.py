"""
/help command - Saare commands ka detailed explanation
"""
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ParseMode
from config import Config


HELP_TEXT = """
📚 **{bot_name} - Complete Help Guide** 📚

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎮 **GAME COMMANDS** 🎮
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🟢 `/start_game` - Naya game shuru karo
🟢 `/join` - Game mein join karo
🟢 `/leave` - Game se leave karo
🟢 `/pass` - Apna turn pass karo (-{pass_penalty} points)
🟢 `/end_game` - Game khatam karo
🟢 `/players` - Current players dekho
🟢 `/scoreboard` - Sabke points dekho

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 **USER COMMANDS** 👤
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔵 `/stats` - Apni stats dekho
🔵 `/leaderboard` - Top players dekho
🔵 `/help` - Yeh help message
🔵 `/about` - Bot ke baare mein

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚙️ **ADMIN COMMANDS** ⚙️
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 `/set_turn_time <seconds>` - Turn time set karo
🔴 `/kick @user` - Player ko remove karo
🔴 `/reset` - Game reset karo

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📖 **GAME RULES** 📖
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣ Pehla player koi bhi valid word bole
2️⃣ Next player ko **last letter** se word bolna hai
3️⃣ Word **dictionary** mein hona chahiye
4️⃣ Pehle bola hua word **dobara nahi** bol sakte
5️⃣ Har turn ke liye **{turn_time} seconds** hain
6️⃣ `/pass` karne pe **{pass_penalty} points** katenge
7️⃣ Jo player time pe word nahi de paya → **OUT**
8️⃣ Last player standing = **WINNER** 🏆

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 **EXAMPLE** 💡
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Player 1: **apple** (ends with 'e')
Player 2: **elephant** (starts with 'e', ends with 't')
Player 3: **tiger** (starts with 't', ends with 'r')
Player 4: **rabbit** (starts with 'r', ends with 't')
...and so on!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""".format(
    bot_name=Config.BOT_NAME,
    pass_penalty=Config.PASS_PENALTY,
    turn_time=Config.TURN_TIME_LIMIT
)


@Client.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    """Help command handler"""
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎮 Game Rules", callback_data="help_rules"),
            InlineKeyboardButton("⚙️ Commands", callback_data="help_commands")
        ],
        [
            InlineKeyboardButton("💡 Examples", callback_data="help_examples"),
            InlineKeyboardButton("📞 Support", callback_data="help_support")
        ],
        [
            InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")
        ]
    ])
    
    await message.reply_text(
        HELP_TEXT,
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True
    )


@Client.on_message(filters.command("about"))
async def about_command(client: Client, message: Message):
    """About command - bot ke baare mein"""
    
    about_text = f"""
🤖 **About {Config.BOT_NAME}** 🤖

━━━━━━━━━━━━━━━━━━━━━
👨‍💻 **Developer:** @YourUsername
📅 **Version:** 1.0.0
🐍 **Built with:** Pyrogram
📚 **Dictionary:** NLTK WordNet + Custom
🗄️ **Database:** SQLite

━━━━━━━━━━━━━━━━━━━━━
✨ **Features:**
━━━━━━━━━━━━━━━━━━━━━
✅ Real-time multiplayer
✅ Dictionary validation
✅ Colored buttons (Pyrogram)
✅ Points & leaderboard system
✅ Turn-based gameplay
✅ Pass & leave options

━━━━━━━━━━━━━━━━━━━━━
💬 **Need Help?**
━━━━━━━━━━━━━━━━━━━━━
Type /help for commands
Contact: @YourSupportGroup
"""
    
    await message.reply_text(
        about_text,
        parse_mode=ParseMode.MARKDOWN
    )
