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
    
    # فحص القناة وإرسال رسالة تجريبية عند التشغيل
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        print(f"✅ تم العثور على القناة: {channel.name}")
        try:
            await channel.send("🤖 **البوت يعمل الآن بنجاح وبدأ عملية الفحص التلقائي!**")
        except Exception as e:
            print(f"❌ البوت وجد القناة ولكن لا يمتلك صلاحية إرسال الرسائل: {e}")
    else:
        print("❌ لم يتم العثور على القناة! تأكد من صحة CHANNEL_ID أو وجود البوت داخل السيرفر.")

    print("🚀 جاري بدء مهمة الفحص الدوري...")
    check_usernames.start()

# أمر تجريبي لاختبار استجابة البوت
@bot.command()
async def ping(ctx):
    await ctx.send("Pong! 🏓 البوت متصل ويستجيب بنجاح.")

@tasks.loop(seconds=10)  # فحص دوري كل 10 ثوانٍ لتجنب حظر الطلبات (Rate Limit)
async def check_usernames():
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        return

    # توليد وفحص يوزر ثلاثي/رباعي
    for p in itertools.product(CHARACTERS, repeat=4):
        username = "".join(p)
        
        is_available = await check_discord_username(username)
        
        if is_available:
            await channel.send(f"🎉 **يوزر متاح جديد!**\nالاسم: `{username}`")
            break

async def check_discord_username(username):
    # إرسال طلب للتحقق من إمكانية استخدام اسم المستخدم عبر Discord API
    url = f"https://discord.com/api/v9/users/pomelo/attempt"
    headers = {
        "Authorization": os.environ.get("DISCORD_TOKEN"),
        "Content-Type": "application/json"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json={"username": username}, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    # إذا كان taken يساوي False فهذا يعني أن اليوزر متاح
                    return data.get("taken") == False
    except Exception as e:
        print(f"خطأ أثناء الفحص: {e}")
    return False

# تشغيل البوت باستخدام متغير البيئة
bot.run(os.environ.get("DISCORD_TOKEN"))
