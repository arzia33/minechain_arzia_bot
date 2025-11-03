import os
import json
import logging
import random
from aiohttp import ClientSession 
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- Initialization ---

try:
    with open('config.json', 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    logging.error("config.json not found.")
    config = {}

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', config.get('bot_token', ''))

# --- Web App Configuration ---
WEB_APP_URL = "https://minechain-testnet.netlify.app/"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message with Web App launch button."""
    welcome_text = (
        "🏔️ **Welcome to MineChain**\n\n"
        "The sophisticated digital asset ecosystem for creators and investors.\n\n"
        "*Professional | Secure | Innovative*\n\n"
        "Built by ARZIA with enterprise-grade Web3 technology."
    )
    
    # Main keyboard with Web App launch as primary button
    keyboard = [
        [InlineKeyboardButton("🚀 LAUNCH MINE CHAIN APP", web_app=WebAppInfo(url=WEB_APP_URL))],
        [
            InlineKeyboardButton("💰 Token Price", callback_data="price"),
            InlineKeyboardButton("📝 Contract", callback_data="contract")
        ],
        [
            InlineKeyboardButton("ℹ️ About", callback_data="about"),
            InlineKeyboardButton("🛟 Help", callback_data="help")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        if update.message:
            await update.message.reply_photo(
                photo="https://i.ibb.co/rRypQ9tX/1001113489.jpg",
                caption=welcome_text,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        else:
            await update.callback_query.edit_message_caption(
                caption=welcome_text,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
    except Exception as e:
        logging.error(f"Error with photo: {e}")
        if update.message:
            await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
        else:
            await update.callback_query.edit_message_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def webapp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Direct command to launch web app."""
    keyboard = [[InlineKeyboardButton("🚀 LAUNCH MINE CHAIN APP", web_app=WebAppInfo(url=WEB_APP_URL))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message_text = "**Mine Chain Web App**\n\nAccess all Mine Chain features directly in our web application."
    
    if update.message:
        await update.message.reply_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update.callback_query.edit_message_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check token balance."""
    keyboard = [
        [InlineKeyboardButton("🚀 Check Balance in App", web_app=WebAppInfo(url=WEB_APP_URL))],
        [InlineKeyboardButton("🔙 Main Menu", callback_data="start")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message_text = (
        "💰 **Check Your MC Token Balance**\n\n"
        "To view your token balance and transaction history, "
        "please use our web application where you can connect your wallet securely."
    )
    
    if update.message:
        await update.message.reply_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update.callback_query.edit_message_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')

async def airdrop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Airdrop information."""
    keyboard = [
        [InlineKeyboardButton("🚀 Claim Airdrop in App", web_app=WebAppInfo(url=WEB_APP_URL))],
        [InlineKeyboardButton("🔙 Main Menu", callback_data="start")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message_text = (
        "🎁 **MC Token Airdrop**\n\n"
        "Airdrop claims are processed through our web application. "
        "Connect your wallet to check eligibility and claim your tokens."
    )
    
    if update.message:
        await update.message.reply_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update.callback_query.edit_message_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')

async def vesting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Vesting schedule."""
    keyboard = [
        [InlineKeyboardButton("🚀 View Vesting in App", web_app=WebAppInfo(url=WEB_APP_URL))],
        [InlineKeyboardButton("🔙 Main Menu", callback_data="start")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message_text = (
        "📅 **Vesting Schedule**\n\n"
        "View your token vesting schedule and unlock dates in our web application. "
        "All vesting information is available after wallet connection."
    )
    
    if update.message:
        await update.message.reply_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update.callback_query.edit_message_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')

async def mint(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mint tokens."""
    keyboard = [
        [InlineKeyboardButton("🚀 Mint Tokens in App", web_app=WebAppInfo(url=WEB_APP_URL))],
        [InlineKeyboardButton("🔙 Main Menu", callback_data="start")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message_text = (
        "🪙 **Mint MC Tokens**\n\n"
        "Token minting is available in our web application. "
        "Connect your wallet to mint new MC tokens according to your allocation."
    )
    
    if update.message:
        await update.message.reply_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update.callback_query.edit_message_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')

async def nft(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """NFT information."""
    keyboard = [
        [InlineKeyboardButton("🚀 Explore NFTs in App", web_app=WebAppInfo(url=WEB_APP_URL))],
        [InlineKeyboardButton("🔙 Main Menu", callback_data="start")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message_text = (
        "🖼️ **MineChain NFTs**\n\n"
        "Explore our NFT collections and upcoming drops in the web application. "
        "Discover exclusive digital assets from the MineChain ecosystem."
    )
    
    if update.message:
        await update.message.reply_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update.callback_query.edit_message_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show current token price information."""
    current_price = round(random.uniform(0.005, 0.015), 4)
    change_24h = round(random.uniform(-5.0, 5.0), 2)
    
    price_text = (
        "💰 **MC Token Economics**\n\n"
        f"• Current Price: **${current_price:.4f}**\n"
        f"• Market Cap: ${random.randint(1000000, 5000000):,}\n"
        f"• 24h Volume: ${random.randint(50000, 500000):,}\n"
        f"• Price Change (24h): {change_24h:+.2f}%\n\n"
        "*Using mock data for demonstration*"
    )
    
    keyboard = [
        [InlineKeyboardButton("📈 Live Chart", url="https://dexscreener.com/")],
        [InlineKeyboardButton("🔄 Refresh Price", callback_data="refresh_price")],
        [InlineKeyboardButton("🔙 Main Menu", callback_data="start")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(price_text, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update.callback_query.edit_message_text(price_text, reply_markup=reply_markup, parse_mode='Markdown')

async def contract(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display token contract address."""
    contract_address = config.get('token_address', '0x76589d79bdbca32b82d9391d5fbb9f199d2af6fa')
    
    keyboard = [
        [InlineKeyboardButton("🔍 View on Explorer", url=f"https://etherscan.io/token/{contract_address}")],
        [InlineKeyboardButton("📋 Copy Address", callback_data="copy_contract")],
        [InlineKeyboardButton("🔙 Main Menu", callback_data="start")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message_text = (
        "📝 **Official Contract Address**\n\n"
        f"`{contract_address}`\n\n"
        "*Always verify contract addresses from official sources.*"
    )
    
    if update.message:
        await update.message.reply_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update.callback_query.edit_message_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')

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
        [InlineKeyboardButton("📚 Documentation", url="https://minechain-testnet.netlify.app/docs")],
        [InlineKeyboardButton("🔙 Main Menu", callback_data="start")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(about_text, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update.callback_query.edit_message_text(about_text, reply_markup=reply_markup, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send help message."""
    help_text = (
        "🛠 **MineChain Bot Assistance**\n\n"
        "**Available Commands:**\n"
        "/start - Launch the MineChain experience\n"
        "/balance - Check your MC token balance\n"
        "/airdrop - Claim airdrop (if available)\n"
        "/vesting - View your vesting schedule\n"
        "/webapp - Open the Mine Chain Web App\n"
        "/mint - Learn how to mint new tokens\n"
        "/nft - Explore upcoming NFT drops\n"
        "/price - View token economics\n"
        "/contract - Retrieve contract address\n"
        "/about - Learn about our ecosystem\n"
        "/help - Display this guidance\n\n"
        "For technical support, contact our development team."
    )
    
    keyboard = [
        [InlineKeyboardButton("🚀 LAUNCH APP", web_app=WebAppInfo(url=WEB_APP_URL))],
        [InlineKeyboardButton("🔙 Main Menu", callback_data="start")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(help_text, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update.callback_query.edit_message_text(help_text, reply_markup=reply_markup, parse_mode='Markdown')

# --- Callback Handlers ---

async def handle_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "start":
        await start(update, context)
    elif data == "price":
        await price(update, context)
    elif data == "contract":
        await contract(update, context)
    elif data == "about":
        await about(update, context)
    elif data == "help":
        await help_command(update, context)
    elif data == "refresh_price":
        await price(update, context)
        await query.answer("Price refreshed! 🔄")
    elif data == "copy_contract":
        contract_address = config.get('token_address', '0x76589d79bdbca32b82d9391d5fbb9f199d2af6fa')
        await query.answer(text=f"Contract Address: {contract_address}", show_alert=True)

def main():
    """Start the bot."""
    if not BOT_TOKEN:
        logging.error("No valid bot token found!")
        return
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("webapp", webapp))
    application.add_handler(CommandHandler("balance", balance))
    application.add_handler(CommandHandler("airdrop", airdrop))
    application.add_handler(CommandHandler("vesting", vesting))
    application.add_handler(CommandHandler("mint", mint))
    application.add_handler(CommandHandler("nft", nft))
    application.add_handler(CommandHandler("price", price))
    application.add_handler(CommandHandler("contract", contract))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CommandHandler("help", help_command))
    
    # Add callback handler
    application.add_handler(CallbackQueryHandler(handle_button_click))
    
    logging.info("MineChain bot starting...")
    application.run_polling()

if __name__ == '__main__':
    logging.getLogger('httpx').setLevel(logging.WARNING)
    main()
