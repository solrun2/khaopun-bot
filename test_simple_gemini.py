import os
import google.generativeai as genai
from dotenv import load_dotenv

# โหลด environment variables
load_dotenv()

# ดึง API Key
api_key = os.getenv("GEMINI_API_KEY")

print("=== ทดสอบ Gemini API แบบง่าย ===")
print(f"API Key: {api_key[:10]}..." if api_key else "ไม่พบ API Key")

if not api_key:
    print("❌ ไม่พบ GEMINI_API_KEY")
    exit(1)

# ตั้งค่า API Key
print("🔧 กำลังตั้งค่า API Key...")
genai.configure(api_key=api_key)
print("✅ ตั้งค่า API Key สำเร็จ")

# ทดสอบเรียก API
print("🚀 กำลังทดสอบ API...")
try:
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content("สวัสดีครับ")
    print("✅ ทดสอบสำเร็จ!")
    print(f"คำตอบ: {response.text}")
except Exception as e:
    print(f"❌ เกิดข้อผิดพลาด: {e}")
    print("\n=== วิธีแก้ไข ===")
    print("1. ตรวจสอบว่า API Key ถูกต้อง")
    print("2. สร้าง API Key ใหม่จาก https://makersuite.google.com/app/apikey")
    print("3. ตรวจสอบว่าเปิดใช้งาน Generative Language API แล้ว")
    print("4. ลองใช้บัญชี Google อื่น")
