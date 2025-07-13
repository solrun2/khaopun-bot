import os
import google.generativeai as genai
from dotenv import load_dotenv

# โหลด environment variables
load_dotenv()

# ดึง API Key
api_key = os.getenv("GEMINI_API_KEY")

print("=== ทดสอบ Gemini API Key ===")
print(f"API Key ที่โหลดได้: {api_key[:10]}..." if api_key else "ไม่พบ API Key")
print(f"ความยาวของ Key: {len(api_key) if api_key else 0}")

if not api_key:
    print("❌ ไม่พบ GEMINI_API_KEY ใน .env file")
    exit(1)

# ตั้งค่า API Key
try:
    genai.configure(api_key=api_key)
    print("✅ ตั้งค่า API Key สำเร็จ")
except Exception as e:
    print(f"❌ เกิดข้อผิดพลาดในการตั้งค่า API Key: {e}")
    exit(1)

# ทดสอบเรียก API
try:
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content("สวัสดีครับ")
    print("✅ ทดสอบ API สำเร็จ!")
    print(f"คำตอบ: {response.text}")
except Exception as e:
    print(f"❌ เกิดข้อผิดพลาดในการเรียก API: {e}")
    print("\n=== ข้อมูลเพิ่มเติม ===")
    print("1. ตรวจสอบว่า API Key ถูกต้องและไม่หมดอายุ")
    print("2. ตรวจสอบว่าเปิดใช้งาน Generative Language API แล้ว")
    print("3. ตรวจสอบว่า Key ไม่ถูกจำกัดสิทธิ์")
    print("4. ลองสร้าง API Key ใหม่จาก https://makersuite.google.com/app/apikey")
