import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from app.config import BOT_TOKEN, ADMIN_ID
from app.db import DB

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start_cmd(msg: types.Message):
    await msg.answer("Привет! Это анонимный чат.\n"
                     "/create — создать комнату\n"
                     "/join ID — зайти в комнату")


@dp.message(Command("create"))
async def create_room(msg: types.Message):
    room_id = DB.create_room(msg.from_user.id)
    await msg.answer(f"Комната создана!\nID: {room_id}\n"
                     f"Отправь другу: /join {room_id}")


@dp.message(Command("join"))
async def join_room(msg: types.Message):
    try:
        room_id = int(msg.text.split()[1])
    except:
        return await msg.answer("Формат: /join 1234")

    ok = DB.join_room(room_id, msg.from_user.id)
    if not ok:
        return await msg.answer("Эта комната не существует или уже занята.")

    await msg.answer("Вы вошли в комнату! Можете писать.")
    await bot.send_message(DB.rooms[room_id]["user1"], "Ваш собеседник подключился.")


@dp.message()
async def relay(msg: types.Message):
    # Ищем комнату, где пользователь участвует
    for room_id, room in DB.rooms.items():
        if msg.from_user.id in room.values():
            partner = DB.get_partner(room_id, msg.from_user.id)
            if partner:
                await bot.send_message(partner, msg.text)

            # Админу копия
            if ADMIN_ID:
                await bot.send_message(ADMIN_ID,
                                       f"[ROOM {room_id}] {msg.from_user.id}: {msg.text}")
            break


async def run_polling():
    await dp.start_polling(bot)
