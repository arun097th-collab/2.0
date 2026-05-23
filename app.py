import telebot

TOKEN = "8653018611:AAGtxeIlVsrWJriE08hrZEsRfII-YVLYUcY"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Send Video 🎬")

@bot.message_handler(content_types=['video','document'])
def video(message):

    file_id = message.video.file_id if message.video else message.document.file_id

    bot.reply_to(
        message,
        f"Saved ✅\n\nFile ID:\n{file_id}"
    )

print("Bot Started...")
bot.infinity_polling()
