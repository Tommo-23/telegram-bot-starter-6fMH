import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Token del bot
TOKEN = os.getenv("TOKEN")

# Canale di destinazione per l'inoltro dei messaggi
CHAT_DESTINAZIONE = "@TuttoModding"

# Canali da monitorare
CANALI_MONITORATI = {
    '@garnet_updates': 'rn13pro5g / PocoX6',
    '@PocoF6GlobalUpdate': 'POCO F6',
    '@Redmi10CUpdates': 'Redmi 10c',
    '@setupTommo23': 'test',
}

async def start(update: Update, context: CallbackContext) -> None:
    """Risponde al comando /start."""
    await update.message.reply_text('my job is to forward the new roms of your device.')

async def inoltra_messaggio(update: Update, context: CallbackContext) -> None:
    """Inoltra il messaggio se proviene da un canale monitorato."""
    if update.message and update.message.chat.username in CANALI_MONITORATI:
        await update.message.forward(chat_id=CHAT_DESTINAZIONE)
    else:
        print("L'aggiornamento ricevuto non proviene da un canale monitorato.")

def main() -> None:
    # Configura l'applicazione
    application = Application.builder().token(TOKEN).build()

    # Aggiungi i gestori di comandi e messaggi
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.ChatType.CHANNEL, inoltra_messaggio))

    # Usa il metodo di esecuzione a seconda delle necessità
    if os.getenv("USE_WEBHOOK") == "True":
        # Configura i Webhook
        application.run_webhook(
            listen="0.0.0.0",
            port=int(os.environ.get("PORT", 8443)),
            url_path=TOKEN,
            webhook_url=f"https://{os.getenv('telegram-bot-starter-production-f0c4.up.railway.app')}/{7514576903:AAH9eTd__xqhey_jnzwP1pLl0DTYgtckODw}",
        )
    else:
        # Usa il Polling
        application.run_polling()

if __name__ == '__main__':
    main()
