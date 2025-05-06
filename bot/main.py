import os
import logging
from pathlib import Path
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.handlers import auth_handlers, password_handlers
from bot.services.database import init_db
from bot.handlers.states import AuthState

load_dotenv()

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

log_file = LOG_DIR / "password_reset.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_file, mode='a', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

config = {
    'LDAP_SERVER': os.getenv("LDAP_SERVER"),
    'LDAP_PORT': 636,
    'LDAP_BIND_USER': os.getenv("LDAP_BIND_USER"),
    'LDAP_BIND_PASSWORD': os.getenv("LDAP_BIND_PASSWORD"),
    'LDAP_BASE_DN': os.getenv("LDAP_BASE_DN"),
    'SMTP_SERVER': "smtp.gmail.com",   # Изменить на smtp.office365.com
    'SMTP_PORT': 587,
    'SMTP_USER': os.getenv("SMTP_USER"),
    'SMTP_PASSWORD': os.getenv("SMTP_PASSWORD")
}

async def wrap_cmd_start(message: types.Message, state: FSMContext):
    await auth_handlers.cmd_start(message, state, config)

async def wrap_process_login(message: types.Message, state: FSMContext):
    await auth_handlers.process_login(message, state, config)

async def wrap_retry_login(message: types.Message, state: FSMContext):
    await auth_handlers.retry_login(message, state, config)

async def wrap_reset_password(message: types.Message):
    await password_handlers.reset_password(message, config)

async def main():
    await init_db()
    bot = Bot(token=os.getenv("TOKEN"))
    dp = Dispatcher()

    dp.message.register(wrap_cmd_start, Command("start"))
    dp.message.register(wrap_process_login, AuthState.awaiting_login)
    dp.message.register(auth_handlers.process_code, AuthState.awaiting_code)
    dp.message.register(wrap_retry_login, lambda msg: msg.text == "🔄 Попробовать ещё раз")
    dp.message.register(wrap_reset_password, lambda msg: msg.text == "🔑 Сбросить пароль")

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    asyncio.run(main())