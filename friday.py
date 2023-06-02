from aiogram import Bot, Dispatcher, executor, types
import aiogram
import python_weather
from dotenv import load_dotenv
import os

#!Connect bot to telegram
load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot)

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)# ----> Buttom inside
markup_2 = types.InlineKeyboardMarkup()# ------------> Buttom outside
admin_panel = types.ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel.add('📚Book').add('🪪ID').add('⬅️Back')

#!Start bot, commands
@dp.message_handler(commands=['start'])
async def new_func(message: types.Message):
    bt1 = types.KeyboardButton(text='📄Info')
    bt2 = types.KeyboardButton(text='🟩Sticker')
    bt3 = types.KeyboardButton(text='🌤️Weather')
    bt4 = types.KeyboardButton(text='Admin-panel')
    markup.add(bt1, bt3, bt2)
    await  bot.send_message(message.chat.id, f"Hey {message.from_user.first_name}!, What's up?".format(message.from_user), reply_markup=markup)
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer('You connected as admin', reply_markup=markup.add(bt4))
    else:
        await message.answer('You connected as guest')
        
@dp.message_handler(text=['Admin-panel'])
async def admin_panels(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(f'Welcom to admin panel', reply_markup=admin_panel)
    else:
        await message.answer(f'Command is not found')      
    
@dp.message_handler(commands=['help'])
async def new_func(message: types.Message):
    await message.answer('You got problems?\nTry to restart bot or clear\nbot and him commands')
    
@dp.message_handler(commands=['$^49$'])
async def new_func(message: types.Message):
    await message.answer(message.from_user.id)

#!Guest and admin panels
@dp.message_handler(content_types=['text'])
async def panels(message: types.Message):
    if message.chat.type == 'private':
        if message.text == '📄Info':
            await bot.send_message(message.chat.id, "Hey!, I'm friday bot asistent which gonna help you\nIt's commands whch I can do:\n/start - turn on the bot\n/help - help you if you got problem with bot")
            
        elif message.text == '🟩Sticker':
            await message.answer_sticker('CAACAgIAAxkBAAIB42R5GOF8gWQJjEYJIrzgnlNh-mzQAAJ6BwAClvoSBZ25jS0fpNKPLwQ')
            
        elif message.text == '🌤️Weather':
            client = python_weather.Client(format=python_weather.IMPERIAL)
            weather = await client.get('Nottingham')
    
            celsius = (weather.current.temperature - 32)* 5/9
            pre = (weather.current.precipitation)
            hre = (weather.current.humidity)
            num = f"The weather is: {weather.current.type};\nTemperature is: {str(round(celsius))}˚;\nPrecipitation is: {pre}\nHumidity is: {hre}%."
            await message.answer(num)
            
        elif message.text == '📚Book':
            markup_2 = types.InlineKeyboardMarkup()
            bk1 = types.InlineKeyboardButton('48 rules succes', url='http://loveread.ec/read_book.php?id=76991&p=1')
            bk2 = types.InlineKeyboardButton('Impact of mind', url='http://loveread.ec/read_book.php?id=51721&p=1')
            bk3 = types.InlineKeyboardButton('Murders in alpha order', url='http://loveread.ec/read_book.php?id=2653&p=1')
            markup_2.row(bk1,bk2)
            markup_2.row(bk3)
            await message.answer('All your books', reply_markup=markup_2)
            
        elif message.text == '🪪ID':
            await message.answer(f'Your ID: {message.from_user.id}')
            
        elif message.text == '⬅️Back':
            await message.delete()
            await message.answer('You moved to guest panel', reply_markup=markup)

@dp.message_handler(content_types=['sticker'])
async def stick(message: types.Message):   
        await message.answer(f'Very nice sticker\nThis is him ID:\n{message.sticker.file_id}')
        
#!Bot will work always
executor.start_polling(dp)
