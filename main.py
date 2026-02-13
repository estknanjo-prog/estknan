import os
import telebot
from yt_dlp import YoutubeDL

# استدعاء التوكن من متغيرات البيئة (أفضل للأمان على Railway)
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! أرسل لي رابط فيديو من (TikTok, Instagram, YouTube) وسأقوم بتحميله لك.")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    if "http" not in url:
        bot.reply_to(message, "الرجاء إرسال رابط صحيح.")
        return

    msg = bot.reply_to(message, "جاري معالجة الرابط والتحميل... انتظر قليلاً ⏳")
    
    # إعدادات التحميل
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.mp4',
        'quiet': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # إرسال الفيديو للمستخدم
        with open('video.mp4', 'rb') as video:
            bot.send_video(message.chat.id, video)
        
        # حذف الملف من السيرفر بعد الإرسال لتوفير المساحة
        os.remove('video.mp4')
        bot.delete_message(message.chat.id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"حدث خطأ أثناء التحميل: {str(e)}", message.chat.id, msg.message_id)

if __name__ == "__main__":
    bot.polling(none_stop=True)
