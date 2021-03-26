from screens import StartMenu, \
    LastTests, \
    StatusPipeline, \
    RunTests, \
    SettingsNotion, \
    AdminMenu, \
    MainScreen


def start(update, context):
    context.chat_data['user'] = update.message.chat.username
    context.chat_data['reply'] = False
    context.chat_data['screen'] = ''
    if context.args and context.args[0] == 'admin':
        AdminMenu(update, context)  # TODO
    else:
        StartMenu(update, context)
    context.chat_data['reply'] = True


def buttons(update, context):
    query = update.callback_query
    query.answer()
    screen = MainScreen(update, context)
    if query.data == 'last_results_tests':
        LastTests(update, context)
        StartMenu(update, context)
    elif query.data == 'status_pipeline_tests':
        StatusPipeline(update, context)
        StartMenu(update, context)
    elif query.data == 'delete_pipeline_tests':
        screen.DeletePipeline()
        StartMenu(update, context)
    elif query.data == 'run_tests':
        RunTests(update, context)
        StartMenu(update, context)
    elif query.data == 'notifications':
        SettingsNotion(update, context)
        StartMenu(update, context)
    else:
        pass


def input_text(update, context):
    if context.chat_data['screen'] == 'StatusPipeline':
        StatusPipeline(update, context)
        StartMenu(update, context)
    else:
        pass