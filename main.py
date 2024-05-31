import telebot
from telebot import types
import random

bot = telebot.TeleBot('7452252630:AAHHuRqic_PPAdyGlL-uxUpzxRGVB23h7zo')

user_perfumes = {}

@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id not in user_perfumes:
        user_perfumes[message.from_user.id] = []
        user_name = message.from_user.first_name
        bold_user_name = f'<b>{user_name}</b>'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Додати парфюм')
        btn2 = types.KeyboardButton('Зарандомити парфюм')
        markup.row(btn1, btn2)
        bot.send_message(message.chat.id, f'Hello, {bold_user_name}', parse_mode='HTML', reply_markup=markup)
        bot.register_next_step_handler(message, on_click)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Додати парфюм')
        btn2 = types.KeyboardButton('Зарандомити парфюм')
        markup.row(btn1, btn2)
        bot.send_message(message.chat.id, 'Що бажаєте зробити?', reply_markup=markup)
        bot.register_next_step_handler(message, on_click)

def on_click(message):
    if message.text == 'Додати парфюм':
        msg = bot.send_message(message.chat.id, 'Введіть назву парфуму:')
        bot.register_next_step_handler(msg, add_perfume)
    elif message.text == 'Зарандомити парфюм':
        random_perfume(message)

def add_perfume(message):
    user_id = message.from_user.id
    perfume_name = message.text

    user_perfumes[user_id].append(perfume_name)
    bot.send_message(message.chat.id, f'Парфум "{perfume_name}" додано до вашого списку!')

    start(message)

def random_perfume(message):
    user_id = message.from_user.id

    if not user_perfumes[user_id]:
        bot.send_message(message.chat.id, 'Ваш список парфумів порожній. Додайте парфуми за допомогою кнопки "Додати парфюм".')
    else:
        chosen_perfume = random.choice(user_perfumes[user_id])
        bot.send_message(message.chat.id, f'Ваш випадковий парфум: "{chosen_perfume}"')

    start(message)

def delete_parfum(message):
    user_id = message.from_user.id


@bot.message_handler(commands=['help'])
def help(message):
    commands_list = [
        "/start - почати використання бота",
        "/help - показати список доступних команд"
    ]
    bot.send_message(message.chat.id, "\n".join(commands_list))

bot.polling(none_stop=True)
