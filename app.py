from telethon.sync import TelegramClient
from telethon import events
from telethon.sessions import StringSession
import asyncio
import os
import time
import datetime

# جلب المتغيرات من Environment
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION = os.environ.get("SESSION")

# انشاء الكلاينت
client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

# ✅ امر فحص
@client.on(events.NewMessage(outgoing=True, pattern=".فحص"))
async def check(event):
    start_time = time.time()
    await asyncio.sleep(1)
    ping = round((time.time() - start_time) * 1000, 2)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await event.edit(
        f"✅ السورس يعمل\n📡 Ping: {ping}ms\n🕒 الوقت: {now}"
    )

# ✅ امر امسحلي (مسح جميع رسائل المرسل داخل القروب)
@client.on(events.NewMessage(pattern=".امسحلي"))
async def delete_my_msgs(event):
    count = 0
    async for msg in client.iter_messages(event.chat_id):
        if msg.sender_id == event.sender_id:
            await msg.delete()
            count += 1
    await client.send_message(event.chat_id, f"🗑️ تم مسح {count} من رسائلك")

# تشغيل البوت
async def main():
    print("✅ البوت يعمل الآن بدون توقف...")
    await client.start()
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
