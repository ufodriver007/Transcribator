from aiogram.utils import executor
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
import config
import transcribator
import sqlite_db
import time


bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


async def on_startup(_):
    """Autostart"""
    sqlite_db.sql_start()
    print('Bot is online...')


@dp.message_handler(content_types=["audio", "voice"])
async def transcribe_handler(message: types.Message):
    """Handler for any audio files"""
    file_id = ''
    size = 0

    # get file id and file size
    if message.audio:
        file_id = message.audio.file_id
        size = round(message.audio.file_size / 1024 / 1024, 2)
    elif message.voice:
        file_id = message.voice.file_id
        size = round(message.voice.file_size / 1024 / 1024, 2)

    # if file size is correct, download and transcribe it
    if size < config.MAX_FILE_SIZE:
        start_time = time.time()
        print(f"Обработка запроса от {message.from_user.full_name}")
        await bot.send_message(message.from_user.id, 'Пожалуйста, подождите...')
        await bot.download_file_by_id(file_id, 'example.ogg')
        text = transcribator.get_file('example.ogg')
        await bot.send_message(message.from_user.id, text)
        await sqlite_db.sql_add(message.from_user.full_name, file_id, text)
        print(f'Запрос обработан за {round(time.time() - start_time, 2)} сек')
    else:
        await bot.send_message(message.from_user.id, f'Размер файла {size}Мб')
        await bot.send_message(message.from_user.id, f'Загрузите файл меньше {config.MAX_FILE_SIZE}Мб...')


@dp.message_handler(content_types=["any"])
async def default_handler(message: types.Message):
    """Default handler"""
    await message.answer(f'Пришлите аудио файл меньше {config.MAX_FILE_SIZE}Мб')


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
