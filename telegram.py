import steam_api
import steam_parser
import telebot
import sqlite3
from telebot import types
from decouple import config
from languages import *

bot = telebot.TeleBot(config("TELEGRAM_TOKEN"))



user_languages = sqlite3.connect('user_languages.db', check_same_thread=False)

def get_language(user):
    global user_languages
    cursor = user_languages.cursor()
    cursor.execute('SELECT language FROM users WHERE user=?', (user,))
    language = cursor.fetchone()[0]
    if language != None:
        return language
    else:
        return -1
    
def game_by_id(message, game):
    language = get_language(message.from_user.id)
    if language != -1:
        game = steam_api.get_game(game)
        
        
        if game:
            if game == -1:
                if language == RU:
                    bot.send_message(message.from_user.id, "Не удалось получить доступ к игре :(")
                elif language == EN:
                    bot.send_message(message.from_user.id, "Failed to get game :(")
            else:
                send_message, photo = steam_parser.parse_game(game, language)
                bot.send_photo(message.from_user.id, photo, caption=send_message)
        
        else:
            if language == RU:
                bot.send_message(message.from_user.id, "Игра не найдена")
            elif language == EN:
                bot.send_message(message.from_user.id, "Game not found")
                
    else:
        lang(message)

@bot.message_handler(commands=['help', 'помощь'])
def help(message):
    global user_languages
    user = message.from_user.id
    language = get_language(user)
    if language != -1:
        msg = ''
        if language == RU:
            msg = '''
Этот бот поможет вам получить информацию
о пользователе и играх в Steam.
Поменять язык:
/language или /lang
Найти пользователя:
/user + короткая ссылка пользователя или SteamID 
Например /user St4ck
Найти игру:
/game + название игры
Чтобы еще раз увидеть это сообщение:
/help или /помощь
            '''
            bot.send_message(message.from_user.id, msg)
        elif language == EN:
            msg = '''
This bot helps you to get information
about user and games on Steam.
Change language:
/language or /lang
Find user:
/user + short link or SteamID
Find game:
/game + name of game
To see this message again:
/help
            '''
            bot.send_message(message.from_user.id, msg)
        else:
            lang(message)
    else:
        lang(message)



@bot.message_handler(commands=['start', 'старт'])
def start_bot(message):
    global user_languages
    cursor = user_languages.cursor()
    
    
    cursor.execute('SELECT user FROM users WHERE user=?', (message.from_user.id,))
    
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users (user) VALUES (?)", (message.from_user.id,))
        lang(message)
    else:
        bot.send_message(message.from_user.id, "Вы уже используете бота")
    user_languages.commit()

@bot.message_handler(commands=['lang', 'язык', 'language'])
def lang(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🇷🇺 Русский")
    btn2 = types.KeyboardButton('🇬🇧 English')
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id, "🇷🇺 Выберите язык / 🇬🇧 Choose your language", reply_markup=markup)

@bot.message_handler(commands=['user', 'имя', 'player', 'игрок', 'пользователь'])
def user(message):
    user = message.from_user.id
    text = message.text.split()
    if len(text) > 1:
        text = text[1]
        language = get_language(user)   
        if language != -1:
            find_user = steam_api.search_user(text)
            if find_user:
                send_message, photo = steam_parser.parse_user(find_user, language)    
                bot.send_photo(message.from_user.id, photo, caption=send_message)
            else:
                if language == RU:
                    bot.send_message(message.from_user.id, "Пользователь не найден")
                elif language == EN:
                    bot.send_message(message.from_user.id, "User not found")
        else:
            lang(message)
    else:
        help(message)
 



@bot.message_handler(commands=['игра', 'game'])
def game(message):
    user = message.from_user.id
    text = message.text.split()
    if len(text) > 1:
        text = " ".join(text[1:])
        language = get_language(user)
        if language != -1:
            
            game = steam_api.search_game(text)
            if len(game) > 1:
                numbers = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣"]
                buttons = [telebot.types.InlineKeyboardButton(numbers[i], callback_data=(str(game[i]['id']) + ' ' + game[i]['price'])) for i in range(len(game))]
                markup = telebot.types.InlineKeyboardMarkup(row_width=len(game))
                markup.add(*buttons)
                msg = ""
                if language == RU:
                    msg = 'Найденные игры:\n'
                elif language == EN:
                    msg = 'Found games:\n'
                for i in range(len(game)):
                    msg += str(i + 1) + '. ' + game[i]['name'] + '\n'
                bot.send_message(message.from_user.id, msg, reply_markup=markup)
            elif len(game) == 1:
                game_by_id(message, str(game[0]['id']) + ' ' + game[0]['price'])
            else:
                if language == RU:
                    bot.send_message(message.from_user.id, "Игра не найдена")
                elif language == EN:
                    bot.send_message(message.from_user.id, "Game not found")
        else:
            lang(message)
    else:
        help(message)



@bot.callback_query_handler(func=lambda call:True)
def callback_inline(message):
    game_by_id(message, message.data)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global user_languages
    cursor = user_languages.cursor()
    if message.text == '🇷🇺 Русский':
        cursor.execute('UPDATE users SET language=? WHERE user=?', (RU, message.from_user.id))
        bot.send_message(message.from_user.id, "Язык установлен на 🇷🇺 Русский", reply_markup=types.ReplyKeyboardRemove())
    elif message.text == '🇬🇧 English':
        cursor.execute('UPDATE users SET language=? WHERE user=?', (EN, message.from_user.id))
        bot.send_message(message.from_user.id, "Language set to 🇬🇧 English", reply_markup=types.ReplyKeyboardRemove())
    
    user_languages.commit()
    help(message)



def start():
    global user_languages
    cursor = user_languages.cursor()
    cursor.execute('''CREATE TABLE  IF NOT EXISTS users
                (id INTEGER PRIMARY KEY AUTOINCREMENT,  
                user INTEGER,
                language INTEGER)''')
    bot.polling(none_stop=True, interval=0)

