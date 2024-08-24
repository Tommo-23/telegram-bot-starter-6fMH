import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Token del bot
TOKEN = "7514576903:AAH9eTd__xqhey_jnzwP1pLl0DTYgtckODw"

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
    """Inoltra il messaggio se proviene da un canale monitorato e logga dettagli."""
    if update.message:
        chat_username = update.message.chat.username
        message_text = update.message.text
        print(f"Ricevuto messaggio da: {chat_username}")
        print(f"Dettagli del messaggio: {update.message.to_dict()}")

        if chat_username in CANALI_MONITORATI:
            nome_canale = CANALI_MONITORATI[chat_username]
            testo_inoltrato = f"Nuova ROM per {nome_canale}\n\n{message_text}"
            await context.bot.send_message(chat_id=CHAT_DESTINAZIONE, text=testo_inoltrato)
            print(f"Inoltrato messaggio: {testo_inoltrato}")
        else:
            print("L'aggiornamento ricevuto non proviene da un canale monitorato.")
    else:
        print("L'aggiornamento ricevuto non contiene un messaggio valido.")

def main() -> None:
    # Configura l'applicazione
    application = Application.builder().token(TOKEN).build()

    # Aggiungi i gestori di comandi e messaggi
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.ChatType.CHANNEL, inoltra_messaggio))

    # Esegui l'applicazione utilizzando il metodo di polling o webhook
    if os.getenv("USE_WEBHOOK") == "True":
        application.run_webhook(
            listen="0.0.0.0",
            port=int(os.environ.get("PORT", 8443)),
            url_path=TOKEN,
            webhook_url="https://telegram-bot-starter-production-f0c4.up.railway.app/" + TOKEN,
        )
    else:
        application.run_polling()

if __name__ == '__main__':
    main()
