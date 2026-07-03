import os
import logging
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, ConversationHandler

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# States
CATEGORY = 1
WAITING_FOR_INPUT = 2

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Realistic", callback_data='Realistic')],
        [InlineKeyboardButton("Anime", callback_data='Anime')],
        [InlineKeyboardButton("Product", callback_data='Product')],
        [InlineKeyboardButton("Food", callback_data='Food')],
        [InlineKeyboardButton("UGC", callback_data='UGC')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome to PromptForge! Please select a style:", reply_markup=reply_markup)
    return CATEGORY

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['style'] = query.data
    await query.edit_message_text(text=f"Selected: {query.data}. Now, tell me what you want to create:")
    return WAITING_FOR_INPUT

async def generate_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    style = context.user_data.get('style')
    
    # Simple logic for prompt generation
    prompt = f"Professional {style} image of {user_input}. Highly detailed, 8k resolution, trending on ArtStation."
    
    await update.message.reply_text(f"Here is your prompt:\n\n`{prompt}`", parse_mode='Markdown')
    return ConversationHandler.END

def main():
    application = Application.builder().token(TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CATEGORY: [CallbackQueryHandler(button)],
            WAITING_FOR_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, generate_prompt)],
        },
        fallbacks=[]
    )
    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == '__main__':
    main()
