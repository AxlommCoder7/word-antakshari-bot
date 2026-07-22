"""
Callback queries - button presses handle karta hai
"""
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ParseMode
from config import Config


@Client.on_callback_query(filters.regex("^back_to_menu$"))
async def back_to_menu(client: Client, query: CallbackQuery):
    """Main menu pe wapas jaata hai"""
    await query.message.delete()
    await query.message.reply_text(
        f"🏠 **Main Menu**\n\nType /help for commands or /start_game to begin!",
        parse_mode=ParseMode.MARKDOWN
    )
    await query.answer()


@Client.on_callback_query(filters.regex("^help_"))
async def help_callbacks(client: Client, query: CallbackQuery):
    """Help section callbacks"""
    data = query.data
    
    if data == "help_rules":
        text = """
📖 **Game Rules** 📖

1️⃣ Pehla player koi bhi valid word bole
2️⃣ Next player ko last letter se word bolna hai
3️⃣ Word dictionary mein hona chahiye
4️⃣ Pehle bola hua word dobara nahi bol sakte
5️⃣ Har turn ke liye 60 seconds hain
6️⃣ /pass karne pe 5 points katenge
7️⃣ Last player standing = WINNER 🏆
"""
    elif data == "help_commands":
        text = """
⚙️ **Commands** ⚙️

/start_game - Naya game shuru karo
/join - Game mein join karo
/leave - Game se leave karo
/pass - Apna turn pass karo
/end_game - Game khatam karo
/players - Current players dekho
/scoreboard - Sabke points dekho
/stats - Apni stats dekho
/leaderboard - Top players dekho
"""
    elif data == "help_examples":
        text = """
💡 **Examples** 💡

apple → elephant → tiger → rabbit → ...

Last letter = Next word's first letter

apple (e) → elephant (t) → tiger (r) → rabbit (t) → ...
"""
    elif data == "help_support":
        text = """
📞 **Support** 📞

Need help? Contact @YourUsername
Join our group: @YourSupportGroup
"""
    else:
        text = "Unknown option"
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back", callback_data="back_to_help")]
    ])
    
    await query.message.edit_text(text, reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)
    await query.answer()


@Client.on_callback_query(filters.regex("^back_to_help$"))
async def back_to_help(client: Client, query: CallbackQuery):
    """Help menu pe wapas"""
    from bot.handlers.help import HELP_TEXT
    
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
    
    await query.message.edit_text(HELP_TEXT, reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)
    await query.answer()


@Client.on_callback_query(filters.regex("^start_new_game$"))
async def start_new_game_callback(client: Client, query: CallbackQuery):
    """Naya game start karne ka callback"""
    from bot.handlers.game import start_game_command
    
    # Fake message object banao
    query.message.from_user = query.from_user
    await start_game_command(client, query.message)
    await query.answer("Game starting...")


@Client.on_callback_query(filters.regex("^how_to_play$"))
async def how_to_play_callback(client: Client, query: CallbackQuery):
    """How to play callback"""
    text = """
🎮 **How to Play** 🎮

1️⃣ Type /start_game to begin
2️⃣ Players join with /join
3️⃣ Admin starts with /play
4️⃣ First player says any word
5️⃣ Next player continues with last letter
6️⃣ Use /pass to skip turn (-5 points)
7️⃣ Use /leave to exit game
8️⃣ Last player standing wins! 🏆
"""
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")]
    ])
    
    await query.message.edit_text(text, reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)
    await query.answer()
