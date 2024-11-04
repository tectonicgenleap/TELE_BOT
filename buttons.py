import logging
from typing import Final
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext

TOKEN: Final = "6404185152:AAFPv6gSrtGoLLNzJ_UIC6eL6WaEEFfggXk"
BOT_USERNAME: Final = "@crypticgen_bot"

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define conversation states
MAIN_MENU, GET_PRICE, ENTER_WALLET, SELECT_PAIR = range(4)

def fetch_crypto_price(token):
    #To insert pricefetch logic here
    return f"The current price of {token} is $XX,XXX.XX"

def swap_tokens(wallet, from_token, to_token):
    #To insert Swap logic here
    return f"Swapped {from_token} to {to_token} for wallet {wallet}"

async def start(update: Update, context: CallbackContext) -> int:
    """Send a message when the command /start is issued."""
    return await show_main_menu(update, context)

async def show_main_menu(update: Update, context: CallbackContext) -> int:
    """Display the main menu."""
    keyboard = [['Get Live Price', 'Swap Tokens']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        'Welcome to the Crypto Bot! Please choose an option:',
        reply_markup=reply_markup
    )
    return MAIN_MENU

async def main_menu(update: Update, context: CallbackContext) -> int:
    """Handle the main menu selection."""
    user_choice = update.message.text
    if user_choice == 'Get Live Price':
        keyboard = [['Back to Main Menu']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)
        await update.message.reply_text('Please enter the cryptocurrency token symbol (e.g., BTC, ETH) or go back to the main menu:', reply_markup=reply_markup)
        return GET_PRICE
    elif user_choice == 'Swap Tokens':
        await update.message.reply_text('Please enter your wallet address:')
        return ENTER_WALLET
    else:
        await update.message.reply_text('Invalid option. Please choose from the menu.')
        return MAIN_MENU

async def get_price(update: Update, context: CallbackContext) -> int:
    """Fetch and display the price for the specified token or return to main menu."""
    user_input = update.message.text
    if user_input == 'Back to Main Menu':
        return await show_main_menu(update, context)
    
    token = user_input.upper()
    price = fetch_crypto_price(token)
    await update.message.reply_text(price)
    # Stay in the GET_PRICE state
    return GET_PRICE

async def enter_wallet(update: Update, context: CallbackContext) -> int:
    """Process the entered wallet address and show swap pairs."""
    wallet = update.message.text
    context.user_data['wallet'] = wallet
    # Validate wallet address here if needed
    
    keyboard = [['ETH/USDT', 'BTC/USDT'], ['Back to Main Menu']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        f'Wallet address received: {wallet}\nPlease select a swap pair:',
        reply_markup=reply_markup
    )
    return SELECT_PAIR

async def select_pair(update: Update, context: CallbackContext) -> int:
    """Process the selected swap pair and perform the swap."""
    pair = update.message.text
    if pair == 'Back to Main Menu':
        return await show_main_menu(update, context)
    
    wallet = context.user_data.get('wallet', 'Unknown')
    from_token, to_token = pair.split('/')
    result = swap_tokens(wallet, from_token, to_token)
    await update.message.reply_text(result)
    return await show_main_menu(update, context)

async def cancel(update: Update, context: CallbackContext) -> int:
    """Cancel and end the conversation."""
    await update.message.reply_text('Operation cancelled. Type /start to begin again.')
    return ConversationHandler.END

if __name__ == "__main__":
    
    app = Application.builder().token('6404185152:AAFPv6gSrtGoLLNzJ_UIC6eL6WaEEFfggXk').build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MAIN_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, main_menu)],
            GET_PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_price)],
            ENTER_WALLET: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_wallet)],
            SELECT_PAIR: [MessageHandler(filters.TEXT & ~filters.COMMAND, select_pair)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    app.add_handler(conv_handler)

    # Start the Bot
    app.run_polling()
