import os
import json
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Load configuration
with open('config.json', 'r') as f:
    config = json.load(f)

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Bot token from environment variable for security
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', config.get('bot_token', ''))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message when the command /start is issued."""
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
    
    # Send logo from URL
    try:
        await update.message.reply_photo(
            photo="https://i.ibb.co/rRypQ9tX/1001113489.jpg",
            caption=welcome_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    except Exception as e:
        logging.error(f"Error sending photo: {e}")
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def website(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Direct command to open website."""
    keyboard = [[InlineKeyboardButton("🌐 Visit Official Website", url=config['website'])]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "**Official MineChain Portal**\n\n"
        "Access our comprehensive platform for token management, "
        "ecosystem features, and project documentation.",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show current token price information."""
    keyboard = [
        [InlineKeyboardButton("📈 Live Chart", url=config['chart_url'])],
        [InlineKeyboardButton("🔄 Refresh Price", callback_data="refresh_price")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "💰 **MC Token Economics**\n\n"
        "• Current Price: --\n"
        "• Market Cap: --\n"
        "• 24h Volume: --\n"
        "• Price Change (24h): --\n\n"
        "*Real-time pricing integration coming soon*",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def contract(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display token contract address."""
    contract_address = config['token_address']
    
    keyboard = [
        [InlineKeyboardButton("🔍 View on Explorer", url=f"{config['explorer_url']}{contract_address}")],
        [InlineKeyboardButton("📋 Copy Address", callback_data="copy_contract")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "📝 **Official Contract Address**\n\n"
        f"`{contract_address}`\n\n"
        "*Always verify contract addresses from official sources.*",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display information about MineChain."""
    about_text = (
        "🏔️ **About MineChain**\n\n"
        "MineChain represents the evolution of digital assets for creators and visionaries. "
        "Our ecosystem combines sophisticated tokenomics with enterprise-grade security.\n\n"
        "**Key Features:**\n"
        "• Advanced token mechanics\n"
        "• Anti-whale protection\n"
        "• Secure Web3 infrastructure\n"
        "• Creator-focused utilities\n\n"
        "Built by **ARZIA** - delivering excellence in blockchain technology."
    )
    
    keyboard = [
        [InlineKeyboardButton("📚 Documentation", url=config.get('docs_url', config['website']))],
        [InlineKeyboardButton("🏢 ARZIA", url=config.get('arzia_url', config['website']))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(about_text, reply_markup=reply_markup, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send help message."""
    help_text = (
        "🛠 **MineChain Bot Assistance**\n\n"
        "**Available Commands:**\n"
        "/start - Launch the MineChain experience\n"
        "/website - Access our official platform\n"
        "/price - View token economics\n"
        "/contract - Retrieve contract address\n"
        "/about - Learn about our ecosystem\n"
        "/help - Display this guidance\n\n"
        "For technical support, contact our development team."
    )
    
    keyboard = [[InlineKeyboardButton("🚀 Get Started", callback_data="start_over")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(help_text, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "website":
        keyboard = [[InlineKeyboardButton("🌐 Visit Website", url=config['website'])]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="**Official MineChain Platform**\n\nAccess our comprehensive ecosystem and tools.",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    elif data == "price":
        keyboard = [
            [InlineKeyboardButton("📈 Live Chart", url=config['chart_url'])],
            [InlineKeyboardButton("🔄 Refresh", callback_data="refresh_price")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="💰 **Token Economics**\n\n*Price tracking integration in development*",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    elif data == "contract":
        contract_address = config['token_address']
        keyboard = [
            [InlineKeyboardButton("🔍 View on Explorer", url=f"{config['explorer_url']}{contract_address}")],
            [InlineKeyboardButton("📋 Copy", callback_data="copy_contract")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=f"📝 **Contract Address**\n\n`{contract_address}`",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    elif data == "about":
        about_text = (
            "🏔️ **MineChain Ecosystem**\n\n"
            "Sophisticated digital assets for the modern creator.\n\n"
            "Built with precision by ARZIA."
        )
        keyboard = [[InlineKeyboardButton("📚 Learn More", url=config['website'])]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=about_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    elif data in ["refresh_price", "copy_contract", "start_over"]:
        # Placeholder for future functionality
        await query.answer("Feature coming soon! ✅")

def main():
    """Start the bot."""
    if not BOT_TOKEN:
        logging.error("No bot token found! Set TELEGRAM_BOT_TOKEN environment variable.")
        return
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("website", website))
    application.add_handler(CommandHandler("price", price))
    application.add_handler(CommandHandler("contract", contract))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(handle_button_click))
    
    # Start bot
    logging.info("MineChain bot starting...")
    application.run_polling()

if __name__ == '__main__':
    main()