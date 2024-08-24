import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

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
    if update.message:
        chat = update.message.chat
        print(f"Chat ID: {chat.id}")
        print(f"Chat Username: {chat.username}")
        print(f"Chat Type: {chat.type}")
        print(f"Chat Title: {chat.title}")
        
        if chat.type == "channel" and chat.username in CANALI_MONITORATI:
            await update.message.forward(chat_id=CHAT_DESTINAZIONE)
        else:
            print(f"Il canale {chat.username} non è monitorato o non è un canale valido.")
    else:
        print("L'aggiornamento ricevuto non contiene un messaggio valido.")

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.ChatType.CHANNEL, inoltra_messaggio))

    application.run_polling()

if __name__ == '__main__':
    main()
