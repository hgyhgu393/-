# ใช้ Image ที่มี Python และ Playwright มาให้พร้อมแล้ว
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

# ตั้งโฟลเดอร์ทำงาน
WORKDIR /app

# ก๊อปปี้ไฟล์ทั้งหมดเข้าเครื่อง
COPY . .

# ติดตั้ง Library จาก requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# สั่งรันบอท
CMD ["python", "bot.py"]
