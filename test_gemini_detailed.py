import os
import google.generativeai as genai
from dotenv import load_dotenv
import requests

load_dotenv()


def test_api_key_directly():
    """ทดสอบ API Key โดยตรงกับ Google API"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ ไม่พบ GEMINI_API_KEY")
        return False

    print(f"🔑 API Key: {api_key[:10]}...")
    print(f"📏 ความยาว: {len(api_key)}")

    # ทดสอบกับ Google API โดยตรง
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": "สวัสดีครับ"}]}]}

    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        print(f"📡 HTTP Status: {response.status_code}")

        if response.status_code == 200:
            print("✅ API Key ทำงานได้!")
            result = response.json()
            if "candidates" in result:
                print(
                    f"💬 คำตอบ: {result['candidates'][0]['content']['parts'][0]['text']}"
                )
            return True
        else:
            print(f"❌ API Error: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Network Error: {e}")
        return False


def test_generativeai_library():
    """ทดสอบ google-generativeai library"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return False

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content("สวัสดีครับ")
        print("✅ google-generativeai library ทำงานได้!")
        print(f"💬 คำตอบ: {response.text}")
        return True
    except Exception as e:
        print(f"❌ Library Error: {e}")
        return False


if __name__ == "__main__":
    print("=== ทดสอบ Gemini API แบบละเอียด ===\n")

    print("1. ทดสอบ API Key โดยตรง:")
    direct_test = test_api_key_directly()

    print("\n2. ทดสอบ google-generativeai library:")
    library_test = test_generativeai_library()

    print("\n=== สรุปผล ===")
    if direct_test and library_test:
        print("✅ ทั้งสองวิธีทำงานได้ปกติ")
    elif direct_test and not library_test:
        print("⚠️ API Key ทำงานได้ แต่ library มีปัญหา")
    elif not direct_test and library_test:
        print("⚠️ Library ทำงานได้ แต่ API Key มีปัญหา")
    else:
        print("❌ ทั้งสองวิธีมีปัญหา")
        print("\n=== วิธีแก้ไข ===")
        print("1. สร้าง API Key ใหม่จาก https://makersuite.google.com/app/apikey")
        print("2. ตรวจสอบว่าเปิดใช้งาน Generative Language API แล้ว")
        print("3. ลองใช้บัญชี Google อื่น")
        print("4. ตรวจสอบว่า Key ไม่หมดอายุหรือถูกจำกัดสิทธิ์")
