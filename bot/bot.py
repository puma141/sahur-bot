import logging
import os
import subprocess
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile
from aiogram.utils import executor

API_TOKEN = "7962214835:AAFvBvk5eMcyCCEHKSvv7HCQIbooVKYXqMU"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Отправь мне ссылку на YouTube-видео, и я загружу его для тебя.")

@dp.message_handler()
async def download_video(message: types.Message):
    url = message.text.strip()
    if not url.startswith("http"):
        await message.reply("Пожалуйста, отправь корректную ссылку на видео.")
        return

    try:
        await message.reply("Загружаю видео, подожди...")

        cmd = [
            "yt-dlp.exe",
            "--cookies", "cookies.txt",
            "-f", "mp4",
            "-o", "video.%(ext)s",
            url
        ]
        subprocess.run(cmd, check=True)

        if os.path.exists("video.mp4"):
            await message.reply_document(InputFile("video.mp4"))
            os.remove("video.mp4")
        else:
            await message.reply("Не удалось найти загруженное видео.")

    except subprocess.CalledProcessError:
        await message.reply("Ошибка при загрузке видео. Возможно, нужно использовать cookies.txt.")
    except Exception as e:
        await message.reply(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
