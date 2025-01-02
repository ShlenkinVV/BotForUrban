from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, Message, \
    CallbackQuery
import asyncio
import os
from dotenv import load_dotenv


load_dotenv()
TOKEN=os.getenv('TOKEN')


bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


main_kb=ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Рассчитать')],
    [KeyboardButton(text='Информация')],
    [KeyboardButton(text='Купить')]],
    resize_keyboard=True
)

inline_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')],
    [InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')]
])

product_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Клавиатура', callback_data="product_buying")],
    [InlineKeyboardButton(text='Мышь', callback_data="product_buying")],
    [InlineKeyboardButton(text='Коврик', callback_data="product_buying")],
    [InlineKeyboardButton(text='Наушники', callback_data="product_buying")]
])

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=['start'])
async def start_massages(message: Message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=main_kb)


@dp.message_handler(text='Купить')
async def get_buying_list(message: Message):
    with open('images/1.png', 'rb') as img:
        await message.answer_photo(img, 'Название: Клавиатура | Описание: описание 1 | Цена: 1000')
    with open('images/2.png', 'rb') as img:
        await message.answer_photo(img, 'Название: Мышь | Описание: описание 2 | Цена: 2000')
    with open('images/3.png', 'rb') as img:
        await message.answer_photo(img, 'Название: Коврик | Описание: описание 3 | Цена: 3000')
    with open('images/4.png', 'rb') as img:
        await message.answer_photo(img, 'Название: Наушники | Описание: описание 4 | Цена: 4000')
    await message.answer('Выберите продукт для покупки:', reply_markup=product_kb)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call: CallbackQuery):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@dp.message_handler(text='Рассчитать')
async def main_menu(message: Message):
    await message.answer('Выберите опцию:', reply_markup=inline_kb)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call: CallbackQuery):
    await call.message.answer(text='10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5', reply_markup=main_kb)
    await call.answer()

@dp.callback_query_handler(text = 'calories')
async def set_age(call: CallbackQuery):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message: Message, state: FSMContext):
    await state.update_data(age = message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight = message.text)
    data = await state.get_data()
    result = 10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) + 5
    await message.answer(f'Ваша норма калорий: {result}')
    await state.finish()

@dp.message_handler()
async def all_massages(message: Message):
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
