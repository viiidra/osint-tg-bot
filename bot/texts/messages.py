search_message = ('This bot can help you find information about a person using open sources.\n'
                  'The search can be carried out by:\n'
                  '✅  last name, first name and patronymic\n'
                  '✅  last and first name\n'
                  '✅  last name\n'
                  '✅  nickname\n')

help_message = ("To successfully search, you need to execute the /search command, "
                "and then choose the query format from the list, which you will be writing. "
                "Send the bot a query in the expected format. In the message that appears, click the \"OK\" button. "
                "That's it, wait for the bot to send you a ready report with the search results 🎉")

about_message = ("This bot was developed as a bachelor's diploma work by Karyna Barkar, "
                 "a 4th year student at the National University \"Odessa Polytechnic\"")

support_message = "For any questions or wishes, please contact the bot administrator: @kbarkar"

admin_welcome_message = ("You are admin!\n"
                         "Available commands:\n"
                         "/admin - this help\n"
                         "/ban - ban user(s) permanently.\n"
                         "<i>Usage:</i> <b>/ban tg_id</b> <i>or</i> <b>/ban tg_id1 tg_id2</b>...\n"
                         "/tban - ban user for a time.\n"
                         "<i>Usage:</i> <b>/ban tg_id 1w</b>\n"
                         "[10m | 2h | 5d | 3w]\n"
                         "/unban - unban user(s).\n"
                         "<i>Usage:</i> <b>/unban tg_id</b> <i>or</i> <b>/unban tg_id1 tg_id2</b>... "
                         "<i>or</i> <b>/unban</b> to unban all users\n"
                         "/isbanned - Check if user is banned.\n"
                         "<i>Usage:</i> <b>/isbanned tg_id</b>\n"
                         "/banlist - List of banned users \n"
                         "<i>Usage:</i> <b>/banlist [records]</b> - List of last N records <i>or</i> <b>/banlist</b> \n"
                         "/stat - display users requsts statistics\n"
                         "<i>Usage:</i> <b>/stat [records]</b> - List of last N records <i>or</i> <b>/stat</b> \n"
                         "/requests - display last users requsts\n"
                         "<i>Usage:</i> <b>/requests [records]</b> - List of last N requests <i>or</i> "
                         "<b>/requests</b> \n")

admin_wrong_message = "⚠️ Something went wrong. Use /admin command for help."

no_results_message = "🤷No results found"

banned_message = "⚠️ Sorry, You can't use Bot! You are banned❗ ⚠️"

unsupported_content_message = '🤷 Unsupported message content!'

search_canceled_message = ("OK, let's start again...\n"
                           "Use /search command to search for information "
                           "about a person using open sources.\n")

search_types = {
    'flp_name': 'last name, first name and patronymic',
    'fl_name': 'last and first name',
    'last_name': 'last name',
    'nickname': 'nickname',
}
