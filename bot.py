import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from telegram.error import NetworkError

TOKEN = os.getenv("TOKEN")

CHAT_DESTINAZIONE = "@TuttoModding"  # Canale di destinazione

CANALI_MONITORATI = {
    '@garnet_updates': 'rn13pro5g / PocoX6',
    '@PocoF6GlobalUpdate': 'POCO F6',
    '@Redmi10CUpdates': 'Redmi 10c',    
    '@setupTommo23': 'test',    
}

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('my job is to forward the new roms of your device.')

async def inoltra_messaggio(update: Update, context: CallbackContext) -> None:
    if update.message and update.message.chat.username in CANALI_MONITORATI:
        try:
            await update.message.forward(chat_id=CHAT_DESTINAZIONE)
        except NetworkError as e:
            print(f"Network error occurred: {e}. Retrying in 5 seconds...")
            await asyncio.sleep(5)
            await update.message.forward(chat_id=CHAT_DESTINAZIONE)
    else:
        print("L'aggiornamento ricevuto non proviene da un canale monitorato.")

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.ChatType.CHANNEL, inoltra_messaggio))

    application.run_polling()

if __name__ == '__main__':
    main()
