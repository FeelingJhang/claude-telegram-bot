import os
import telebot
import anthropic

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

user_histories = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_histories[message.chat.id] = []
    bot.reply_to(message, "你好！我是 Claude AI，有什麼可以幫你的？")

@bot.message_handler(commands=['clear'])
def clear(message):
    user_histories[message.chat.id] = []
    bot.reply_to(message, "對話記錄已清除！")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    chat_id = message.chat.id
    if chat_id not in user_histories:
        user_histories[chat_id] = []
    
    user_histories[chat_id].append({
        "role": "user",
        "content": message.text
    })
    
    bot.send_chat_action(chat_id, 'typing')
    
    try:
        response = client.messages.create(
            model="claude-sonnet-5-5",
            max_tokens=1024,
            messages=user_histories[chat_id]
        )
        reply = response.content[0].text
        
        user_histories[chat_id].append({
            "role": "assistant",
            "content": reply
        })
        
        bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, f"發生錯誤：{str(e)}")

bot.polling()
