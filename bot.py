import discord
from discord.ext import commands
from playwright.async_api import async_playwright
import asyncio

# --- ตั้งค่า Discord ---
TOKEN = 'MTQyNDcxMjIxMjgyMzU0Mzg1OQ.GKZtgq.8V0pIWNCdJCJ4hR2XCzh1nfMvhTIm_MDqNPoW4'
# ห้องที่ต้องการให้บอททำงาน (ใส่ ID ห้อง)
TARGET_CHANNEL_ID = 1424730367952289822

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

async def ask_gemini_web(question):
    async with async_playwright() as p:
        # เปิดเบราว์เซอร์
        browser = await p.chromium.launch(headless=True) # ตั้งเป็น False ถ้าอยากเห็นตอนมันพิมพ์
        page = await browser.new_page()
        
        try:
            # 1. เข้าหน้าเว็บ Gemini
            await page.goto("https://gemini.google.com/app", wait_until="networkidle")
            
            # 2. หาช่องพิมพ์ข้อความ (Selector ของ Gemini มักจะเป็น div ที่เขียนได้)
            # เราจะใช้วิธีโฟกัสไปที่จุดที่เขียนว่า "Enter a prompt here"
            placeholder = "Enter a prompt here"
            await page.get_by_placeholder(placeholder).fill(user_question)
            
            # 3. กดปุ่มส่ง (หรือกด Enter)
            await page.keyboard.press("Enter")
            
            # 4. รอให้ AI พิมพ์ตอบ (เราจะรอจนกว่าปุ่ม "Stop" จะหายไป หรือข้อความนิ่ง)
            # นี่คือจุดที่ยากที่สุด เพราะหน้าเว็บจะขยับตลอดเวลา
            await asyncio.sleep(10) # รอเบื้องต้น 10 วินาทีให้ AI ประมวลผล
            
            # 5. ดึงข้อความตอบกลับล่าสุด
            # โดยปกติ Gemini จะเก็บคำตอบไว้ใน class ที่ชื่อประมาณ 'model-response-text'
            responses = await page.query_selector_all(".model-response-text")
            if responses:
                last_response = await responses[-1].inner_text()
                return last_response
            else:
                return "❌ บอทงงครับ หาช่องคำตอบไม่เจอ (หน้าเว็บอาจจะเปลี่ยนโครงสร้าง)"
                
        except Exception as e:
            return f"❌ เกิดข้อผิดพลาดทางเทคนิค: {str(e)}"
        finally:
            await browser.close()

@bot.event
async def on_ready():
    print(f'✅ บอท Gemini Web ออนไลน์แล้ว: {bot.user}')

@bot.event
async def on_message(message):
    # ไม่ตอบข้อความตัวเอง และตอบเฉพาะห้องที่ตั้งไว้
    if message.author == bot.user:
        return
    
    if message.channel.id == TARGET_CHANNEL_ID:
        async with message.channel.typing():
            print(f"📩 รับคำถามจาก {message.author}: {message.content}")
            answer = await ask_gemini_web(message.content)
            await message.reply(answer)

bot.run(TOKEN)
