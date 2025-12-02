from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from app.config import BOT_TOKEN, WEBHOOK_BASE
from app.bot import dp
import asyncio

app = FastAPI()
bot = Bot(BOT_TOKEN)


@app.on_event("startup")
async def on_startup():
    if WEBHOOK_BASE:
        webhook_url = WEBHOOK_BASE + "/webhook"
        await bot.set_webhook(webhook_url)
        print("Webhook set:", webhook_url)


@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update(**data)
    await dp.feed_raw_update(bot, update)
    return {"ok": True}
