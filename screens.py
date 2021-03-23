from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from threading import Timer

from sheets import history_books, current_books, search_books


def StartMenu(update, context):
    keyboard = [
        [InlineKeyboardButton('Взять', callback_data='take_book')],
        [InlineKeyboardButton('Мои книги', callback_data='list_book')],
        [InlineKeyboardButton('Поделиться', callback_data='share_point')],
    ]
    if context.chat_data['reply']:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='X-Booking! 🌟',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        update.message.reply_text('Привет! Добро пожаловать в X-Booking! 🌟', reply_markup=InlineKeyboardMarkup(keyboard))


def TakeBook(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Введи название / автора'
    )
    context.chat_data['screen'] = 'SearchBook'


def ListBooks(update, context):
    list_books = current_books(update, context)
    keyboard = []
    for i, name_book in enumerate(list_books):
        row_str = str(i + 1) + '. ' + name_book
        row_book = [InlineKeyboardButton(row_str, callback_data='info_book')]
        keyboard.append(row_book)

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Книжки, которые ты взял почитать:',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    keyboard = [
        [InlineKeyboardButton('Возврат в меню', callback_data='start_menu')],
    ]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Спасибо, что пользуешься нашим сервисом, \n\
надеемся книжки, которыми мы делимся \n\
помогают тебе в достижении твоих целей! \n\
Не забудь вовремя вернуть, участники нашего комьюнити, \n\
возможно, хотят почитать эти книжки тоже \U000026C4',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


def SearchBook(update, context):
    context.chat_data['book'] = update.message.text
    context.chat_data['list_book'] = []
    results = search_books(update, context)
    if len(results) == 0:
        keyboard = [
            [InlineKeyboardButton(f'Хорошо, я нашел {context.chat_data["book"]}', callback_data='start_menu')],
        ]
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Упс! Не получилось найти такую книгу 🙄 \n\
Попробуйте еще раз или напишите в личку нашему менеджеру @galimoved. \n\
Вы можете нажать на кнопку ниже, наши менеджеры увидят, какую книжку вы взяли 🙂',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        context.chat_data['screen'] = 'SearchBook'
    elif len(results) > 5:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Мы нашли много схожих вариантов 🙄 \n\
Пожалуйста, введи название полностью 🙌🏼'
        )
        context.chat_data['screen'] = 'SearchBook'
    elif len(results) > 1 and len(results) <= 5:
        keyboard = []
        for i, result in enumerate(results):
            keyboard.append([InlineKeyboardButton(f'{i + 1}. {result}', callback_data=f'record_book_{i}')])
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Похоже, ты выбрал одну из этих книг👇🏼 \n\
Нажми на ту, которую ты выбрал и забирай читать!',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        context.chat_data['list_book'] = results
    elif len(results) == 1:
        keyboard = [[InlineKeyboardButton(f'{results[0]}', callback_data='record_book_0')]]
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Похоже, ты выбрал эту книжку 👇🏼 \n\
 Нажми на нее и забирай читать!',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        context.chat_data['list_book'] = [results[0]]


def InfoBook(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Для возврата книги приди на checkpoint \n\
и сканируй QR-code, после этого отметь возвращаемую книгу'
    )


def ReturnBook(update, context, pickpoint):
    context.chat_data['list_book'] = current_books(update, context)
    keyboard = []
    for i, name_book in enumerate(context.chat_data['list_book']):
        row_str = str(i + 1) + '. ' + name_book
        row_book = [InlineKeyboardButton(row_str, callback_data=f'return_book_{i}_{pickpoint}')]
        keyboard.append(row_book)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Выбери книгу для возврата',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def HistoryBook(update, context, pickpoint):
    history_books(update, context, pickpoint)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Книга успешно возвращена'
    )
    context.bot.send_sticker(
        chat_id=update.effective_chat.id,
        sticker='CAACAgIAAxkBAAECFgNgV0B2dK7o9XsJTl--i28HBoQ3uQACsw8AAiJVuEqjk_I7TYr_aR4E'
    )
    context.bot.send_message(
        chat_id='-1001267184860',
        text=f'@{context.chat_data.get("user")} вернул книгу {context.chat_data["book"]}'
    )


def SharePickpoint(update, context):
    context.chat_data['list_book'] = current_books(update, context)
    keyboard = [
        [InlineKeyboardButton('Первый пикпоинт', callback_data='share_book_1'),
        InlineKeyboardButton('Второй пикпоинт', callback_data='share_book_2')],
    ]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Выбери пикпоинт',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


def ShareBook(update, context, pickpoint):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Выбери книгу для добавления'
    )
    keyboard = []
    for i, name_book in enumerate(context.chat_data['list_book']):
        row_str = str(i + 1) + '. ' + name_book
        row_book = [InlineKeyboardButton(row_str, callback_data=f'shared_book_{i}_{pickpoint}')]
        keyboard.append(row_book)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Выбери книгу для добавления',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


def RecordBook(update, context):
    context.bot.send_message(
       chat_id='-1001267184860',
       text=f'@{context.chat_data.get("user")} взял почитать книгу {context.chat_data["book"]}'
    )
    keyboard = [
        [InlineKeyboardButton('Взять еще', callback_data='take_book'),
        InlineKeyboardButton('Возврат в меню', callback_data='start_menu')],
    ]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Спасибо! Мы записали книжку, которую вы взяли почитать. \n\
Пожалуйста, постарайтесь вернуть ее в течении 4-х недель 🙌🏼 \n\
Мы напомним об этом через 3 недели. \n\
Если не успеете вернуть, можно \n\
будет отложить дату возврата на пару недель 😉 \n\
Не забывайте, что многие тоже хотят прочитать эту книжку! 🙂',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    history_books(update, context, 'take')
    keyboard = [
        [InlineKeyboardButton('Верну позже', callback_data='pass_timeout'),
         InlineKeyboardButton('Не могу вернуть', callback_data='break_timeout')],
    ]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Привет! Ты уже прочитал {context.chat_data["book"]}? \n\
Сможешь вернуть в течении следующей недели?',
        reply_markup=InlineKeyboardMarkup(keyboard),
        timeout=10
    )


def PassTimeout(update, context):
    context.bot.send_message(
        chat_id='-1001267184860',
        text=f'@{context.chat_data.get("user")} взял почитать книгу \n\
{context.chat_data["book"]} \n\
и сказал, что вернет ее позже. Вы можете связаться с ним, \n\
чтобы книжка не потерялась.'
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Хорошо, напомню через пару недель 😉'
    )
    t = Timer(10.0, lambda_t, (update, context))
    t.start()


def lambda_t(update, context):
    keyboard = [
        [InlineKeyboardButton('Верну позже', callback_data='pass_timeout'),
         InlineKeyboardButton('Не могу вернуть', callback_data='break_timeout')],
    ]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Привет! Ты уже прочитал {context.chat_data["book"]}? \n\
    Сможешь вернуть в течении следующей недели?',
        reply_markup=InlineKeyboardMarkup(keyboard),
        timeout=10
    )


def BreakTimeout(update, context):
    context.bot.send_message(
        chat_id='-1001267184860',
        text=f'@{context.chat_data.get("user")} взял книгу \n\
{context.chat_data["book"]} \n\
и сказал, что не сможет ее вернуть. \n\
Вы можете связаться с ним, \n\
чтобы книжка не потерялась.'
    )
    keyboard = [
        [InlineKeyboardButton('Вернуться в меню', callback_data='start_menu')],
    ]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Окей, наш менеджер свяжется с тобой, \n\
чтобы помочь вернуть книжку на свое место',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
