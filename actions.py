from screens import StartMenu, \
    LastTests, \
    HistoryTests, \
    RunTests, \
    SettingsNotion, \
    AdminMenu


def start(update, context):
    context.chat_data["user"] = update.message.chat.username
    if context.args and context.args[0] == 'admin':
        AdminMenu(update, context)  # TODO
    else:
        context.chat_data['reply'] = False
        StartMenu(update, context)
        context.chat_data['reply'] = True


def buttons(update, context):
    query = update.callback_query
    query.answer()
    if query.data == 'last_results':
        LastTests(update, context)
        StartMenu(update, context)
    elif query.data.startswith('tests'):
        pass  # TODO
    elif query.data == 'history':
        HistoryTests(update, context)
        StartMenu(update, context)
    elif query.data == 'run':
        RunTests(update, context)
        StartMenu(update, context)
    elif query.data == 'notifications':
        SettingsNotion(update, context)
        StartMenu(update, context)
    else:
        pass


def input_text(update, context):
    if context.chat_data['screen'] == 'HistoryTests':
        HistoryTests(update, context)
        StartMenu(update, context)
    else:
        pass