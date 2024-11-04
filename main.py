from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import get_price
import asyncio

TOKEN: Final = "6404185152:AAFPv6gSrtGoLLNzJ_UIC6eL6WaEEFfggXk"
BOT_USERNAME: Final = "@crypticgen_bot"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hey there, Welcome! Use /price to get crypto prices.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('I can help you get cryptocurrency prices. Use /price to see available options.')

async def price_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text('Please specify a cryptocurrency symbol (e.g., /price btc)')
        return

    symbol = context.args[0].upper() + 'USDT'
    if symbol not in get_price.latest_prices:
        await update.message.reply_text(f"Sorry, I don't have price information for {symbol}")
        return

    message = await update.message.reply_text(f"Fetching live price for {symbol}...")
    
    update_interval = 5  # Update every 5 seconds
    
    try:
        while True:
            price = float(get_price.latest_prices.get(symbol, 0))
            if price == 0:
                await context.bot.edit_message_text(
                    chat_id=update.effective_chat.id,
                    message_id=message.message_id,
                    text=f"Waiting for price data for {symbol}..."
                )
            else:
                await context.bot.edit_message_text(
                    chat_id=update.effective_chat.id,
                    message_id=message.message_id,
                    text=f"The current price of {symbol} is: ${price:.2f}\nUpdating every {update_interval} seconds. Send any command to stop."
                )
            await asyncio.sleep(update_interval)
    except asyncio.CancelledError:
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=message.message_id,
            text=f"Price updates for {symbol} have been stopped."
        )
    except Exception as e:
        print(f"Error updating price: {e}")
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=message.message_id,
            text=f"An error occurred while updating the price for {symbol}. Please try again later."
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Cancel any ongoing price update tasks
    for task in context.chat_data.get('price_tasks', []):
        task.cancel()
    context.chat_data['price_tasks'] = []

    message_type: str = update.message.chat.type
    text: str = update.message.text
    
    print(f'User ({update.message.chat.id}) in ({message_type}): "{text}"')
    
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
        
    print('BOT:', response)
    await update.message.reply_text(response)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    
    print(f'User ({update.message.chat.id}) in ({message_type}): "{text}"')
    
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
        
    print('BOT:', response)
    await update.message.reply_text(response)

def handle_response(text: str) -> str:
    processed: str = text.lower()
    
    if 'hello' in processed:
        return 'Yo Fam!'
    
    if 'how are you' in processed:
        return 'Im peachy, how about you?'
    
    return 'Come again?'

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == "__main__":
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()
    
    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('price', price_command))
    
    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    # Errors
    app.add_error_handler(error)
    
    # Start WebSocket connection
    symbols = ["BTCUSDT", "ETHUSDT", "DOGEUSDT", "BNBUSDT", "SOLUSDT"]  # Add more symbols as needed
    get_price.init_websocket(symbols)
    
    # Polls the Bot
    print("Polling...")
    app.run_polling(poll_interval=3)