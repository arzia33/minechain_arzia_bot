            import os
import json
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Enhanced logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

try:
    with open('config.json', 'r') as f:
        config = json.load(f)
except Exception as e:
    logger.error(f"Config loading failed: {e}")
    config = {}

# Bot token - check environment variable first
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not BOT_TOKEN:
    BOT_TOKEN = config.get('bot_token')
    if not BOT_TOKEN:
        logger.error("No bot token found in environment or config!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        welcome_text = (
            "🏔️ **Welcome to MineChain**\n\n"
            "The sophisticated digital asset ecosystem for creators and investors.\n\n"
            "*Professional | Secure | Innovative*\n\n"
            "Built by ARZIA with enterprise-grade Web3 technology."
        )
        
        keyboard = [
            [InlineKeyboardButton("🌐 Official Website", callback_data="website")],
            [InlineKeyboardButton("💰 Token Price", callback_data="price")],
            [InlineKeyboardButton("📝 Contract Address", callback_data="contract")],
            [InlineKeyboardButton("ℹ️ About MineChain", callback_data="about")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_photo(
            photo="https://i.ibb.co/rRypQ9tX/1001113489.jpg",
            caption=welcome_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"Start command error: {e}")
        await update.message.reply_text("Welcome to MineChain! Use /help for commands.")

# [Keep all your other command functions the same as before]
async def website(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🌐 Visit Official Website", url=config['website'])]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "**Official MineChain Portal**\n\nAccess our comprehensive platform.",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("📈 Live Chart", url=config['chart_url'])]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "💰 **MC Token Economics**\n\n*Price tracking coming soon*",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def contract(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contract_address = config['token_address']
    keyboard = [[InlineKeyboardButton("🔍 View on Explorer", url=f"{config['explorer_url']}{contract_address}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"📝 **Official Contract Address**\n\n`{contract_address}`",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    about_text = (
        "🏔️ **About MineChain**\n\n"
        "Sophisticated digital assets for creators and visionaries."
    )
    await update.message.reply_text(about_text, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🛠 **MineChain Bot Commands:**\n"
        "/start - Launch bot\n"
        "/website - Official website\n"
        "/price - Token economics\n"
        "/contract - Contract address\n"
        "/about - Project information\n"
        "/help - This message"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def handle_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data == "website":
            keyboard = [[InlineKeyboardButton("🌐 Visit Website", url=config['website'])]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                text="**Official MineChain Platform**",
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        # [Add other button handlers]
        
    except Exception as e:
        logger.error(f"Button handler error: {e}")

def main():
    if not BOT_TOKEN:
        logger.error("No bot token available!")
        return
    
    try:
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("website", website))
        application.add_handler(CommandHandler("price", price))
        application.add_handler(CommandHandler("contract", contract))
        application.add_handler(CommandHandler("about", about))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CallbackQueryHandler(handle_button_click))
        
        logger.info("MineChain bot starting...")
        application.run_polling()
        
    except Exception as e:
        logger.error(f"Bot startup failed: {e}")

if __name__ == '__main__':
    main()
