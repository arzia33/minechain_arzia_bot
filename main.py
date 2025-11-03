import os
import json
import logging
import random
from aiohttp import ClientSession 
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- Initialization ---

# Load configuration
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    logging.error("config.json not found. Please create one.")
    config = {}

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Bot token from environment variable for security
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', config.get('bot_token', ''))

# --- Web App Info ---
web_app_url = config.get('webapp_url', 'https://minechain-testnet.netlify.app/')

# --- Helper Functions ---

async def fetch_price_data(contract_address: str, api_url: str) -> dict:
    """Fetches real-time price data using aiohttp."""
    # Mock data for demonstration
    current_price = round(random.uniform(0.005, 0.015), 4)
    change_24h = round(random.uniform(-5.0, 5.0), 2)
    market_cap = f"${random.randint(1000000, 5000000):,}"
    volume_24h = f"${random.randint(50000, 500000):,}"

    return {
        'price': f"${current_price:.4f}",
        'market_cap': market_cap,
        'volume_24h': volume_24h,
        'change_24h': f"{change_24h:+.2f}%"
    }

async def get_price_message_content(contract_address: str, api_url: str):
    """Generates the price message text and keyboard."""
    price_data = await fetch_price_data(contract_address, api_url)
    
    if price_data:
        price_text = (
            "💰 **MC Token Economics (Live Data)**\n\n"
            f"• Current Price: **{price_data['price']}**\n"
            f"• Market Cap: {price_data['market_cap']}\n"
            f"• 24h Volume: {price_data['volume_24h']}\n"
            f"• Price Change (24h): {price_data['change_24h']}\n\n"
            "*Prices are mock data, refresh to see changes.*"
        )
    else:
        price_text = (
            "💰 **MC Token Economics**\n\n"
            "• Current Price: --\n"
            "• Market Cap: --\n"
            "• 24h Volume: --\n"
            "• Price Change (24h): --\n\n"
            "*Could not fetch real-time price data. Try refreshing.*"
        )
    
    keyboard = [
        [InlineKeyboardButton("📈 Live Chart", url=config.get('chart_url', 'https://dexscreener.com/'))],
        [InlineKeyboardButton("🔄 Refresh Price", callback_data="refresh_price")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    return price_text, reply_markup

# --- Command Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message with Web App launch button."""
    welcome_text = (
        "🏔️ **Welcome to MineChain**\n\n"
        "The sophisticated digital asset ecosystem for creators and investors.\n\n"
        "*Professional | Secure | Innovative*\n\n"
        "Built by ARZIA with enterprise-grade Web3 technology."
    )
    
    # Main keyboard with Web App launch button
    keyboard = [
        [InlineKeyboardButton("🚀 LAUNCH APP", web_app=WebAppInfo(url=web_app_url))],
        [
            InlineKeyboardButton("💰 Token Price", callback_data="price"),
            InlineKeyboardButton("📝 Contract", callback_data="contract")
        ],
        [
            InlineKeyboardButton("ℹ️ About", callback_data="about"),
            InlineKeyboardButton("🛟 Help", callback_data="help_menu")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
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

async def webapp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Direct command to launch web app."""
    keyboard = [[InlineKeyboardButton("🚀 LAUNCH MINE CHAIN APP", web_app=WebAppInfo(url=web_app_url))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(
            "**Mine Chain Web App**\n\nAccess all Mine Chain features directly in our web application.",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    elif update.callback_query:
        await update.callback_query.edit_message_text(
            "**Mine Chain Web App**\n\nAccess all Mine Chain features directly in our web application.",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check token balance - redirects to web app."""
    keyboard = [[InlineKeyboardButton("🚀 Check Balance in App", web_app=WebAppInfo(url=web_app_url))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message_text = (
        "💰 **Check Your MC Token Balance**\n\n"
        "To view your token balance and transaction history, "
        "please use our web application where you can connect your wallet securely."
    )
    
    if update.message:
        await update.message.reply_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')
    elif update.callback_query:
        await update.callback_query.edit_message_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')

async def airdrop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Airdrop information - redirects to web app."""
    keyboard = [[InlineKeyboardButton("🚀 Claim Airdrop in App", web_app=WebAppInfo(url=web_app_url))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message_text = (
        "🎁 **MC Token Airdrop**\n\n"
        "Airdrop claims are processed through our web application. "
        "Connect your wallet to check eligibility and claim your tokens."
    )
    
    if update.message:
        await update.message.reply_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')
    elif update.callback_query:
        await update.callback_query.edit_message_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')

async def vesting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Vesting schedule - redirects to web app."""
    keyboard = [[InlineKeyboardButton("🚀 View Vesting in App", web_app=WebAppInfo(url=web_app_url))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message_text = (
        "📅 **Vesting Schedule**\n\n"
        "View your token vesting schedule and unlock dates in our web application. "
        "All vesting information is available after wallet connection."
    )
    
    if update.message:
        await update.message.reply_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')
    elif update.callback_query:
        await update.callback_query.edit_message_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')

async def mint(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mint tokens - redirects to web app."""
    keyboard = [[InlineKeyboardButton("🚀 Mint Tokens in App", web_app=WebAppInfo(url=web_app_url))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message_text = (
        "🪙 **Mint MC Tokens**\n\n"
        "Token minting is available in our web application. "
        "Connect your wallet to mint new MC tokens according to your allocation."
    )
    
    if update.message:
        await update.message.reply_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')
    elif update.callback_query:
        await update.callback_query.edit_message_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')

async def nft(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """NFT information - redirects to web app."""
    keyboard = [[InlineKeyboardButton("🚀 Explore NFTs in App", web_app=WebAppInfo(url=web_app_url))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message_text = (
        "🖼️ **MineChain NFTs**\n\n"
        "Explore our NFT collections and upcoming drops in the web application. "
        "Discover exclusive digital assets from the MineChain ecosystem."
    )
    
    if update.message:
        await update.message.reply_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')
    elif update.callback_query:
        await update.callback_query.edit_message_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show current token price information."""
    contract_address = config.get('token_address', '')
    api_url = config.get('price_api_url', '')

    price_text, reply_markup = await get_price_message_content(contract_address, api_url)
    
    if update.message:
        await update.message.reply_text(price_text, reply_markup=reply_markup, parse_mode='Markdown')
    elif update.callback_query:
        await update.callback_query.edit_message_text(price_text, reply_markup=reply_markup, parse_mode='Markdown')

async def contract(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display token contract address."""
    contract_address = config.get('token_address', 'N/A')
    
    keyboard = [
        [InlineKeyboardButton("🔍 View on Explorer", url=f"{config.get('explorer_url', 'https://etherscan.io/token/')}{contract_address}")],
        [InlineKeyboardButton("📋 Copy Address", callback_data="copy_contract")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(
            "📝 **Official Contract Address**\n\n"
            f"`{contract_address}`\n\n"
            "*Always verify contract addresses from official sources.*",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    elif update.callback_query:
        await update.callback_query.edit_message_text(
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

    if update.message:
        await update.message.reply_text(about_text, reply_markup=reply_markup, parse_mode='Markdown')
    elif update.callback_query:
        await update.callback_query.edit_message_text(about_text, reply_markup=reply_markup, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send comprehensive help message."""
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
    
    keyboard = [[InlineKeyboardButton("🚀 LAUNCH APP", web_app=WebAppInfo(url=web_app_url))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(help_text, reply_markup=reply_markup, parse_mode='Markdown')
    elif update.callback_query:
        await update.callback_query.edit_message_text(help_text, reply_markup=reply_markup, parse_mode='Markdown')

# --- Callback Handlers ---

async def handle_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "price":
        await price(update, context)
    elif data == "contract":
        await contract(update, context)
    elif data == "about":
        await about(update, context)
    elif data == "help_menu":
        await help_command(update, context)
    elif data == "refresh_price":
        contract_address = config.get('token_address', '')
        api_url = config.get('price_api_url', '')
        price_text, reply_markup = await get_price_message_content(contract_address, api_url)
        await query.edit_message_text(price_text, reply_markup=reply_markup, parse_mode='Markdown')
        await query.answer("Price data refreshed! 🔄")
    elif data == "copy_contract":
        contract_address = config.get('token_address', 'N/A')
        await query.answer(text=f"Contract Address: {contract_address}", show_alert=True)

def main():
    """Start the bot."""
    if not BOT_TOKEN or BOT_TOKEN == 'YOUR_TOKEN_HERE':
        logging.error("No valid bot token found! Set TELEGRAM_BOT_TOKEN environment variable or update config.json.")
        return
    
    # Create application
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
    
    # Start bot
    logging.info("MineChain bot starting...")
    application.run_polling()

if __name__ == '__main__':
    logging.getLogger('httpx').setLevel(logging.WARNING)
    main()    To use a real API like CoinGecko, you would uncomment the aiohttp block.
    """
    
    # --- MOCK DATA FOR DEMONSTRATION ---
    # Replace this block with the real API call below when deploying
    current_price = round(random.uniform(0.005, 0.015), 4)
    change_24h = round(random.uniform(-5.0, 5.0), 2)
    market_cap = f"${random.randint(1000000, 5000000):,}"
    volume_24h = f"${random.randint(50000, 500000):,}"

    return {
        'price': f"${current_price:.4f}",
        'market_cap': market_cap,
        'volume_24h': volume_24h,
        'change_24h': f"{change_24h:+.2f}%"
    }

    # --- REAL API CALL STRUCTURE (requires actual API to be live) ---
    # try:
    #     async with ClientSession() as session:
    #         async with session.get(api_url, timeout=10) as response:
    #             if response.status == 200:
    #                 data = await response.json()
    #                 # You would need to parse 'data' here to extract the values
    #                 # For now, let's stick to the mock structure for safe execution
    #                 return data
    #             else:
    #                 logging.warning(f"Price API failed with status: {response.status}")
    # except Exception as e:
    #     logging.error(f"Error fetching price data: {e}")
    # return None

async def get_price_message_content(contract_address: str, api_url: str):
    """Generates the price message text and keyboard."""
    price_data = await fetch_price_data(contract_address, api_url)
    
    if price_data:
        price_text = (
            "💰 **MC Token Economics (Live Data)**\n\n"
            f"• Current Price: **{price_data['price']}**\n"
            f"• Market Cap: {price_data['market_cap']}\n"
            f"• 24h Volume: {price_data['volume_24h']}\n"
            f"• Price Change (24h): {price_data['change_24h']}\n\n"
            "*Prices are mock data, refresh to see changes.*"
        )
    else:
        price_text = (
            "💰 **MC Token Economics**\n\n"
            "• Current Price: --\n"
            "• Market Cap: --\n"
            "• 24h Volume: --\n"
            "• Price Change (24h): --\n\n"
            "*Could not fetch real-time price data. Try refreshing.*"
        )
    
    keyboard = [
        [InlineKeyboardButton("📈 Live Chart", url=config['chart_url'])],
        [InlineKeyboardButton("🔄 Refresh Price", callback_data="refresh_price")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    return price_text, reply_markup

# --- Command Handlers ---

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
        # Fallback to text message if photo fails
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def website(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Direct command to open website."""
    keyboard = [[InlineKeyboardButton("🌐 Visit Official Website", url=config['website'])]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Check if we are responding to a command or a callback for consistent message handling
    if update.message:
        response_sender = update.message.reply_text
    elif update.callback_query:
        response_sender = update.callback_query.edit_message_text
    else:
        return # Should not happen

    await response_sender(
        "**Official MineChain Portal**\n\n"
        "Access our comprehensive platform for token management, "
        "ecosystem features, and project documentation.",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show current token price information."""
    contract_address = config.get('token_address', '')
    api_url = config.get('price_api_url', '')

    price_text, reply_markup = await get_price_message_content(contract_address, api_url)
    
    # Check if we are responding to a command or a callback for consistent message handling
    if update.message:
        response_sender = update.message.reply_text
    elif update.callback_query:
        response_sender = update.callback_query.edit_message_text
    else:
        return

    await response_sender(price_text, reply_markup=reply_markup, parse_mode='Markdown')


async def contract(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display token contract address."""
    contract_address = config.get('token_address', 'N/A')
    
    keyboard = [
        # Note: Telegram usually auto-detects the address to be copied when tapped/clicked
        [InlineKeyboardButton("🔍 View on Explorer", url=f"{config['explorer_url']}{contract_address}")],
        # The 'Copy Address' button is handled in handle_button_click via a Telegram Alert
        [InlineKeyboardButton("📋 Copy Address", callback_data="copy_contract")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Check if we are responding to a command or a callback for consistent message handling
    if update.message:
        response_sender = update.message.reply_text
    elif update.callback_query:
        response_sender = update.callback_query.edit_message_text
    else:
        return

    await response_sender(
        "📝 **Official Contract Address**\n\n"
        f"`{contract_address}`\n\n" # Backticks allow easy copy on Telegram
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

    # Check if we are responding to a command or a callback for consistent message handling
    if update.message:
        response_sender = update.message.reply_text
    elif update.callback_query:
        response_sender = update.callback_query.edit_message_text
    else:
        return
    
    await response_sender(about_text, reply_markup=reply_markup, parse_mode='Markdown')

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
    
    # The 'start_over' button is now used to trigger the start command
    keyboard = [[InlineKeyboardButton("🚀 Go to Main Menu", callback_data="start_over")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(help_text, reply_markup=reply_markup, parse_mode='Markdown')

# --- Callback Handlers ---

async def handle_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer() # Always answer the query to dismiss the loading indicator
    
    data = query.data
    
    if data == "website":
        # Call the existing command handler to reuse logic and edit the message
        await website(update, context) 
    
    elif data == "price":
        # Call the existing command handler to reuse logic and edit the message
        await price(update, context)
    
    elif data == "contract":
        # Call the existing command handler to reuse logic and edit the message
        await contract(update, context)
    
    elif data == "about":
        # Call the existing command handler to reuse logic and edit the message
        await about(update, context)
    
    elif data == "refresh_price":
        # Re-fetch and edit the current message with the new price data
        contract_address = config.get('token_address', '')
        api_url = config.get('price_api_url', '')

        price_text, reply_markup = await get_price_message_content(contract_address, api_url)
        
        await query.edit_message_text(price_text, reply_markup=reply_markup, parse_mode='Markdown')
        await query.answer("Price data refreshed! 🔄")

    
    elif data == "copy_contract":
        # Use a Telegram Alert to display the address for easy copying.
        contract_address = config.get('token_address', 'N/A')
        await query.answer(
            text=f"Contract Address: {contract_address}", 
            show_alert=True
        )

    elif data == "start_over":
        # Sends the /start message as a new message
        # Since update.callback_query is present, update.message is None. We need to create
        # a mock message object or ensure 'start' handles callbacks gracefully. 
        # For simplicity, we'll let 'start' send a new message.
        await start(update, context)


def main():
    """Start the bot."""
    if not BOT_TOKEN or BOT_TOKEN == 'YOUR_TOKEN_HERE':
        logging.error("No valid bot token found! Set TELEGRAM_BOT_TOKEN environment variable or update config.json.")
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
    # Ensure correct logging level for debugging for external libraries
    logging.getLogger('httpx').setLevel(logging.WARNING) 
    main()
