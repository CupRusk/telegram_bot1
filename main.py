import telebot

bot = telebot.TeleBot('7691146935:AAETEjwWIxON4LdPn0jCLzEYVIJj9CkGTb0')

# Словарь с вопросами и переходами
questions = {
    1: {
        'question': "Чем ты хотел бы заниматься в будущем?",
        'answers': ["Разработчик", "Тестировщик"],
        'next': {
            "Разработчик": 2,
            "Тестировщик": 3
        }
    },
    2: {
        'question': "Какой язык программирования тебе ближе?",
        'answers': ["Python", "C#"],
        'next': {
            "Python": "specialization_python",
            "C#": "specialization_csharp"
        }
    },
    3: {
        'question': "Что для тебя важнее: скорость разработки или качество кода?",
        'answers': ["Скорость", "Качество"],
        'next': {
            "Скорость": "specialization_fast",
            "Качество": "specialization_quality"
        }
    },
    # Добавьте еще вопросы по аналогии
}

# Словарь для хранения состояния опроса пользователей
user_states = {}

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
    bot.send_message(message.chat.id, "Доступные команды:\n1. /start - Начать\n2. /site - Сайт \n 3. /help - Помощь \n 4. /start_survey - начать опрос", parse_mode='html')

@bot.message_handler(commands=['start_survey'])
def start_survey(message):
    user_states[message.chat.id] = {'current_question': 1}  # Начинаем с первого вопроса
    ask_question(message)

@bot.message_handler(func=lambda message: message.text in ['Да', 'Нет'])
def survey_response(message):
    if message.text == 'Да':
        bot.send_message(message.chat.id, "Отлично! Начинаем опрос.")
        user_states[message.chat.id] = {'current_question': 1}  # Начинаем с первого вопроса
        ask_question(message)
    else:
        bot.send_message(message.chat.id, "Жаль, но ты всегда можешь начать позже!")

def ask_question(message):
    user_id = message.chat.id
    current_question = user_states[user_id]['current_question']
    question_data = questions.get(current_question)

    if question_data:
        # Отправляем вопрос
        question = question_data['question']
        answers = question_data['answers']

        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        for answer in answers:
            keyboard.add(telebot.types.KeyboardButton(answer))

        bot.send_message(message.chat.id, question, reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text in ['Разработчик', 'Тестировщик', 'Python', 'C#', 'Скорость', 'Качество'])
def handle_answer(message):
    user_id = message.chat.id
    answer = message.text

    current_question = user_states[user_id]['current_question']
    question_data = questions.get(current_question)

    if question_data:
        # Получаем следующий вопрос
        next_question = question_data['next'].get(answer)
        if isinstance(next_question, int):
            user_states[user_id]['current_question'] = next_question
            ask_question(message)
        else:
            # Специализация
            handle_specialization(message, next_question)

def handle_specialization(message, specialization):
    if specialization == "specialization_python":
        bot.send_message(message.chat.id, "Ты хорошо подойдешь для разработки с Python, изучи Flask или Django!")
    elif specialization == "specialization_csharp":
        bot.send_message(message.chat.id, "Ты можешь развиваться как разработчик на C# и использовать Unity для игр!")
    elif specialization == "specialization_fast":
        bot.send_message(message.chat.id, "Для тебя подойдет работа в стартапах с быстрым циклом разработки!")
    elif specialization == "specialization_quality":
        bot.send_message(message.chat.id, "Ты идеально подойдешь для работы в крупных компаниях, где важна высокая степень тестирования!")

@bot.message_handler()
def none_command(message):
    bot_username = "@RuskaGo_bot"
    help_link = f'tg://resolve?domain={bot_username}&start=help'
    
    mess = f'<b>{message.from_user.first_name}</b>! Я не умею распознавать просто текст, введи <b><a href="{help_link}">/help</a></b>!'
    bot.send_message(message.chat.id, mess, parse_mode='html')

bot.polling(none_stop=True)
