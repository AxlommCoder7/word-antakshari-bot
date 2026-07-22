"""
Game Manager - Saare games ko manage karta hai
"""
import asyncio
import time
from typing import Dict, Optional
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from config import Config
from bot.core.dictionary import Dictionary


class GameSession:
    """Ek chat ka game session"""
    
    def __init__(self, chat_id: int, chat_title: str):
        self.chat_id = chat_id
        self.chat_title = chat_title
        self.players: Dict[int, str] = {}  # user_id -> username
        self.scores: Dict[int, int] = {}   # user_id -> score
        self.words_used: list = []         # All words used in game
        self.current_player_id: Optional[int] = None
        self.current_player_index: int = 0
        self.last_letter: Optional[str] = None
        self.is_started: bool = False
        self.started_at: Optional[float] = None
        self.turn_started_at: Optional[float] = None
        self.turn_task: Optional[asyncio.Task] = None
        self.dictionary = Dictionary()
    
    def add_player(self, user_id: int, username: str):
        """Player add karta hai"""
        self.players[user_id] = username
        self.scores[user_id] = 0
    
    def remove_player(self, user_id: int):
        """Player remove karta hai"""
        if user_id in self.players:
            del self.players[user_id]
        if user_id in self.scores:
            del self.scores[user_id]
    
    def get_player_name(self, user_id: int) -> str:
        """Player ka naam return karta hai"""
        return self.players.get(user_id, "Unknown")
    
    def get_player_score(self, user_id: int) -> int:
        """Player ka score return karta hai"""
        return self.scores.get(user_id, 0)
    
    def start_game(self):
        """Game start karta hai"""
        self.is_started = True
        self.started_at = time.time()
        self.current_player_index = 0
        player_ids = list(self.players.keys())
        self.current_player_id = player_ids[0]
        self.turn_started_at = time.time()
    
    def get_current_player_id(self) -> int:
        """Current player ID return karta hai"""
        return self.current_player_id
    
    def validate_word(self, word: str) -> tuple[bool, str]:
        """Word validate karta hai"""
        word = word.lower().strip()
        
        # Check if word is empty
        if not word:
            return False, "Word cannot be empty!"
        
        # Check if word is only letters
        if not word.isalpha():
            return False, "Word must contain only letters!"
        
        # Check minimum length
        if len(word) < 2:
            return False, "Word must be at least 2 letters!"
        
        # Check if word already used
        if word in self.words_used:
            return False, f"Word '{word}' already used!"
        
        # Check if first word (no last letter requirement)
        if self.last_letter is None:
            # First word - just check dictionary
            if self.dictionary.is_valid_word(word):
                self.last_letter = word[-1]
                return True, ""
            else:
                return False, f"Word '{word}' not found in dictionary!"
        
        # Check if word starts with correct letter
        if word[0] != self.last_letter:
            return False, f"Word must start with '{self.last_letter.upper()}'!"
        
        # Check dictionary
        if not self.dictionary.is_valid_word(word):
            return False, f"Word '{word}' not found in dictionary!"
        
        # All checks passed
        self.last_letter = word[-1]
        return True, ""
    
    def add_word(self, user_id: int, word: str):
        """Word add karta hai game mein"""
        self.words_used.append(word.lower())
        self.scores[user_id] = self.scores.get(user_id, 0) + 10
    
    def apply_pass_penalty(self, user_id: int, penalty: int):
        """Pass penalty apply karta hai"""
        self.scores[user_id] = max(0, self.scores.get(user_id, 0) - penalty)
    
    def next_player(self):
        """Next player pe move karta hai"""
        if not self.players:
            return
        
        player_ids = list(self.players.keys())
        self.current_player_index = (self.current_player_index + 1) % len(player_ids)
        self.current_player_id = player_ids[self.current_player_index]
        self.turn_started_at = time.time()
    
    def get_winner(self) -> Optional[int]:
        """Winner return karta hai"""
        if not self.scores:
            return None
        return max(self.scores.items(), key=lambda x: x[1])[0]
    
    async def turn_timer(self, client: Client, chat_id: int, message: Message):
        """Turn timer - agar time khatam ho gaya toh next player"""
        while self.is_started and self.current_player_id:
            await asyncio.sleep(1)
            
            if not self.is_started:
                break
            
            elapsed = time.time() - self.turn_started_at
            
            # Warning at 10 seconds
            if int(elapsed) == Config.TURN_TIME_LIMIT - 10:
                player_name = self.get_player_name(self.current_player_id)
                await client.send_message(
                    chat_id,
                    f"⚠️ **{player_name}** - Only 10 seconds left!",
                    parse_mode=ParseMode.MARKDOWN
                )
            
            # Time's up
            if elapsed >= Config.TURN_TIME_LIMIT:
                player_name = self.get_player_name(self.current_player_id)
                await client.send_message(
                    chat_id,
                    f"⏰ **Time's up!**\n\n"
                    f"👤 {player_name} didn't respond in time.\n"
                    f"💔 Penalty: -{Config.PASS_PENALTY} points\n\n"
                    f"Moving to next player...",
                    parse_mode=ParseMode.MARKDOWN
                )
                
                self.apply_pass_penalty(self.current_player_id, Config.PASS_PENALTY)
                await self.next_turn(client, chat_id, message)
                break
    
    async def next_turn(self, client: Client, chat_id: int, message: Message):
        """Next turn pe move karta hai"""
        self.next_player()
        
        if not self.players:
            return
        
        player_name = self.get_player_name(self.current_player_id)
        required_letter = self.last_letter.upper() if self.last_letter else "ANY"
        
        await client.send_message(
            chat_id,
            f"🎯 **Next Turn:** {player_name}\n\n"
            f"📝 Start with: **{required_letter}**\n"
            f"⏱️ Time: {Config.TURN_TIME_LIMIT} seconds",
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Start new timer
        if self.turn_task:
            self.turn_task.cancel()
        self.turn_task = asyncio.create_task(self.turn_timer(client, chat_id, message))


class GameManager:
    """Saare games ko manage karta hai"""
    
    def __init__(self):
        self.games: Dict[int, GameSession] = {}
    
    def is_game_running(self, chat_id: int) -> bool:
        """Check karta hai ki game chal raha hai ya nahi"""
        return chat_id in self.games
    
    def create_game(self, chat_id: int, chat_title: str):
        """Naya game create karta hai"""
        self.games[chat_id] = GameSession(chat_id, chat_title)
    
    def get_game(self, chat_id: int) -> GameSession:
        """Game session return karta hai"""
        return self.games.get(chat_id)
    
    def end_game(self, chat_id: int):
        """Game khatam karta hai"""
        if chat_id in self.games:
            game = self.games[chat_id]
            game.is_started = False
            if game.turn_task:
                game.turn_task.cancel()
            del self.games[chat_id]
