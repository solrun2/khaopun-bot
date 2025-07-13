# 🔄 สรุปการเปลี่ยนแปลง: Gemini API → OpenAI API

## 📋 การเปลี่ยนแปลงหลัก

### 1. เปลี่ยน AI Provider

- **เดิม**: Google Gemini API
- **ใหม่**: OpenAI GPT-3.5-turbo API

### 2. ไฟล์ที่เปลี่ยนแปลง

#### ✅ ไฟล์ที่อัปเดตแล้ว

- `requirements.txt` - เปลี่ยนจาก `google-generativeai` เป็น `openai`
- `config.py` - ปรับการตั้งค่าให้รองรับ OpenAI API
- `ai_handler.py` - ปรับโค้ดให้ใช้ OpenAI API พร้อมบุคลิกข้าวปั้น
- `env_example.txt` - เปลี่ยนจาก `GEMINI_API_KEY` เป็น `OPENAI_API_KEY`
- `README.md` - อัปเดตเอกสารให้ใช้ OpenAI API
- `setup_guide.md` - อัปเดตคู่มือการติดตั้ง

#### ✅ ไฟล์ใหม่

- `test_openai.py` - ไฟล์ทดสอบ OpenAI API

#### ❌ ไฟล์ที่ลบแล้ว

- `test_ai.py` - ไฟล์ทดสอบ Gemini API (ลบแล้ว)

### 3. การเปลี่ยนแปลงในโค้ด

#### AI Handler (`ai_handler.py`)

```python
# เดิม
import google.generativeai as genai
genai.configure(api_key=GEMINI_API_KEY)

# ใหม่
import openai
openai.api_key = OPENAI_API_KEY
```

#### Configuration (`config.py`)

```python
# เดิม
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TEXT_MODELS = ["gemini-1.5-pro", "gemini-pro"]

# ใหม่
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TEXT_MODELS = ["gpt-3.5-turbo", "gpt-4"]
```

### 4. บุคลิกข้าวปั้น

บอท AI มีบุคลิกเป็น "ข้าวปั้น" หมาชิบะน่ารัก:

- แทนตัวเองว่า "ข้าวปั้น" และพูดภาษาไทยอย่างเป็นมิตรสดใส
- เวลารู้สึกเสียใจจะร้อง "อะแง้" และเวลากวน ๆ จะพูดว่า "อ่าวู้ววว"
- ถ้ามีใครบอกว่าข้าวปั้นดื้อหรือดื้อชะมัด ให้ตอบว่า "ข้าวปั้นไม่ดื้อนะ!!"
- เรียกผู้ใช้ตามแท็ก:
  - แท็ก "nanatsukisolrun" → "แม่แม่"
  - แท็ก "homura2410" → "พ่อพ่อ"
  - คนอื่น → "พี่[ชื่อ]"

## 🚀 วิธีใช้งานใหม่

### 1. ตั้งค่า Environment Variables

สร้างไฟล์ `.env`:

```env
DISCORD_TOKEN=your_discord_bot_token
OPENAI_API_KEY=sk-your_openai_api_key
```

### 2. ติดตั้ง Dependencies

```bash
pip install -r requirements.txt
```

### 3. ทดสอบการเชื่อมต่อ

```bash
python test_openai.py
```

### 4. รันบอท

```bash
python bot.py
```

## 📝 คำสั่งที่เปลี่ยนแปลง

### คำสั่ง AI

- `/ถาม [คำถาม]` - ถามคำถามกับข้าวปั้น AI
- `/ล้างประวัติ` - ล้างประวัติการสนทนากับ AI
- `@ข้าวปั้น [ข้อความ]` - พูดคุยกับข้าวปั้นโดยตรง

### คำสั่งที่ถูกลบ

- `/อธิบายรูป` - ไม่รองรับใน OpenAI API เวอร์ชันนี้

## ⚠️ ข้อควรระวัง

### OpenAI API Quota

- OpenAI มี quota ฟรีจำกัด (ประมาณ $5 ต่อเดือน)
- หลังจากนั้นจะต้องชำระเงิน
- ตรวจสอบ quota ได้ที่ [OpenAI Platform](https://platform.openai.com/usage)

### การเปลี่ยนแปลง API Key

- ต้องสร้าง OpenAI API Key ใหม่
- API Key ขึ้นต้นด้วย "sk-"
- ไปที่ [OpenAI Platform](https://platform.openai.com/api-keys)

## 🔧 การแก้ไขปัญหา

### ปัญหาที่พบบ่อย

1. **API Key ไม่ถูกต้อง**

   - ตรวจสอบว่า API Key ขึ้นต้นด้วย "sk-"
   - รัน `python test_openai.py` เพื่อทดสอบ

2. **Quota หมด**

   - ตรวจสอบ quota ที่ [OpenAI Platform](https://platform.openai.com/usage)
   - เพิ่มเงินในบัญชีหรือรอให้ quota รีเซ็ต

3. **Rate Limit**
   - รอสักครู่แล้วลองใหม่
   - หรืออัปเกรดบัญชีเพื่อเพิ่ม rate limit

## 📊 ข้อดีของการเปลี่ยนเป็น OpenAI API

1. **เสถียรภาพ** - OpenAI API มีเสถียรภาพสูงกว่า
2. **ความเร็ว** - การตอบสนองเร็วกว่า
3. **คุณภาพ** - GPT-3.5-turbo มีคุณภาพการตอบที่ดีกว่า
4. **การสนับสนุน** - มีการสนับสนุนและเอกสารที่ดีกว่า

## 📊 ข้อเสีย

1. **ค่าใช้จ่าย** - มีค่าใช้จ่ายหลังจาก quota ฟรีหมด
2. **ไม่รองรับรูปภาพ** - ไม่มีฟีเจอร์อธิบายรูปภาพในเวอร์ชันนี้

## 🎯 สรุป

การเปลี่ยนแปลงเสร็จสิ้นแล้ว! บอทของคุณตอนนี้ใช้ OpenAI API แทน Gemini API และมีบุคลิกข้าวปั้นหมาชิบะน่ารัก พร้อมใช้งานได้ทันที

หากมีปัญหาหรือต้องการความช่วยเหลือเพิ่มเติม กรุณาตรวจสอบเอกสารใน `README.md` และ `setup_guide.md`
