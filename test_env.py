import os
from dotenv import load_dotenv

load_dotenv()

print("=== ทดสอบ Environment Variables ===")
print(
    f"OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY', 'ไม่พบ')[:10]}..."
    if os.getenv("OPENAI_API_KEY")
    else "OPENAI_API_KEY: ไม่พบ"
)
print(
    f"GEMINI_API_KEY: {os.getenv('GEMINI_API_KEY', 'ไม่พบ')[:10]}..."
    if os.getenv("GEMINI_API_KEY")
    else "GEMINI_API_KEY: ไม่พบ"
)
print(
    f"DISCORD_TOKEN: {os.getenv('DISCORD_TOKEN', 'ไม่พบ')[:10]}..."
    if os.getenv("DISCORD_TOKEN")
    else "DISCORD_TOKEN: ไม่พบ"
)

print("\n=== วิธีแก้ไข ===")
print("1. สร้างไฟล์ .env ในโฟลเดอร์หลัก")
print("2. เพิ่มบรรทัดต่อไปนี้:")
print("   GEMINI_API_KEY=your_api_key_here")
print("   DISCORD_TOKEN=your_discord_token_here")
print("3. แทนที่ your_api_key_here ด้วย API Key จริงจาก Makersuite")
print("4. บันทึกไฟล์และรันบอทใหม่")
