"""
Game commands - Main game logic yahan hai
"""
import asyncio
import time
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ParseMode, ChatMemberStatus
from config import Config
from bot.core.game_manager import GameManager
from bot.core.database import Database


# Global instances
game_manager = GameManager()
db = Database()


# ═══════════════════════════════════════════
# GAME COMMANDS
# ═══════════════════════════════════════════

@Client.on_message(filters.command("start_game") & filters.group)
async def start_game_command(client: Client, message: Message):
    """Naya game start karta hai"""
    chat_id = message.chat.id
    
    # Check if game already running
    if game_manager.is_game_running(chat_id):
        await message.reply_text(
            "⚠️ **Game already running!**\n\n"
            "Pehle current game khatam karo /end_game se.",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Create new game
    game_manager.create_game(chat_id, message.chat.title)
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Join Game", callback_data=f"join_{chat_id}"),
            InlineKeyboardButton("👥 View Players", callback_data=f"players_{chat_id}")
        ],
        [
            InlineKeyboardButton("🎮 Start Game (Admin)", callback_data=f"begin_{chat_id}")
        ]
    ])
    
    await message.reply_text(
        f"🎮 **New Game Started!** 🎮\n\n"
        f"📍 **Chat:** {message.chat.title}\n"
        f"👤 **Started by:** {message.from_user.mention}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"📋 **Instructions:**\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"1️⃣ Click 'Join Game' button to participate\n"
        f"2️⃣ Minimum {Config.MIN_PLAYERS} players required\n"
        f"3️⃣ Admin can start game with 'Start Game' button\n"
        f"4️⃣ Each turn has {Config.TURN_TIME_LIMIT} seconds\n\n"
        f"👇 **Join now!** 👇",
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN
    )


@Client.on_message(filters.command("join") & filters.group)
async def join_game_command(client: Client, message: Message):
    """Game mein join karta hai"""
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.first_name
    
    # Check if game exists
    if not game_manager.is_game_running(chat_id):
        await message.reply_text(
            "❌ **No active game!**\n\n/start_game se naya game shuru karo.",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    game = game_manager.get_game(chat_id)
    
    # Check if game already started
    if game.is_started:
        await message.reply_text(
            "⚠️ **Game already started!**\n\nNext game mein join karo.",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Check max players
    if len(game.players) >= Config.MAX_PLAYERS:
        await message.reply_text(
            f"❌ **Game full!**\n\nMaximum {Config.MAX_PLAYERS} players allowed.",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Check if already joined
    if user_id in game.players:
        await message.reply_text(
            f"⚠️ **{username}** already joined!",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Add player
    game.add_player(user_id, username)
    
    await message.reply_text(
        f"✅ **{username} joined the game!**\n\n"
        f"👥 **Players:** {len(game.players)}/{Config.MAX_PLAYERS}\n"
        f"📊 **Minimum required:** {Config.MIN_PLAYERS}",
        parse_mode=ParseMode.MARKDOWN
    )


@Client.on_message(filters.command("players") & filters.group)
async def players_command(client: Client, message: Message):
    """Current players dikhata hai"""
    chat_id = message.chat.id
    
    if not game_manager.is_game_running(chat_id):
        await message.reply_text("❌ No active game!", parse_mode=ParseMode.MARKDOWN)
        return
    
    game = game_manager.get_game(chat_id)
    
    if not game.players:
        await message.reply_text(
            "👥 **No players yet!**\n\n/join se join karo.",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    players_list = "\n".join([
        f"{i+1}. 👤 {name} (ID: {uid})" 
        for i, (uid, name) in enumerate(game.players.items())
    ])
    
    status = "🟢 Started" if game.is_started else "🟡 Waiting"
    
    await message.reply_text(
        f"👥 **Current Players**\n\n"
        f"📍 **Chat:** {message.chat.title}\n"
        f"📊 **Status:** {status}\n"
        f"👤 **Count:** {len(game.players)}/{Config.MAX_PLAYERS}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"{players_list}\n"
        f"━━━━━━━━━━━━━━━━━━━━━",
        parse_mode=ParseMode.MARKDOWN
    )


@Client.on_message(filters.command("play") & filters.group)
async def play_game_command(client: Client, message: Message):
    """Game start karta hai (admin only)"""
    chat_id = message.chat.id
    
    if not game_manager.is_game_running(chat_id):
        await message.reply_text("❌ No active game!", parse_mode=ParseMode.MARKDOWN)
        return
    
    game = game_manager.get_game(chat_id)
    
    if game.is_started:
        await message.reply_text("⚠️ Game already started!", parse_mode=ParseMode.MARKDOWN)
        return
    
    # Check minimum players
    if len(game.players) < Config.MIN_PLAYERS:
        await message.reply_text(
            f"❌ **Not enough players!**\n\n"
            f"Minimum {Config.MIN_PLAYERS} players required.\n"
            f"Current: {len(game.players)}",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Start the game
    game.start_game()
    
    # Get first player
    first_player_id = game.get_current_player_id()
    first_player_name = game.get_player_name(first_player_id)
    
    await message.reply_text(
        f"🎮 **GAME STARTED!** 🎮\n\n"
        f"👥 **Players:** {len(game.players)}\n"
        f"⏱️ **Turn Time:** {Config.TURN_TIME_LIMIT} seconds\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"🎯 **First Turn:** {first_player_name}\n\n"
        f"📝 **Your task:** Type any valid English word!\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"⚠️ Remember:\n"
        f"• Word must be in dictionary\n"
        f"• No repeated words\n"
        f"• Use /pass to skip (-{Config.PASS_PENALTY} points)\n"
        f"• Use /leave to exit",
        parse_mode=ParseMode.MARKDOWN
    )
    
    # Start turn timer
    asyncio.create_task(game.turn_timer(client, chat_id, message))


@Client.on_message(filters.command("pass") & filters.group)
async def pass_command(client: Client, message: Message):
    """Turn pass karta hai"""
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    if not game_manager.is_game_running(chat_id):
        await message.reply_text("❌ No active game!", parse_mode=ParseMode.MARKDOWN)
        return
    
    game = game_manager.get_game(chat_id)
    
    if not game.is_started:
        await message.reply_text("⚠️ Game not started yet!", parse_mode=ParseMode.MARKDOWN)
        return
    
    # Check if it's user's turn
    if game.current_player_id != user_id:
        await message.reply_text(
            "❌ **Not your turn!**\n\nWait for your turn.",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Apply penalty
    game.apply_pass_penalty(user_id, Config.PASS_PENALTY)
    
    player_name = game.get_player_name(user_id)
    
    await message.reply_text(
        f"⏭️ **{player_name} passed their turn!**\n\n"
        f"💔 **Penalty:** -{Config.PASS_PENALTY} points\n"
        f"📊 **Current Score:** {game.get_player_score(user_id)}",
        parse_mode=ParseMode.MARKDOWN
    )
    
    # Move to next player
    await game.next_turn(client, chat_id, message)


@Client.on_message(filters.command("leave") & filters.group)
async def leave_command(client: Client, message: Message):
    """Game se leave karta hai"""
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    if not game_manager.is_game_running(chat_id):
        await message.reply_text("❌ No active game!", parse_mode=ParseMode.MARKDOWN)
        return
    
    game = game_manager.get_game(chat_id)
    
    if user_id not in game.players:
        await message.reply_text("❌ You're not in the game!", parse_mode=ParseMode.MARKDOWN)
        return
    
    player_name = game.get_player_name(user_id)
    game.remove_player(user_id)
    
    await message.reply_text(
        f"👋 **{player_name} left the game!**\n\n"
        f"👥 **Remaining Players:** {len(game.players)}",
        parse_mode=ParseMode.MARKDOWN
    )
    
    # Check if game should end
    if len(game.players) < Config.MIN_PLAYERS and game.is_started:
        await message.reply_text(
            "⚠️ **Not enough players!**\n\nGame ending...",
            parse_mode=ParseMode.MARKDOWN
        )
        await end_game_command(client, message)


@Client.on_message(filters.command("end_game") & filters.group)
async def end_game_command(client: Client, message: Message):
    """Game khatam karta hai"""
    chat_id = message.chat.id
    
    if not game_manager.is_game_running(chat_id):
        await message.reply_text("❌ No active game!", parse_mode=ParseMode.MARKDOWN)
        return
    
    game = game_manager.get_game(chat_id)
    
    # Get winner if game was started
    winner_text = ""
    if game.is_started and game.players:
        winner_id = game.get_winner()
        if winner_id:
            winner_name = game.get_player_name(winner_id)
            winner_score = game.get_player_score(winner_id)
            winner_text = f"\n\n🏆 **Winner:** {winner_name} ({winner_score} points)"
    
    # End game
    game_manager.end_game(chat_id)
    
    await message.reply_text(
        f"🎮 **Game Ended!** 🎮{winner_text}\n\n"
        f"Thanks for playing! 🎉\n\n"
        f"Type /start_game to play again.",
        parse_mode=ParseMode.MARKDOWN
    )


@Client.on_message(filters.command("scoreboard") & filters.group)
async def scoreboard_command(client: Client, message: Message):
    """Scoreboard dikhata hai"""
    chat_id = message.chat.id
    
    if not game_manager.is_game_running(chat_id):
        await message.reply_text("❌ No active game!", parse_mode=ParseMode.MARKDOWN)
        return
    
    game = game_manager.get_game(chat_id)
    
    if not game.scores:
        await message.reply_text("📊 No scores yet!", parse_mode=ParseMode.MARKDOWN)
        return
    
    # Sort scores
    sorted_scores = sorted(game.scores.items(), key=lambda x: x[1], reverse=True)
    
    scoreboard = "\n".join([
        f"{i+1}. 👤 {game.get_player_name(uid)} - **{score}** points"
        for i, (uid, score) in enumerate(sorted_scores)
    ])
    
    await message.reply_text(
        f"📊 **Scoreboard** 📊\n\n"
        f"📍 **Chat:** {message.chat.title}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"{scoreboard}\n"
        f"━━━━━━━━━━━━━━━━━━━━━",
        parse_mode=ParseMode.MARKDOWN
    )


# ═══════════════════════════════════════════
# WORD INPUT HANDLER
# ═══════════════════════════════════════════

@Client.on_message(filters.text & filters.group, group=1)
async def handle_word_input(client: Client, message: Message):
    """Player ke words handle karta hai"""
    chat_id = message.chat.id
    user_id = message.from_user.id
    text = message.text.strip().lower()
    
    # Skip commands
    if text.startswith("/"):
        return
    
    # Check if game is running
    if not game_manager.is_game_running(chat_id):
        return
    
    game = game_manager.get_game(chat_id)
    
    # Check if game started
    if not game.is_started:
        return
    
    # Check if it's user's turn
    if game.current_player_id != user_id:
        return
    
    # Validate word
    is_valid, error_msg = game.validate_word(text)
    
    if not is_valid:
        await message.reply_text(
            f"❌ **Invalid Word!**\n\n{error_msg}\n\nTry again!",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Word is valid - add to game
    player_name = game.get_player_name(user_id)
    game.add_word(user_id, text)
    
    # Get next letter
    next_letter = text[-1].upper()
    
    await message.reply_text(
        f"✅ **Valid Word!**\n\n"
        f"👤 **{player_name}:** {text}\n"
        f"📊 **Score:** +10 points\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"🎯 **Next player must start with:** {next_letter}\n"
        f"━━━━━━━━━━━━━━━━━━━━━",
        parse_mode=ParseMode.MARKDOWN
    )
    
    # Move to next turn
    await game.next_turn(client, chat_id, message)


# ═══════════════════════════════════════════
# STATS COMMANDS
# ═══════════════════════════════════════════

@Client.on_message(filters.command("stats"))
async def stats_command(client: Client, message: Message):
    """User ki stats dikhata hai"""
    user_id = message.from_user.id
    
    stats = await db.get_user_stats(user_id)
    
    await message.reply_text(
        f"📊 **Your Stats** 📊\n\n"
        f"👤 **Name:** {message.from_user.first_name}\n"
        f"🎮 **Games Played:** {stats.get('games_played', 0)}\n"
        f"🏆 **Games Won:** {stats.get('games_won', 0)}\n"
        f"💯 **Total Points:** {stats.get('total_points', 0)}\n"
        f"📝 **Words Used:** {stats.get('words_used', 0)}\n"
        f"⏭️ **Passes:** {stats.get('passes', 0)}",
        parse_mode=ParseMode.MARKDOWN
    )


@Client.on_message(filters.command("leaderboard"))
async def leaderboard_command(client: Client, message: Message):
    """Global leaderboard dikhata hai"""
    leaderboard = await db.get_leaderboard(limit=10)
    
    if not leaderboard:
        await message.reply_text("📊 No data yet! Play some games first.", parse_mode=ParseMode.MARKDOWN)
        return
    
    leaderboard_text = "\n".join([
        f"{i+1}. 👤 {entry['name']} - **{entry['total_points']}** points"
        for i, entry in enumerate(leaderboard)
    ])
    
    await message.reply_text(
        f"🏆 **Global Leaderboard** 🏆\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"{leaderboard_text}\n"
        f"━━━━━━━━━━━━━━━━━━━━━",
        parse_mode=ParseMode.MARKDOWN
    )
