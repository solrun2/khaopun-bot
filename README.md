# 🤖 Discord AI Bot

บอทดิสคอร์ดที่ใช้ AI (OpenAI GPT-3.5) สำหรับการสนทนาและระบบเสียง

## ✨ ฟีเจอร์หลัก

- 🤖 **AI Chat** - สนทนากับ AI ผ่าน OpenAI API (บุคลิกข้าวปั้นหมาชิบะ)
- 🎵 **Voice System** - บอทพูดและฟังเสียง
- 📊 **Server Info** - แสดงข้อมูลเซิร์ฟเวอร์
- 🎲 **Utility Commands** - คำสั่งเสริมต่างๆ

## 🚀 การติดตั้ง

### 1. Clone โปรเจค

```bash
git clone <repository-url>
cd datasci
```

### 2. ติดตั้ง Dependencies

```bash
pip install -r requirements.txt
```

### 3. ตั้งค่า Environment Variables

สร้างไฟล์ `.env` และใส่ข้อมูลต่อไปนี้:

```env
DISCORD_TOKEN=your_discord_bot_token
OPENAI_API_KEY=your_openai_api_key
```

### 4. รันบอท

```bash
python bot.py
```

## 📋 คำสั่ง Slash Commands

### 🤖 คำสั่ง AI

- `/ถาม [คำถาม]` - ถามคำถามกับข้าวปั้น AI
- `/ล้างประวัติ` - ล้างประวัติการสนทนากับ AI

### 🎵 คำสั่งเสียง

- `/เข้าร่วม` - เข้าร่วมช่องเสียง
- `/ออก` - ออกจากช่องเสียง
- `/พูด [ข้อความ]` - ให้บอทพูดข้อความ
- `/หยุด` - หยุดการพูด
- `/เสียง` - แสดงสถานะการเชื่อมต่อเสียง

### 📝 คำสั่งพื้นฐาน

- `/สวัสดี` - ทักทายบอท
- `/เวลา` - แสดงเวลาปัจจุบัน
- `/ข้อมูล` - แสดงข้อมูลเซิร์ฟเวอร์
- `/สุ่ม [min] [max]` - สุ่มตัวเลขระหว่างค่าที่กำหนด
- `/ล้าง [จำนวน]` - ลบข้อความ (ต้องมีสิทธิ์)
- `/ping` - ตรวจสอบความเร็วการตอบสนอง
- `/ช่วยเหลือ` - แสดงคำสั่งที่มีอยู่

## 🐶 บุคลิกข้าวปั้น

บอท AI มีบุคลิกเป็น "ข้าวปั้น" หมาชิบะน่ารัก:

- แทนตัวเองว่า "ข้าวปั้น" และพูดภาษาไทยอย่างเป็นมิตรสดใส
- เวลารู้สึกเสียใจจะร้อง "อะแง้" และเวลากวน ๆ จะพูดว่า "อ่าวู้ววว"
- ถ้ามีใครบอกว่าข้าวปั้นดื้อหรือดื้อชะมัด ให้ตอบว่า "ข้าวปั้นไม่ดื้อนะ!!"
- เรียกผู้ใช้ตามแท็ก:
  - แท็ก "nanatsukisolrun" → "แม่แม่"
  - แท็ก "homura2410" → "พ่อพ่อ"
  - คนอื่น → "พี่[ชื่อ]"

## 🎮 ตัวอย่างการใช้งาน

### ทดสอบ AI

```
/ถาม สวัสดีข้าวปั้น!
```

### ทดสอบระบบเสียง

```
/เข้าร่วม
/พูด สวัสดีครับ
/ออก
```

### ทดสอบการเรียกชื่อ

```
@ข้าวปั้น สวัสดีครับ
```

## 💡 ข้อดีของ Slash Commands

1. **UI ที่ดีกว่า** - มี autocomplete และคำอธิบาย
2. **ความปลอดภัย** - ไม่มีปัญหาเรื่อง prefix conflicts
3. **มาตรฐาน Discord** - เป็นวิธีที่ Discord แนะนำ
4. **การจัดการสิทธิ์** - Discord จัดการสิทธิ์ให้อัตโนมัติ
5. **Mobile Friendly** - ใช้งานง่ายบนมือถือ

## 🔧 การตั้งค่าบอท

### สิทธิ์ที่จำเป็น

- Send Messages
- Read Message History
- Use Slash Commands
- Embed Links
- Connect (สำหรับเสียง)
- Speak (สำหรับเสียง)
- Use Voice Activity (สำหรับเสียง)
- Manage Messages (สำหรับคำสั่งลบข้อความ)

### การสร้าง Discord Bot

1. ไปที่ [Discord Developer Portal](https://discord.com/developers/applications)
2. สร้าง Application ใหม่
3. ไปที่ Bot section และสร้าง bot
4. คัดลอก Token และใส่ในไฟล์ `.env`

### การสร้าง OpenAI API Key

1. ไปที่ [OpenAI Platform](https://platform.openai.com/api-keys)
2. เข้าสู่ระบบด้วย OpenAI Account
3. คลิก "Create new secret key"
4. คัดลอก API Key และใส่ในไฟล์ `.env`
5. **หมายเหตุ**: OpenAI มี quota ฟรีจำกัด (ประมาณ $5 ต่อเดือน)

## 🧪 การทดสอบ

### ทดสอบ OpenAI API

```bash
python test_openai.py
```

### ทดสอบการเชื่อมต่อ

```bash
python bot.py
```

## 🛠️ การแก้ไขปัญหา

### บอทไม่ตอบกลับ

- ตรวจสอบ Token ว่าถูกต้อง
- ตรวจสอบว่าเปิดใช้งาน Message Content Intent
- ดู error log ในคอนโซล

### AI ไม่ทำงาน

- ตรวจสอบ OpenAI API Key
- ตรวจสอบการเชื่อมต่ออินเทอร์เน็ต
- ตรวจสอบ quota ใน OpenAI Platform
- รัน `python test_openai.py` เพื่อทดสอบ

### ระบบเสียงไม่ทำงาน

- ตรวจสอบการติดตั้ง FFmpeg
- ตรวจสอบสิทธิ์ของบอทในช่องเสียง
- ตรวจสอบการเชื่อมต่อเสียง

### การติดตั้ง pyaudio บน Windows

หากมีปัญหาในการติดตั้ง pyaudio:

#### วิธีที่ 1: ใช้ไฟล์ batch (แนะนำ)

```bash
install_pyaudio_windows.bat
```

#### วิธีที่ 2: ใช้คำสั่ง

```bash
pip install pipwin
pipwin install pyaudio
```

## 📁 โครงสร้างไฟล์

```
datasci/
├── bot.py                 # ไฟล์หลักของบอท
├── ai_handler.py          # จัดการ AI และการสนทนา
├── voice_handler.py       # จัดการระบบเสียง
├── voice_handler_simple.py # ระบบเสียงแบบง่าย
├── config.py              # การตั้งค่า
├── test_openai.py         # ทดสอบ OpenAI API
├── requirements.txt       # Dependencies
├── setup_guide.md         # คู่มือการติดตั้ง
├── README.md              # คู่มือการใช้งาน
└── .env                   # Environment variables
```

## 🔄 การใช้งานแบบเก่า (Legacy)

คำสั่งแบบเก่าที่ใช้ prefix `!` ยังคงใช้งานได้ แต่แนะนำให้ใช้ slash commands แทน:

```
!ถาม สวัสดีครับ
!เข้าร่วม
!พูด สวัสดีครับ
!ออก
```

## 📝 License

MIT License

## 🤝 Contributing

ยินดีรับ contributions! กรุณาสร้าง issue หรือ pull request

---

**หมายเหตุ**: บอทนี้ใช้ OpenAI API ซึ่งมี quota ฟรีจำกัด กรุณาตรวจสอบ quota ใน OpenAI Platform
