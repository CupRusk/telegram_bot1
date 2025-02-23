import telebot

bot = telebot.TeleBot('769221146935:AAETEjwWIxON4LdPn0jCLzEYVIJj9CkGTb0')

@bot.message_handler(commands=['start'])
def start(message):
    bot_username = "@RuskaGo_bot" 
    help_link = f'tg://resolve?domain={bot_username}&start=help'
    first_name = message.from_user.first_name or "Пользователь"
    last_name = message.from_user.last_name or ""
    
    if last_name:
        mess = f'Привет, <b>{first_name} <u>{last_name}</u></b>! Введи <b><a href="{help_link}">/help</a></b>!'
    else:
        mess = f'Привет, <b>{first_name}</b>! Введи <b><a href="{help_link}">/help</a></b>!'
    
    bot.send_message(message.chat.id, mess, parse_mode='html')

@bot.message_handler(commands=['site'])
def site(message):
    bot.send_message(message.chat.id, '🔗 <a href="https://www.youtube.com/watch?v=HodO2eBEz_8&t=2004s">Посмотреть видео</a>', parse_mode='html')

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, "Доступные команды:\n/start - Начать\n/site - Сайт")

@bot.message_handler()
def none_command(message):
    bot_username = "@RuskaGo_bot" 
    help_link = f'tg://resolve?domain={bot_username}&start=help'
    
    mess = f'<b>{message.from_user.first_name}</b>! Я не умею распознавать просто текст, введи <b><a href="{help_link}">/help</a></b>!'
    bot.send_message(message.chat.id, mess, parse_mode='html')




bot.polling(none_stop=True)
