#!/usr/bin/env python3
"""
ทดสอบการเชื่อมต่อ Google Gemini API
ใช้สำหรับตรวจสอบว่า GEMINI_API_KEY ทำงานได้หรือไม่
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

# โหลด environment variables
load_dotenv()


def test_gemini_connection():
    """ทดสอบการเชื่อมต่อ Gemini API"""
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("❌ ไม่พบ GEMINI_API_KEY ใน environment variables")
        print("กรุณาตั้งค่า GEMINI_API_KEY ในไฟล์ .env")
        return False

    if not api_key.startswith("AIza"):
        print("❌ GEMINI_API_KEY ไม่ถูกต้อง (ควรขึ้นต้นด้วย AIza)")
        return False

    print(f"🔑 พบ Gemini API Key: {api_key[:12]}...")

    # ตั้งค่า API key
    genai.configure(api_key=api_key)

    try:
        print("🔄 กำลังทดสอบการเชื่อมต่อ Gemini API...")
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content("สวัสดีข้าวปั้น!")
        print("✅ การเชื่อมต่อ Gemini API สำเร็จ!")
        print(f"🤖 ข้าวปั้นตอบ: {response.text}")
        return True
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
        return False


if __name__ == "__main__":
    print("🧪 ทดสอบการเชื่อมต่อ Google Gemini API")
    print("=" * 50)
    test_gemini_connection()
    print("\n" + "=" * 50)
    print("✅ การทดสอบเสร็จสิ้น")
