"""
Database - SQLite operations
"""
import aiosqlite
from config import Config


class Database:
    """SQLite database handler"""
    
    def __init__(self):
        self.db_path = Config.DATABASE_URL
    
    async def init_db(self):
        """Database initialize karta hai"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    games_played INTEGER DEFAULT 0,
                    games_won INTEGER DEFAULT 0,
                    total_points INTEGER DEFAULT 0,
                    words_used INTEGER DEFAULT 0,
                    passes INTEGER DEFAULT 0
                )
            """)
            await db.commit()
    
    async def get_user_stats(self, user_id: int) -> dict:
        """User ki stats return karta hai"""
        async with aiosqlite.connect(self.db_path) as db:
            await self.init_db()
            async with db.execute(
                "SELECT * FROM users WHERE user_id = ?", 
                (user_id,)
            ) as cursor:
                row = await cursor.fetchone()
                
                if row:
                    return {
                        'user_id': row[0],
                        'username': row[1],
                        'games_played': row[2],
                        'games_won': row[3],
                        'total_points': row[4],
                        'words_used': row[5],
                        'passes': row[6]
                    }
                return {}
    
    async def update_user_stats(self, user_id: int, username: str, **kwargs):
        """User stats update karta hai"""
        async with aiosqlite.connect(self.db_path) as db:
            await self.init_db()
            
            # Check if user exists
            async with db.execute(
                "SELECT user_id FROM users WHERE user_id = ?", 
                (user_id,)
            ) as cursor:
                if not await cursor.fetchone():
                    await db.execute(
                        "INSERT INTO users (user_id, username) VALUES (?, ?)",
                        (user_id, username)
                    )
            
            # Update stats
            for key, value in kwargs.items():
                await db.execute(
                    f"UPDATE users SET {key} = {key} + ? WHERE user_id = ?",
                    (value, user_id)
                )
            
            await db.commit()
    
    async def get_leaderboard(self, limit: int = 10) -> list:
        """Leaderboard return karta hai"""
        async with aiosqlite.connect(self.db_path) as db:
            await self.init_db()
            async with db.execute(
                "SELECT username, total_points FROM users ORDER BY total_points DESC LIMIT ?",
                (limit,)
            ) as cursor:
                rows = await cursor.fetchall()
                return [
                    {'name': row[0], 'total_points': row[1]}
                    for row in rows
                ]
