import telebot
import os

# سحب التوكن من إعدادات ريل واي (Variables)
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# معرف الأدمن الخاص بك
ADMIN_ID = 5307344707 

# ملف لحفظ المستخدمين
USERS_FILE = "users.txt"

def save_user(user_id):
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as f:
            pass
    with open(USERS_FILE, 'r') as f:
        users = f.read().splitlines()
    if str(user_id) not in users:
        with open(USERS_FILE, 'a') as f:
            f.write(f"{user_id}\n")

def count_users():
    if not os.path.exists(USERS_FILE):
        return 0
    with open(USERS_FILE, 'r') as f:
        return len(f.read().splitlines())

@bot.message_handler(commands=['start'])
def send_welcome(message):
    save_user(message.from_user.id)
    user_name = message.from_user.first_name
    
    # نص الترحيب الجديد حسب طلبك
    welcome_text = (
        f"👋 أهلاً بك يا {user_name} في بوت سناب تيوب!\n\n"
        "📥 يمكنك الآن تحميل الفيديوهات والموسيقى بكل سهولة.\n"
        "🚀 فقط قم بإرسال رابط الفيديو الذي تود تحميله.\n\n"
        "✨ جاري العمل على معالجة طلباتك بسرعة عالية!"
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(commands=['stats'])
def show_stats(message):
    if message.from_user.id == ADMIN_ID:
        total = count_users()
        bot.reply_to(message, f"📊 **إحصائيات البوت:**\n\n👥 عدد المستخدمين: {total}")
    else:
        bot.reply_to(message, "⚠️ هذا الأمر مخصص للإدارة فقط.")

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    save_user(message.from_user.id)
    # رد ذكي عند استلام رابط أو نص
    bot.reply_to(message, "🔍 جاري فحص الرابط وتحضير ملف التحميل... انتظر لحظة!")

if __name__ == "__main__":
    bot.infinity_polling()
