from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os

# Replace with your actual Bot Token
TOKEN = os.environ.get("TOKEN") 
# Replace with your Group ID or your own User ID to receive the questions
ADMIN_GROUP_ID = os.environ.get("ADMIN_GROUP_ID") 


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Explains anonymity and builds trust."""
    welcome_text = (
        "👋 **Welcome to the Anonymous Questions Bot.**\n\n"
        "We are here to discuss **Imposter Syndrome and Guilt** safely. "
        "Your privacy is our priority:\n\n"
        "🔒 **Total Anonymity:** Your name and username are never shared with the group.\n"
        "📝 **How it works:** Simply type your question below.\n"
        "🚫 **No Logs:** This bot does not store your identity.\n\n"
        "Go ahead—what's on your mind?"
    )
    await update.message.reply_text(welcome_text, parse_mode='Markdown')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Intercepts the message and strips user data before sending to Admin."""
    if update.message.chat.type == 'private':
        # Send the question to the Admin Group/User
        # We manually build the message to ensure NO metadata from the user is attached
        await context.bot.send_message(
            chat_id=ADMIN_GROUP_ID,
            text=f"**New Anonymous Question:**\n\n{update.message.text}",
            parse_mode='Markdown'
        )

        # Friendly confirmation to the user
        await update.message.reply_text(
            "✅ Your message has been delivered anonymously. Thank you for sharing.",
            reply_markup=ReplyKeyboardRemove()
        )


if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    # Add the /start command handler
    app.add_handler(CommandHandler("start", start))

    # Add the message handler for text (ignoring commands)
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot is running... monitoring for anonymous questions.")
    app.run_polling()