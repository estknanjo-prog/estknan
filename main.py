import telebot
import os
import yt_dlp

# التوكن الجديد لبوت SBNAPTUBE_bot
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# معرفك كأدمن
ADMIN_ID = 5307344707 
USERS_FILE = "users.txt"

def save_user(user_id):
    if not os.path.exists(USERS_FILE):
        open(USERS_FILE, 'w').close()
    with open(USERS_FILE, 'r') as f:
        users = f.read().splitlines()
    if str(user_id) not in users:
        with open(USERS_FILE, 'a') as f:
            f.write(f"{user_id}\n")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    save_user(message.from_user.id)
    user_name = message.from_user.first_name
    welcome_text = (
        f"👋 أهلاً بك يا {user_name} في بوت سناب تيوب!\n\n"
        "📥 أرسل لي رابط الفيديو (يوتيوب حالياً) وسأرسله لك كملف صوتي MP3 فوراً.\n"
        "🚀 الخدمة سريعة ومجانية بالكامل!"
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(commands=['stats'])
def show_stats(message):
    if message.from_user.id == ADMIN_ID:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r') as f:
                total = len(f.read().splitlines())
            bot.reply_to(message, f"📊 عدد مستخدمي البوت حالياً: {total}")
    else:
        bot.reply_to(message, "⚠️ مخصص للمطور فقط.")

@bot.message_handler(func=lambda message: True)
def handle_download(message):
    url = message.text
    if "youtube.com" in url or "youtu.be" in url:
        save_user(message.from_user.id)
        msg = bot.reply_to(message, "⏳ جاري التحميل والمعالجة... انتظر لحظة")
        
        try:
            # إعدادات التحميل لتحويله لـ MP3
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'song.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            # إرسال الملف
            with open('song.mp3', 'rb') as audio:
                bot.send_audio(message.chat.id, audio, caption="🎵 تم التحميل بواسطة سناب تيوب")
            
            # تنظيف السيرفر
            os.remove('song.mp3')
            bot.delete_message(message.chat.id, msg.message_id)
            
        except Exception as e:
            bot.edit_message_text(f"❌ فشل التحميل. تأكد من الرابط وحاول مجدداً.", message.chat.id, msg.message_id)
    else:
        bot.reply_to(message, "⚠️ من فضلك أرسل رابط يوتيوب صحيح.")

if __name__ == "__main__":
    bot.infinity_polling()
