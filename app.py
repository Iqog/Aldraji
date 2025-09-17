import telebot
import requests
import os
from flask import Flask

# تهيئة البوت
TOKEN = os.environ.get('BOT_TOKEN')  # سيأتي من متغيرات البيئة
bot = telebot.TeleBot(TOKEN)

# خادم ويب للحفاظ على تشغيل البوت
app = Flask(name)

@app.route('/')
def home():
    return "Bot is running!"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "مرحبًا! أرسل لي صورة وسأحولها إلى رابط Telegra.ph.")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        # الحصول على أعلى دقة للصورة
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # حفظ الصورة مؤقتاً
        file_name = f"temp_{message.message_id}.jpg"
        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        # رفع الصورة إلى Telegra.ph
        with open(file_name, 'rb') as file:
            response = requests.post('https://telegra.ph/upload', files={'file': file})
        
        # تنظيف الملف المؤقت
        os.remove(file_name)
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                image_url = "https://telegra.ph" + data[0]['src']
                bot.reply_to(message, f"رابط الصورة: {image_url}")
            else:
                bot.reply_to(message, "❌ فشل في الحصول على الرابط.")
        else:
            bot.reply_to(message, "❌ فشل في رفع الصورة.")
            
    except Exception as e:
        bot.reply_to(message, f"❌ حدث خطأ: {str(e)}")

# تشغيل البوت وخادم الويب
if name == "main":
    import threading
    threading.Thread(target=bot.infinity_polling).start()
    app.run(host='0.0.0.0', port=5000)
