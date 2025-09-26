import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from dotenv import load_dotenv
import requests

load_dotenv()
URL = 'https://openlibrary.org/search.json?'
TOKEN = os.getenv('TOKEN')

TOKENS_NAME = [TOKEN]
MISSING_TOKENS_MESSAGE = 'Tokens are missing: {missing_tokens}.'

WELCOME_MESSAGE = ('Hi, {username}! Welcome to your personal assistant!\n\n'
                   'This bot is powered by Open Library, '
                   'giving you access to millions of books and authors.')
CHOOSE_OPTION_MESSAGE = 'Please choose an option!'
ENTER_TITLE_MESSAGE = 'Please enter the title of book'


# Определяем состояния для FSM
class BookStates(StatesGroup):
    waiting_for_title = State()


def check_tokens():
    missing_tokens = [
        token for token in TOKENS_NAME
        if not globals().get(token)
    ]
    if missing_tokens:
        raise ValueError(MISSING_TOKENS_MESSAGE.format(missing_tokens))


def get_book_info(title):
    """Получаем информацию о книге из API"""
    params = {'title': title}
    response = requests.get(URL, params=params)
    data = response.json()
    if not data['docs']:
        return None
    return data['docs'][0]


async def main():

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    @dp.message(Command('start'))
    async def send_welcome(message: types.Message):
        inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text='Open Library Site',
                url='https://openlibrary.org'
            )]
        ])

        reply_keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='Search Book'),
                 KeyboardButton(text='Random Book')],
                [KeyboardButton(text='Help')]
            ],
            resize_keyboard=True,
            one_time_keyboard=False
        )

        await message.answer(
            WELCOME_MESSAGE.format(
                username=message.from_user.first_name
            ),
            reply_markup=inline_keyboard
        )
        await message.answer(
            CHOOSE_OPTION_MESSAGE,
            reply_markup=reply_keyboard
        )

    @dp.message(Command('search_book'))
    @dp.message(F.text == 'Search Book')
    async def search_book(message: types.Message, state: FSMContext):
        await message.answer(ENTER_TITLE_MESSAGE)
        await state.set_state(BookStates.waiting_for_title)

    # Обработчик состояния ожидания названия книги
    @dp.message(BookStates.waiting_for_title)
    async def send_book_info(message: types.Message, state: FSMContext):

        book_info = get_book_info(message.text)

        # Формируем ответ
        title = book_info.get('title', 'Unknown title')
        authors = ', '.join(book_info.get('author_name', ['Unknown author']))
        year = book_info.get('first_publish_year', 'unknown year')

        response = (
            f'<b>{title}</b>\n'
            f'<b>Author(s):</b> {authors}\n'
            f'<b>First published:</b> {year}\n'
            f'\n<i>Powered by Open Library</i>'
        )

        book_key = book_info.get('key', '')
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text='View on Open Library',
                url=f'https://openlibrary.org{book_key}'
            )]
        ])

        await message.answer(response, parse_mode='HTML', reply_markup=markup)
        await state.clear()

    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    asyncio.run(main())
