from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.services import database, ldap_service, email_service
from bot.handlers.states import AuthState
import random
import string

async def generate_confirmation_code():
    return ''.join(random.choices(string.digits, k=6))

async def cmd_start(message: types.Message, state: FSMContext, config: dict):
    user = await database.get_user_by_tg_id(message.from_user.id)
    if user:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="🔑 Сбросить пароль")]],
            resize_keyboard=True
        )
        await message.answer("Вы уже привязаны. Доступен сброс пароля:", reply_markup=keyboard)
    else:
        await message.answer("Введите ваш AD-логин:")
        await state.set_state(AuthState.awaiting_login)

async def process_login(message: types.Message, state: FSMContext, config: dict):
    ad_login = message.text.strip().lower()
    existing_user = await database.get_user_by_login(ad_login)

    if existing_user:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="🔄 Попробовать ещё раз")]],
            resize_keyboard=True,
            one_time_keyboard=True
        )
        response = ("Этот логин уже привязан к вашему аккаунту."
                    if existing_user[0] == message.from_user.id
                    else "⚠️ Этот логин уже привязан к другому Telegram аккаунту!")
        await message.answer(response, reply_markup=keyboard)
        await state.clear()
        return

    found, email = await ldap_service.check_ad_login(ad_login, config)

    if not found or not email:
        await message.answer("Логин не найден в AD. Попробуйте еще раз.")
        return

    code = await generate_confirmation_code()
    if await email_service.send_confirmation_email(email, code):
        await state.update_data(ad_login=ad_login, email=email, code=code)
        await message.answer(f"✉️ Код отправлен на {email}. Введите его:")
        await state.set_state(AuthState.awaiting_code)
    else:
        await message.answer("❌ Ошибка отправки письма. Попробуйте позже.")

async def process_code(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.text.strip() != data["code"]:
        await message.answer("❌ Неверный код. Попробуйте ещё раз.")
        return

    success = await database.save_user(
        message.from_user.id,
        data["ad_login"],
        data["email"]
    )

    if success:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="🔑 Сбросить пароль")]],
            resize_keyboard=True
        )
        await message.answer("✅ Привязка успешна!", reply_markup=keyboard)
    else:
        await message.answer("⚠️ Произошла ошибка при сохранении данных!")

    await state.clear()

async def retry_login(message: types.Message, state: FSMContext, config: dict):
    await cmd_start(message, state, config)