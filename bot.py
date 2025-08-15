import telebot
from telebot import types

# --- ВАШИ ДАННЫЕ УЖЕ ВСТАВЛЕНЫ ---
TOKEN = '8333375119:AAFX-6-QZHaC8Ouje4hwmaTQV1JN1auTzco'
ADMIN_ID = 721157686
# ------------------------------------

bot = telebot.TeleBot(TOKEN)

# Словарь для хранения данных о пользователях во время диалога
user_data = {}

# --- Тексты на двух языках (Полная версия) ---
texts = {
    'ru': {
        'welcome': "Здравствуйте!\nДля продолжения, пожалуйста, выберите язык общения.",
        'menu_prompt': "Я ваш цифровой ассистент. Чем могу помочь?",
        # --- Кнопки меню ---
        'menu_what_bots_can_do': "Узнать, что умеют чат-боты",
        'menu_see_example': "Посмотреть пример работы",
        'menu_discuss_project': "Обсудить мой проект",
        'menu_prices': "Узнать примерные цены",
        # --- Ответы на кнопки меню ---
        'reply_what_bots_can_do': (
            "Наши чат-боты — это полноценные виртуальные сотрудники, которые умеют:\n\n"
            "✅ *Принимать заказы:* для ресторанов, кафе и магазинов.\n"
            "✅ *Записывать на услуги:* для салонов красоты, клиник, автосервисов.\n"
            "✅ *Консультировать:* отвечать на 90% частых вопросов о ценах, адресе, услугах.\n"
            "✅ *Собирать заявки:* и моментально передавать их менеджерам."
        ),
        'reply_see_example': (
            "Отличный выбор! Вместо тысячи слов — один наглядный пример.\n\n"
            "Представьте бота для ресторана:\n\n"
            "1️⃣ Клиент видит кнопки: 'Меню', 'Заказ', 'Бронь'.\n"
            "2️⃣ Нажимает 'Меню', видит категории: 'Салаты', 'Горячее'.\n"
            "3️⃣ Выбирает блюдо, добавляет в корзину.\n"
            "4️⃣ Нажимает 'Оформить заказ', пишет адрес и телефон.\n\n"
            "Всё! Заказ моментально приходит менеджеру. Просто, быстро и 24/7."
        ),
        'reply_prices': (
            "Стоимость зависит от сложности задач. Вот наши базовые пакеты:\n\n"
            "🔹 *'Старт' (450 - 2000 сомони):* Бот-визитка с информацией о компании и ответами на частые вопросы (FAQ).\n\n"
            "🔹 *'Бизнес' (2000 - 4000 сомони):* Бот с функцией онлайн-записи или приема простых заказов.\n\n"
            "🔹 *'Профи' (от 4000 сомони):* Сложный бот с интеграцией с вашей CRM-системой или базой данных."
        ),
        # --- Сбор заявки ---
        'ask_name': "Отлично! Как я могу к вам обращаться?",
        'ask_business': "Приятно познакомиться, {}!\nРасскажите коротко о вашем бизнесе (например, 'кафе', 'магазин').",
        'ask_task': "Спасибо! Какую главную задачу вы бы хотели поручить боту?",
        'final_thanks': "Превосходно! Спасибо за ответы. Ваша заявка передана нашему руководителю. Он скоро свяжется с вами.",
        'new_lead_notification': "🔥 Новая заявка! 🔥\n\nИмя: {}\nБизнес: {}\nЗадача: {}\nЯзык: Русский\n\nНужно срочно связаться!"
    },
    'tj': {
        'welcome': "Ассалому алейкум!\nБарои идома, лутфан забони муоширатро интихоб кунед.",
        'menu_prompt': "Ман ёрдамчии рақамии шумо. Чӣ хизмат карда метавонам?",
        # --- Кнопки меню ---
        'menu_what_bots_can_do': "Чат-ботҳо чӣ кор карда метавонанд",
        'menu_see_example': "Намунаи корро дидан",
        'menu_discuss_project': "Лоиҳаи худро муҳокима кардан",
        'menu_prices': "Нархҳои тахминиро фаҳмидан",
        # --- Ответы на кнопки меню ---
        'reply_what_bots_can_do': (
            "Чат-ботҳои мо кормандони виртуалии комил мебошанд, ки метавонанд:\n\n"
            "✅ *Фармоиш қабул кунанд:* барои тарабхонаҳо, қаҳвахонаҳо ва мағозаҳо.\n"
            "✅ *Барои хизматрасонӣ номнавис кунанд:* барои салонҳои зебоӣ, клиникаҳо, сервисҳои автомобилӣ.\n"
            "✅ *Машварат диҳанд:* ба 90% саволҳои маъмул дар бораи нарх, суроға, хизматрасониҳо ҷавоб диҳанд.\n"
            "✅ *Дархостҳоро ҷамъ кунанд:* ва фавран ба менеҷерон ирсол намоянд."
        ),
        'reply_see_example': (
            "Интихоби олӣ! Ба ҷои ҳазор калима — як мисоли возеҳ.\n\n"
            "Боти тарабхонаро тасаввур кунед:\n\n"
            "1️⃣ Мизоҷ тугмаҳоро мебинад: 'Меню', 'Фармоиш', 'Банд кардан'.\n"
            "2️⃣ 'Меню'-ро пахш мекунад, категорияҳоро мебинад: 'Хӯришҳо', 'Таомҳои гарм'.\n"
            "3️⃣ Таомро интихоб карда, ба сабад илова мекунад.\n"
            "4️⃣ 'Фармоиш додан'-ро пахш мекунад, суроға ва телефонро менависад.\n\n"
            "Тамом! Фармоиш фавран ба менеҷер мерасад. Содда, тез ва 24/7."
        ),
        'reply_prices': (
            "Нарх аз мураккабии вазифаҳо вобаста аст. Инҳо бастаҳои асосии мо:\n\n"
            "🔹 *'Оғоз' (450 - 2000 сомонӣ):* Бот-визитка бо маълумот дар бораи ширкат ва ҷавобҳо ба саволҳои зуд-зуд додашаванда (FAQ).\n\n"
            "🔹 *'Бизнес' (2000 - 4000 сомонӣ):* Бот бо функсияи сабти онлайн ё қабули фармоишҳои оддӣ.\n\n"
            "🔹 *'Профи' (аз 4000 сомонӣ):* Боти мураккаб бо интегратсия бо системаи CRM ё пойгоҳи додаҳои шумо."
        ),
        # --- Сбор заявки ---
        'ask_name': "Олӣ! Ба шумо чӣ тавр муроҷиат кунам?",
        'ask_business': "Аз шиносоӣ бо шумо шодам, {}!\nДар бораи тиҷорати худ мухтасар нақл кунед (масалан, 'қаҳвахона', 'мағоза').",
        'ask_task': "Ташаккур! Кадом вазифаи асосиро ба бот супоридан мехоҳед?",
        'final_thanks': "Беҳтарин! Ташаккур барои ҷавобҳо. Дархости шумо ба роҳбари мо фиристода шуд. Ӯ ба зудӣ бо шумо дар тамос хоҳад шуд.",
        'new_lead_notification': "🔥 Дархости нав! 🔥\n\nНом: {}\nТиҷорат: {}\nВазифа: {}\nЗабон: Тоҷикӣ\n\nБояд фавран дар тамос шавед!"
    }
}

# --- Функция для отображения главного меню ---
def show_main_menu(user_id, lang):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(
        types.KeyboardButton(texts[lang]['menu_what_bots_can_do']),
        types.KeyboardButton(texts[lang]['menu_see_example']),
        types.KeyboardButton(texts[lang]['menu_prices']),
        types.KeyboardButton(texts[lang]['menu_discuss_project'])
    )
    bot.send_message(user_id, texts[lang]['menu_prompt'], reply_markup=markup, parse_mode="Markdown")

# --- Обработчик команды /start ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    user_data[user_id] = {}
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_tj = types.InlineKeyboardButton("Тоҷикӣ", callback_data='lang_tj')
    btn_ru = types.InlineKeyboardButton("Русский", callback_data='lang_ru')
    markup.add(btn_tj, btn_ru)
    
    # Отправляем сообщение на обоих языках для первого контакта
    welcome_text = f"{texts['tj']['welcome']}\n\n{texts['ru']['welcome']}"
    bot.send_message(user_id, welcome_text, reply_markup=markup)

# --- Обработчик нажатия на кнопки выбора языка ---
@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def handle_language_selection(call):
    user_id = call.message.chat.id
    lang = call.data.split('_')[1]
    user_data[user_id] = {'lang': lang}
    
    bot.answer_callback_query(call.id) # Убираем часики на кнопке
    bot.delete_message(chat_id=user_id, message_id=call.message.message_id) # Удаляем кнопки выбора языка
    
    show_main_menu(user_id, lang)

# --- Обработчик текстовых сообщений (кнопок меню) ---
@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_id = message.chat.id
    text = message.text

    # Проверяем, есть ли пользователь в нашей "сессии"
    if user_id not in user_data or 'lang' not in user_data[user_id]:
        send_welcome(message)
        return
        
    lang = user_data[user_id]['lang']
    
    # --- Логика для кнопок меню ---
    if text == texts[lang]['menu_what_bots_can_do']:
        bot.send_message(user_id, texts[lang]['reply_what_bots_can_do'], parse_mode="Markdown")
    
    elif text == texts[lang]['menu_see_example']:
        bot.send_message(user_id, texts[lang]['reply_see_example'], parse_mode="Markdown")

    elif text == texts[lang]['menu_prices']:
        bot.send_message(user_id, texts[lang]['reply_prices'], parse_mode="Markdown")

    elif text == texts[lang]['menu_discuss_project']:
        msg = bot.send_message(user_id, texts[lang]['ask_name'], reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, process_name_step)
    
    else:
        # Если введено что-то другое, просто показываем меню еще раз
        show_main_menu(user_id, lang)


# --- Шаги сбора заявки ---
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
    
    # Отправляем пользователю благодарность
    bot.send_message(user_id, texts[lang]['final_thanks'])
    
    # Формируем и отправляем заявку админу
    name = user_data[user_id].get('name', 'Не указано')
    business = user_data[user_id].get('business', 'Не указано')
    task = user_data[user_id].get('task', 'Не указано')
    
    lang_full = "Русский" if lang == "ru" else "Тоҷикӣ"
    
    notification_text = (
        f"🔥 Новая заявка! 🔥\n\n"
        f"👤 **Имя:** {name}\n"
        f"🏢 **Бизнес:** {business}\n"
        f"📝 **Задача:** {task}\n"
        f"🌐 **Язык:** {lang_full}\n\n"
        f"Нужно срочно связаться!"
    )
    bot.send_message(ADMIN_ID, notification_text, parse_mode="Markdown")
    
    # Очищаем данные, чтобы пользователь мог начать сначала
    del user_data[user_id]
    
    # После завершения заявки снова показываем приветствие
    send_welcome(message)

# --- Запуск бота ---
print("Бот запущен...")
bot.polling(none_stop=True)