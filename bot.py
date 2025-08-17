import telebot
from telebot import types
import requests
import os
import signal # Добавляем новый импорт
import sys    # Добавляем новый импорт

# --- НАСТРОЙКИ ---
BOT_TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_PANEL_URL = os.environ.get('ADMIN_PANEL_URL')
ADMIN_PANEL_API_TOKEN = os.environ.get('ADMIN_PANEL_API_TOKEN')
BOT_API_AUTH_TOKEN = os.environ.get('BOT_API_AUTH_TOKEN')
# -----------------

# Проверяем, что все переменные заданы
if not all([BOT_TOKEN, ADMIN_PANEL_URL, ADMIN_PANEL_API_TOKEN, BOT_API_AUTH_TOKEN]):
    print("FATAL ERROR: One or more environment variables are not set.")
    sys.exit(1)

bot = telebot.TeleBot(BOT_TOKEN)
user_data = {}

# --- НОВЫЙ БЛОК: Обработка сигнала остановки ---
def shutdown(signum, frame):
    print("Shutdown signal received. Stopping bot...")
    bot.stop_polling()
    sys.exit(0)

signal.signal(signal.SIGTERM, shutdown)
signal.signal(signal.SIGINT, shutdown)
# --- КОНЕЦ НОВОГО БЛОКА ---


# Тексты (остаются без изменений)
texts = {
    'ru': {
        'welcome': "Здравствуйте!\nДля продолжения, пожалуйста, выберите язык общения.",
        'menu_prompt': "Я ваш цифровой ассистент. Чем могу помочь?",
        'menu_discuss_project': "Обсудить мой проект",
        'ask_name': "Отлично! Как я могу к вам обращаться?",
        'ask_business': "Приятно познакомиться, {}!\nРасскажите коротко о вашем бизнесе (например, 'кафе').",
        'ask_task': "Спасибо! Какую главную задачу вы бы хотели поручить боту?",
        'final_thanks': "Превосходно! Спасибо за ответы. Ваша заявка передана нашему руководителю. Он скоро свяжется с вами.",
    },
    'tj': {
        'welcome': "Ассалому алейкум!\nБарои идома, лутфан забони муоширатро интихоб кунед.",
        'menu_prompt': "Ман ёрдамчии рақамии шумо. Чӣ хизмат карда метавонам?",
        'menu_discuss_project': "Лоиҳаи худро муҳокима кардан",
        'ask_name': "Олӣ! Ба шумо чӣ тавр муроҷиат кунам?",
        'ask_business': "Аз шиносоӣ бо шумо шодам, {}!\nДар бораи тиҷорати худ мухтасар нақл кунед.",
        'ask_task': "Ташаккур! Кадом вазифаи асосиро ба бот супоридан мехоҳед?",
        'final_thanks': "Беҳтарин! Ташаккур барои ҷавобҳо. Дархости шумо ба роҳбари мо фиристода шуд. Ӯ ба зудӣ бо шумо дар тамос хоҳад шуд.",
    }
}

# Все остальные обработчики (send_welcome, handle_text, process_..._step) остаются без изменений
# ... (здесь идет весь ваш код обработчиков, я его не меняю) ...

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    user_data[user_id] = {}
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_tj = types.InlineKeyboardButton("Тоҷикӣ", callback_data='lang_tj')
    btn_ru = types.InlineKeyboardButton("Русский", callback_data='lang_ru')
    markup.add(btn_tj, btn_ru)
    
    welcome_text = f"{texts['tj']['welcome']}\n\n{texts['ru']['welcome']}"
    bot.send_message(user_id, welcome_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def handle_language_selection(call):
    user_id = call.message.chat.id
    lang = call.data.split('_')[1]
    user_data[user_id] = {'lang': lang}
    
    bot.answer_callback_query(call.id)
    bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(texts[lang]['menu_discuss_project'])
    bot.send_message(user_id, texts[lang]['menu_prompt'], reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    user_id = message.chat.id
    if user_id not in user_data or 'lang' not in user_data[user_id]:
        send_welcome(message)
        return
        
    lang = user_data[user_id]['lang']
    
    if message.text == texts[lang]['menu_discuss_project']:
        msg = bot.send_message(user_id, texts[lang]['ask_name'], reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, process_name_step)

def process_name_step(message):
    user_id = message.chat.id
    user_data[user_id]['name'] = message.text
    lang = user_data[user_id]['lang']
    msg = bot.send_message(user_id, texts[lang]['ask_business'].format(message.text))
    bot.register_next_step_handler(msg, process_business_step)

def process_business_step(message):
    user_id = message.chat.id
    user_data[user_id]['business'] = message.text
    lang = user_data[user_id]['lang']
    msg = bot.send_message(user_id, texts[lang]['ask_task'])
    bot.register_next_step_handler(msg, process_task_step)

def process_task_step(message):
    user_id = message.chat.id
    user_data[user_id]['task'] = message.text
    lang = user_data[user_id]['lang']
    
    bot.send_message(user_id, texts[lang]['final_thanks'])
    
    try:
        name = user_data[user_id].get('name', 'Не указано')
        business = user_data[user_id].get('business', 'Не указано')
        task = user_data[user_id].get('task', 'Не указано')
        
        full_lead_data = (
            f"Имя: {name}\n"
            f"Бизнес: {business}\n"
            f"Задача: {task}\n"
            f"Язык: {'Русский' if lang == 'ru' else 'Тоҷикӣ'}"
        )
        
        payload = {
            'bot_api_token': BOT_API_AUTH_TOKEN,
            'customer_name': name,
            'customer_data': full_lead_data
        }

        headers = {
            'Authorization': f'Token {ADMIN_PANEL_API_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(f"{ADMIN_PANEL_URL}/api/submit_lead/", json=payload, headers=headers)
        
        if response.status_code == 201:
            print("Заявка успешно отправлена в админку.")
        else:
            print(f"Ошибка отправки в админку: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"Критическая ошибка при отправке заявки: {e}")
    
    del user_data[user_id]
    send_welcome(message)

# --- ИЗМЕНЕННЫЙ БЛОК ЗАПУСКА ---
if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(non_stop=True)
# --- КОНЕЦ ИЗМЕНЕННОГО БЛОКА ---