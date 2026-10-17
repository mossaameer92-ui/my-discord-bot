import os
import discord
from discord.ext import tasks, commands
import itertools
import string
import aiohttp

# إعداد الصلاحيات الأساسية للبوت
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# أيدي الروم المخصص لإرسال النتائج
CHANNEL_ID = 1560832353020936344

# الحروف والأرقام المستخدمة في توليد الأسماء (حروف صغيرة وأرقام)
CHARACTERS = string.ascii_lowercase + string.digits

@bot.event
async def on_ready():
    print(f"✅ تم تسجيل الدخول باسم البوت: {bot.user.name}")
    print("🚀 جاري بدء مهمة الفحص الدوري...")
    check_usernames.start()

@tasks.loop(seconds=5)  # فحص دوري كل 5 ثوانٍ
async def check_usernames():
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print("⚠️ تعذر العثور على القناة، تأكد من وجود البوت فيها وصحة الصلاحيات.")
        return

    # توليد وفحص يوزر ثلاثي/رباعي
    for p in itertools.product(CHARACTERS, repeat=4):
        username = "".join(p)
        
        is_available = await check_discord_username(username)
        
        if is_available:
            await channel.send(f"🎉 **يوزر متاح جديد!**\nالاسم: `{username}`")
            # توقف مؤقت لتجنب الإغراق (Spam)
            break

async def check_discord_username(username):
    # إرسال طلب للتحقق من إمكانية استخدام اسم المستخدم عبر Discord API
    url = f"https://discord.com/api/v9/users/pomelo/attempt"
    headers = {
        "Authorization": os.environ.get("DISCORD_TOKEN"),
        "Content-Type": "application/json"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json={"username": username}, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data.get("taken") == False
    return False

# تشغيل البوت باستخدام متغير البيئة
bot.run(os.environ.get("DISCORD_TOKEN"))
