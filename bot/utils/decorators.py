"""
Custom decorators
"""
from functools import wraps
from pyrogram.types import Message
from config import Config


def admin_only(func):
    """Sirf admin ke liye command"""
    @wraps(func)
    async def wrapper(client, message: Message, *args, **kwargs):
        # Check if user is admin
        chat = await client.get_chat(message.chat.id)
        user = await client.get_chat_member(message.chat.id, message.from_user.id)
        
        if user.status not in ["creator", "administrator"]:
            await message.reply_text("❌ Only admins can use this command!")
            return
        
        return await func(client, message, *args, **kwargs)
    return wrapper


def owner_only(func):
    """Sirf bot owner ke liye"""
    @wraps(func)
    async def wrapper(client, message: Message, *args, **kwargs):
        if message.from_user.id != Config.OWNER_ID:
            await message.reply_text("❌ Only bot owner can use this command!")
            return
        
        return await func(client, message, *args, **kwargs)
    return wrapper
