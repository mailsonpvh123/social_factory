from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
import uvicorn
import os

# Variáveis de ambiente injetadas pelo Easypanel
BOT_TOKEN = os.getenv("BOT_TOKEN", "TOKEN_PROVISORIO")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://api.seudominio.com/webhook")

app = FastAPI()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@app.on_event("startup")
async def on_startup():
    # Avisa ao Telegram para onde enviar as mensagens recebidas
    await bot.set_webhook(WEBHOOK_URL)

@app.post("/webhook")
async def telegram_webhook(request: Request):
    # Recebe o pacote de dados do Telegram e processa no Aiogram
    update_data = await request.json()
    update = types.Update(**update_data)
    await dp.feed_update(bot, update)
    return {"status": "ok"}

@dp.message()
async def echo_handler(message: types.Message):
    # Resposta básica para validar que o bot está vivo
    await message.answer(f"Chefe, comando recebido na Social Factory: {message.text}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
