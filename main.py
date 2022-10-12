from aiogram import types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import bot, dp
import logging


@dp.message_handler(commands=['start', 'help'])
async def start_handler(message: types.Message):
    await bot.send_message(message.from_user.id, f"Hello {message.from_user.first_name}!")


@dp.message_handler(commands=['mem'])
async def mem_command(message: types.Message):
    mem_photo = open("media/mem.jpg", "rb")
    await bot.send_photo(message.chat.id, mem_photo)


@dp.message_handler(commands=['quiz'])
async def quiz_one(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_call_1 = InlineKeyboardButton("NEXT", callback_data="button_call_1")
    markup.add(button_call_1)

    question = "У какого животного пот красного цвета?"
    answers = [
        "Бегемот",
        "Носорог",
        "Жираф",
        "Горилла",
        "Мангуст"
    ]

    await bot.send_poll(
        chat_id=message.from_user.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=0,
        explanation='Это было легко',
        open_period=15,
        reply_markup=markup
    )


@dp.callback_query_handler(lambda call: call.data == "button_call_1")
async def quiz_two(call: types.CallbackQuery):
    markup = InlineKeyboardMarkup()
    button_call_1 = InlineKeyboardButton("NEXT", callback_data="button_call_2")
    markup.add(button_call_1)

    question = "А и Б сидели на ветке, А упал, Б пропал. Кто остался на ветке?"
    answers = [
        "А",
        "И",
        "Б",
        "Никто",
        "Ветка",
    ]

    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=1,
        explanation="Молодец",
        open_period=20,
        reply_markup=markup
    )


@dp.message_handler()
async def echo(message: types.Message):
    if message.text.isnumeric():
        await message.answer(int(message.text) ** 2)
    else:
        await bot.send_message(message.from_user.id, message.text)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)