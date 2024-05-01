from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from pytube import YouTube
import os
import asyncio

# Замените на API токен вашего бота
BOT_TOKEN = '7164087939:AAH7ipdQu7YC-wXHe2kN7-gQVZCwGvuwRBk'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    await message.reply("Привет! Пришли мне ссылку на YouTube видео, и я скачаю его для тебя.")


@dp.message()
async def download_youtube_video(message: types.Message):
    url = message.text
    # Проверка URL на соответствие YouTube
    if not "youtube.com/watch?" in url:
        await message.reply("Это не похоже на ссылку YouTube. Пожалуйста, отправьте действительную ссылку.")
        return

    try:
        # Используем pytube для скачивания видео
        yt = YouTube(url)
        # Выбираем стрим с максимальным разрешением
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        if not stream:
            await message.reply("Не удалось найти подходящий стрим для скачивания.")
            return

        # Скачиваем видео и сохраняем во временной папке
        file_path = stream.download()
        file_name = os.path.basename(file_path)

        # Отправляем скачанное видео пользователю
        with open(file_path, 'rb') as video_file:
            await message.reply_video(video_file, caption="Вот ваше видео!")

        # Удаляем временный файл после отправки
        os.remove(file_path)
    except Exception as e:
        await message.reply(f"Произошла ошибка во время скачивания видео: {e}")

    if __name__ == '__main__':
        dp.run_polling(bot)