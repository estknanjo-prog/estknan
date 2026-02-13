import telebot
import os
import yt_dlp
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# التوكن من إعدادات ريل واي
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# معرفك كأدمن
ADMIN_ID = 5307344707 

# ملفات التخزين
USERS_FILE = "users.txt"
RATINGS_FILE = "ratings.txt"

def save_data(file, data):
    if not os.path.exists(file):
        open(file, 'w').close()
    with open(file, 'a') as f:
        f.write(f"{data}\n")

def get_total_count(file):
    if not os.path.exists(file): return 0
    with open(file, 'r') as f:
        return len(set(f.read().splitlines()))

@bot.message_handler(commands=['start'])
def send_welcome(message):
    save_data(USERS_FILE, message.from_user.id)
    bot.reply_to(message, f"👋 أهلاً بك يا {message.from_user.first_name} في بوت سناب تيوب!\n\n📥 أرسل رابط الفيديو للتحميل فوراً.")

# لوحة التحكم المطورة للأدمن
@bot.message_handler(commands=['admin'])
def show_admin_panel(message):
    if message.from_user.id == ADMIN_ID:
        total_users = get_total_count(USERS_FILE)
        
        # قراءة التقييمات
        last_ratings = "لا يوجد تقييمات بعد."
        if os.path.exists(RATINGS_FILE):
            with open(RATINGS_FILE, 'r') as f:
                lines = f.read().splitlines()
                total_r = len(lines)
                # عرض آخر 5 تقييمات فقط عشان الرسالة ما تكون طويلة
                last_ratings = "\n".join(lines[-5:]) if lines else "لا يوجد"
        else:
            total_r = 0

        admin_msg = (
            "📊 **لوحة تحكم الإدارة**\n\n"
            f"👥 عدد المستخدمين: {total_users}\n"
            f"⭐ إجمالي التقييمات: {total_r}\n\n"
            f"📜 **آخر 5 تقييمات وصلتك:**\n{last_ratings}"
        )
        bot.reply_to(message, admin_msg, parse_mode="Markdown")
    else:
        bot.reply_to(message, "⚠️ مخصص للمطور فقط.")

@bot.message_handler(func=lambda message: message.text.startswith("http"))
def handle_download(message):
    url = message.text
    msg = bot.reply_to(message, "⏳ جاري التحميل... انتظر لحظة")
    
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': f'video_{message.chat.id}.mp4',
            'noplaylist': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        with open(f'video_{message.chat.id}.mp4', 'rb') as video:
            bot.send_video(message.chat.id, video, caption="✅ تم التحميل بواسطة سناب تيوب")
        
        os.remove(f'video_{message.chat.id}.mp4')
        bot.delete_message(message.chat.id, msg.message_id)
        
        # إظهار أزرار التقييم
        show_rating_keyboard(message.chat.id)
        
    except Exception:
        bot.edit_message_text("❌ فشل التحميل. تأكد من الرابط.", message.chat.id, msg.message_id)

def show_rating_keyboard(chat_id):
    markup = InlineKeyboardMarkup()
    stars = [InlineKeyboardButton("⭐", callback_data="r_1"),
             InlineKeyboardButton("⭐⭐", callback_data="r_2"),
             InlineKeyboardButton("⭐⭐⭐", callback_data="r_3"),
             InlineKeyboardButton("⭐⭐⭐⭐", callback_data="r_4"),
             InlineKeyboardButton("⭐⭐⭐⭐⭐", callback_data="r_5")]
    markup.add(stars[0], stars[1], stars[2])
    markup.add(stars[3], stars[4])
    bot.send_message(chat_id, "🙏 ما هو تقييمك للخدمة؟", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("r_"))
def handle_rating(call):
    rating_val = call.data.split("_")[1]
    user_info = f"👤 {call.from_user.first_name}: {rating_val} نجوم"
    save_data(RATINGS_FILE, user_info)
    bot.answer_callback_query(call.id, "شكراً لتقييمك! ❤️")
    bot.edit_message_text(f"✅ تم تسجيل تقييمك ({rating_val} نجوم).", call.message.chat.id, call.message.message_id)

if __name__ == "__main__":
    bot.infinity_polling()
