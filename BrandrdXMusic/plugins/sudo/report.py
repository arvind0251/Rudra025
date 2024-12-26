from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os
import logging

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

group_reports = {}

def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message when the /start command is issued."""
    update.message.reply_text('Welcome to the bot! Use /report to fetch group member details.')

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a help message when the /help command is issued."""
    update.message.reply_text('Available commands:\n/start - Welcome message\n/help - List of commands\n/report - Get group member details')

def report(update: Update, context: CallbackContext) -> None:
    """Fetch and log group members' IDs and names."""
    if update.message.chat.type not in ['group', 'supergroup']:
        update.message.reply_text("This command can only be used in groups.")
        return

    chat = update.message.chat
    members = context.bot.get_chat_administrators(chat.id)
    report_data = "Group Members in {}:\n".format(chat.title)

    for member in members:
        user = member.user
        report_data += f"ID: {user.id}, Name: {user.full_name}\n"

    # Save report
    group_reports[chat.id] = report_data

    with open(f"group_report_{chat.id}.txt", "w") as file:
        file.write(report_data)

    update.message.reply_text("Group member report generated and saved.")
    logger.info("Report generated for group: %s", chat.title)

def main():
    """Start the bot."""
    # Get the token from environment variable
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

    if not TOKEN:
        raise ValueError("Please set the TELEGRAM_BOT_TOKEN environment variable.")

    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(CommandHandler('report', report))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a signal to stop
    updater.idle()

if __name__ == '__main__':
    main()
