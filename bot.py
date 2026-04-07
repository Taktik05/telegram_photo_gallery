import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from storage import storage

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не задан в .env")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

class GalleryState(StatesGroup):
    waiting = State()

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.set_state(GalleryState.waiting)
    await message.answer(
        "Отправляй фотографии (можно несколько).\n"
        "Когда закончишь — /done\n"
        "Отменить всё — /cancel"
    )

@dp.message(Command("cancel"))
async def cmd_cancel(message: types.Message, state: FSMContext):
    storage.clear_temp_photos(message.from_user.id)
    await state.clear()
    await message.answer("Загрузка отменена")

@dp.message(F.photo, GalleryState.waiting)
async def handle_photo(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    file_bytes = await bot.download_file(file.file_path)
    filename = storage.save_photo(user_id, file_bytes.read(), ".jpg")
    storage.add_temp_photo(user_id, filename)
    count = len(storage.get_temp_photos(user_id))
    await message.answer(f"Фото {count} сохранено. Можно добавить ещё или /done")

@dp.message(Command("done"), GalleryState.waiting)
async def cmd_done(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    gallery_id = storage.create_gallery(user_id)
    if not gallery_id:
        await message.answer("Нет фотографий. Сначала отправьте фото.")
        return
    link = f"http://localhost:8080/gallery/{gallery_id}"
    await message.answer("Галерея создана!")
    await message.answer(link)
    await state.clear()

async def main():
    print("Бот запущен. Ожидание сообщений...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())