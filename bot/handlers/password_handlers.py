from aiogram import types
from bot.services import database, ldap_service
import logging
import random
import string

logger = logging.getLogger(__name__)


async def generate_password():
    digits = ''.join(random.choices(string.digits, k=4))
    symbols = ''.join(random.choices('![]{}?@#$%', k=4))
    return f"Jmart{digits}{symbols}"


async def reset_password(message: types.Message, config: dict):
    user = await database.get_user_by_tg_id(message.from_user.id)
    if not user:
        await message.answer("ℹ️ Сначала привяжите ваш AD-аккаунт через /start")
        return

    ad_login = user[0]
    new_password = await generate_password()

    try:
        success = await ldap_service.reset_ad_password(ad_login, new_password, config)
        if success:
            await message.answer(
                f"✅ Пароль сброшен: {new_password}\nСмените его при следующем входе в систему!")
        else:
            await message.answer("❌ Ошибка сброса. Попробуйте позже.")
    except Exception as e:
        logger.error(f"Password reset error: {e}")
        await message.answer("❌ Критическая ошибка. Обратитесь к администратору.")