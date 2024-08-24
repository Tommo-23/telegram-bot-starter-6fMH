import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Token del bot
TOKEN = "7514576903:AAH9eTd__xqhey_jnzwP1pLl0DTYgtckODw"

# Canale di destinazione per l'inoltro dei messaggi
CHAT_DESTINAZIONE = "@TuttoModding"

async def start(update: Update, context: CallbackContext) -> None:
    """Risponde al comando /start."""
    await update.message.reply_text('my job is to forward all messages to the specified channel.')

async def inoltra_messaggio(update: Update, context: CallbackContext) -> None:
    """Inoltra tutti i messaggi al canale di destinazione e logga dettagli."""
    if update.message:
        chat = update.message.chat
        chat_username = chat.username if chat.username else 'N/A'
        message_text = update.message.text if update.message.text else 'No text'
        print(f"Ricevuto messaggio da: {chat_username}")
        print(f"Dettagli del messaggio: {update.message.to_dict()}")

        # Costruisci il testo del messaggio da inoltrare
        testo_inoltrato = f"Messaggio da {chat_username}:\n\n{message_text}"
        await context.bot.send_message(chat_id=CHAT_DESTINAZIONE, text=testo_inoltrato)
        print(f"Inoltrato messaggio: {testo_inoltrato}")
    else:
        print("L'aggiornamento ricevuto non contiene un messaggio valido.")

def main() -> None:
    # Configura l'applicazione
    application = Application.builder().token(TOKEN).build()

    # Aggiungi i gestori di comandi e messaggi
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.ALL, inoltra_messaggio))

    # Esegui l'applicazione utilizzando il metodo di polling o webhook
    if os.getenv("USE_WEBHOOK") == "True":
        application.run_webhook(
            listen="0.0.0.0",
            port=int(os.environ.get("PORT", 8443)),
            url_path=TOKEN,
            webhook_url=f"https://telegram-bot-starter-production-f0c4.up.railway.app/{TOKEN}",
        )
    else:
        application.run_polling()

if __name__ == '__main__':
    main()
