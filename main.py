import telebot
import os

# سحب التوكن من إعدادات ريل واي (Variables)
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# معرف الأدمن الخاص بك (Estknan Jo)
ADMIN_ID = 5307344707 

# ملف لحفظ المستخدمين (سيتم إنشاؤه تلقائياً)
USERS_FILE = "users.txt"

def save_user(user_id):
    """حفظ المستخدم الجديد في ملف نصي لضمان عدم التكرار"""
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as f:
            pass
    
    with open(USERS_FILE, 'r') as f:
        users = f.read().splitlines()
    
    if str(user_id) not in users:
        with open(USERS_FILE, 'a') as f:
            f.write(f"{user_id}\n")

def count_users():
    """حساب عدد المستخدمين المسجلين"""
    if not os.path.exists(USERS_FILE):
        return 0
    with open(USERS_FILE, 'r') as f:
        return len(f.read().splitlines())

# --- الأوامر ---

@bot.message_handler(commands=['start'])
def send_welcome(message):
    save_user(message.from_user.id)
    user_name = message.from_user.first_name
    welcome_text = (
        f"🌟 أهلاً بك يا {user_name} في بوت استكنان جو! 🎵\n\n"
        "أنا هنا لأجعل تجربتك الموسيقية أفضل.\n"
        "🎶 أرسل اسم الأغنية التي تبحث عنها وسأساعدك.\n\n"
        "✅ البوت يعمل الآن بنجاح على Railway."
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(commands=['stats'])
def show_stats(message):
    # التأكد أنك أنت الأدمن
    if message.from_user.id == ADMIN_ID:
        total = count_users()
        bot.reply_to(message, f"📊 **إحصائيات البوت:**\n\n👥 عدد المستخدمين النشطين: {total}")
    else:
        bot.reply_to(message, "⚠️ هذا الأمر مخصص للمطور فقط.")

# معالج الرسائل العادية
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    save_user(message.from_user.id)
    bot.reply_to(message, "🔍 جاري البحث عن طلبك... ترقب التحديثات القادمة!")

# تشغيل البوت
if __name__ == "__main__":
    print("استكنان جو يعمل الآن...")
    bot.infinity_polling()
