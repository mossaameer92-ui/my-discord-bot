import discord
from discord.ext import tasks, commands
import itertools
import string
import aiohttp

# إعداد الصلاحيات الأساسية للبوت
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# آيدي الروم المخصص لإرسال النتائج في سيرفرك
CHANNEL_ID = 1560832353020936344  

# إعداد الحروف والأرقام المستخدمة في توليد الأسماء (حروف صغيرة وأرقام)
CHARACTERS = string.ascii_lowercase + string.digits

@bot.event
async def on_ready():
    print(f"✅ تم تسجيل الدخول بنجاح باسم البوت: {bot.user.name}")
    print("🚀 جاري بدء مهمة الفحص الدوري...")
    check_usernames.start()

@tasks.loop(minutes=2)  # فاصل زمني آمن لتجنب حظر البوت أو إغلاق الاتصال
async def check_usernames():
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print("⚠️ تعذر العثور على القناة، تأكد من وجود البوت فيها وصحة الصلاحيات.")
        return

    # مثال لتوليد وفحص يوزر ثلاثي/رباعي
    for p in itertools.product(CHARACTERS, repeat=4):
        username = "".join(p)
        
        # الاتصال بفحص توفر اسم المستخدم
        is_available = await check_discord_username(username)
        
        if is_available:
            await channel.send(f"🎉 **يوزر متاح جديد!**\nالاسم: `{username}`")
            # توقف مؤقت لمنع الإغراق (Spam)
            break

async def check_discord_username(username):
    # دالة فحص الآبي آي لتوفر الاسم
    return False

# توكن البوت الخاص بك
bot.run("MTU2MDgzMjQzNjExODc1MzQyMQ.Gy7e5O.GRArKOsvw2PRIFEpAU7HUxTBXUAEPYe3aHDETY")
