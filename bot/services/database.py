import aiosqlite
import logging

logger = logging.getLogger(__name__)

async def init_db():
    async with aiosqlite.connect("bot.db") as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS users (
                            telegram_id INTEGER PRIMARY KEY, 
                            ad_login TEXT UNIQUE, 
                            email TEXT)''')
        await db.commit()

async def save_user(telegram_id: int, ad_login: str, email: str):
    async with aiosqlite.connect("bot.db") as db:
        try:
            await db.execute(
                "INSERT OR REPLACE INTO users (telegram_id, ad_login, email) VALUES (?, ?, ?)",
                (telegram_id, ad_login, email)
            )
            await db.commit()
            return True
        except aiosqlite.IntegrityError as e:
            logger.error(f"Database integrity error: {e}")
            return False

async def get_user_by_login(ad_login: str):
    async with aiosqlite.connect("bot.db") as db:
        cursor = await db.execute(
            "SELECT telegram_id FROM users WHERE ad_login = ?",
            (ad_login,)
        )
        return await cursor.fetchone()

async def get_user_by_tg_id(telegram_id: int):
    async with aiosqlite.connect("bot.db") as db:
        cursor = await db.execute(
            "SELECT ad_login FROM users WHERE telegram_id = ?",
            (telegram_id,)
        )
        return await cursor.fetchone()