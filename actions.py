from screens import StartMenu, \
    TakeBook, \
    ListBooks, \
    SearchBook, \
    ShareBook, \
    RecordBook, \
    ReturnBook, \
    InfoBook, \
    HistoryBook, \
    PassTimeout, \
    BreakTimeout, \
    SharePickpoint


def start(update, context):
    context.chat_data["user"] = update.message.chat.username
    if context.args and context.args[0] == 'return':
        ReturnBook(update, context, 'return')
    elif context.args and context.args[0] == 'return2':
        ReturnBook(update, context, 'return2')
    else:
        context.chat_data['reply'] = False
        StartMenu(update, context)


def buttons(update, context):
    query = update.callback_query
    query.answer()
    if query.data == 'take_book':
        TakeBook(update, context)
    elif query.data.startswith('record_book'):
        name_book = context.chat_data['list_book'][int(query.data[12:])]
        context.chat_data['book'] = name_book
        RecordBook(update, context)
    elif query.data == 'list_book':
        ListBooks(update, context)
    elif query.data == 'share_point':
        SharePickpoint(update, context)
    elif query.data.startswith('share_point'):
        if query.data[11] == '1':
            ShareBook(update, context, 'return')
        elif query.data[11] == '2':
            ShareBook(update, context, 'return2')
    elif query.data == 'info_book':
        InfoBook(update, context)
    elif query.data.startswith('return_book'):
        name_book = context.chat_data['list_book'][int(query.data[12])]
        context.chat_data['book'] = name_book
        pickpoint = query.data[14:]
        HistoryBook(update, context, pickpoint)
    elif query.data == 'start_menu':
        context.chat_data['reply'] = True
        StartMenu(update, context)
    elif query.data == 'pass_timeout':
        PassTimeout(update, context)
    elif query.data == 'break_timeout':
        BreakTimeout(update, context)
    else:
        pass


def input_text(update, context):
    if context.chat_data['screen'] == 'SearchBook':
        SearchBook(update, context)
    elif context.chat_data['screen'] == 'TakeBook':
        TakeBook(update, context)
    else:
        pass