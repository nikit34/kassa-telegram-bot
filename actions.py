from screens import StartMenu, MainScreen


def start(update, context):
    context.chat_data['user'] = update.message.chat.username
    context.chat_data['reply'] = False
    StartMenu(update, context)


def buttons(update, context):
    query = update.callback_query
    query.answer()
    context.chat_data['reply'] = True
    screen = MainScreen(update, context)
    if query.data == 'last_results_tests':
        screen.LastTests()
    elif query.data == 'run_tests':
        screen.RunTests()
    elif query.data == 'delete_pipeline_tests':
        screen.CancelPipeline()
    elif query.data == 'status_pipeline_tests':
        screen.StatusPipeline()
    elif query.data == 'enable_all_runners':
        screen.EnabledRunners()
    StartMenu(update, context)