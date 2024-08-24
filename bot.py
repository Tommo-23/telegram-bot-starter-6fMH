import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Token del bot
TOKEN = "7514576903:AAH9eTd__xqhey_jnzwP1pLl0DTYgtckODw"

# Canale di destinazione per l'inoltro dei messaggi
CHAT_DESTINAZIONE = "@TuttoModding"

# Lista di chat pubbliche da cui inoltrare i messaggi
CHAT_MONITORATE = ["@setupTommo23"]  # Sostituisci con i tuoi canali pubblici

async def start(update: Update, context: CallbackContext) -> None:
    """Risponde al comando /start."""
    await update.message.reply_text('I am here to forward messages from monitored channels to the destination channel.')

async def inoltra_messaggio(update: Update, context: CallbackContext) -> None:
    """Inoltra messaggi da chat monitorate a chat di destinazione."""
    if update.message:
        chat = update.message.chat
        chat_username = chat.username if chat.username else 'N/A'
        message_text = update.message.text if update.message.text else 'No text'
        
        print(f"Ricevuto messaggio da: {chat_username}")
        print(f"Dettagli del messaggio: {update.message.to_dict()}")

        if chat_username in CHAT_MONITORATE:
            # Costruisci il testo del messaggio da inoltrare
            testo_inoltrato = f"Messaggio da {chat_username}:\n\n{message_text}"
            await context.bot.send_message(chat_id=CHAT_DESTINAZIONE, text=testo_inoltrato)
            print(f"Inoltrato messaggio: {testo_inoltrato}")
        else:
            print("Il messaggio non proviene da una chat monitorata.")
    else:
        print("L'aggiornamento ricevuto non contiene un messaggio valido.")

def main() -> None:
    # Configura l'applicazione
    application = Application.builder().token(TOKEN).build()

    # Aggiungi i gestori di comandi e messaggi
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.ChatType.CHANNEL & filters.TEXT, inoltra_messaggio))

    # Usa il Webhook
    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8443)),
        url_path=TOKEN,
        webhook_url=f"https://telegram-bot-starter-production-f0c4.up.railway.app/{TOKEN}",
    )

if __name__ == '__main__':
    main()
