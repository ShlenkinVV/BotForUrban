from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, Message, \
    CallbackQuery
from crud_functions import *
import os
from dotenv import load_dotenv


load_dotenv()
TOKEN=os.getenv('TOKEN')


bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
initiate_db()


main_kb=ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Рассчитать')],
    [KeyboardButton(text='Информация')],
    [KeyboardButton(text='Купить')],
    [KeyboardButton(text='Регистрация')]],
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

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()

@dp.message_handler(commands=['start'])
async def start_massages(message: Message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=main_kb)

@dp.message_handler(text='Регистрация')
async def sing_up(message: Message):
    await message.answer('Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()


@dp.message_handler(state = RegistrationState.username)
async def set_username(message: Message, state: FSMContext):
    if is_included(message.text):
        await message.answer('Пользователь существует, введите другое имя')
    else:
        await state.update_data(username = message.text)
        await message.answer('Введите свой email:')
        await RegistrationState.email.set()

@dp.message_handler(state = RegistrationState.email)
async def set_email(message: Message, state: FSMContext):
    await state.update_data(email = message.text)
    await message.answer('Введите свой возраст:')
    await RegistrationState.age.set()

@dp.message_handler(state = RegistrationState.age)
async def set_age(message: Message, state: FSMContext):
    await state.update_data(age = message.text)
    await state.update_data(balance=1000)
    data = await state.get_data()
    add_user(str(data['username']), str(data['email']), int(data['age']), int(data['balance']))
    await message.answer('Регистрация прошла успешно')
    await state.finish()


@dp.message_handler(text='Купить')
async def get_buying_list(message: Message):
    products = get_all_products()
    for product in products:
        with open(f'images/{product[0]}.png', 'rb') as img:
            await message.answer_photo(img, f'Название: {product[1]} | Описание: {product[2]} | Цена: {product[3]}')

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
