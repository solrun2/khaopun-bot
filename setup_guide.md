# 🛠️ คู่มือการติดตั้งเพิ่มเติม

## การติดตั้ง FFmpeg (สำหรับระบบเสียง)

### Windows

1. ดาวน์โหลด FFmpeg จาก https://ffmpeg.org/download.html
2. แตกไฟล์และเพิ่ม path ใน Environment Variables
3. หรือใช้ Chocolatey: `choco install ffmpeg`

### macOS

```bash
brew install ffmpeg
```

### Ubuntu/Debian

```bash
sudo apt update
sudo apt install ffmpeg
```

## การสร้าง OpenAI API Key

1. ไปที่ [OpenAI Platform](https://platform.openai.com/api-keys)
2. เข้าสู่ระบบด้วย OpenAI Account
3. คลิก "Create new secret key"
4. คัดลอก API Key ที่ได้
5. ใส่ในไฟล์ `.env`:
   ```
   OPENAI_API_KEY=sk-your_api_key_here
   ```

**หมายเหตุ**: OpenAI มี quota ฟรีจำกัด (ประมาณ $5 ต่อเดือน) หลังจากนั้นจะต้องชำระเงิน

## การตั้งค่าสิทธิ์บอท

เมื่อเชิญบอทเข้าเซิร์ฟเวอร์ ให้เลือกสิทธิ์เหล่านี้:

### สิทธิ์พื้นฐาน

- Send Messages
- Read Message History
- Use Slash Commands
- Embed Links

### สิทธิ์สำหรับระบบเสียง

- Connect
- Speak
- Use Voice Activity

### สิทธิ์สำหรับการจัดการ

- Manage Messages (สำหรับคำสั่งลบข้อความ)

## การทดสอบระบบ

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

## การแก้ไขปัญหา

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

1. รันไฟล์ `install_pyaudio_windows.bat` ที่อยู่ในโปรเจค
2. รอให้การติดตั้งเสร็จสิ้น

#### วิธีที่ 2: ใช้คำสั่ง

```bash
pip install pipwin
pipwin install pyaudio
```

#### วิธีที่ 3: ติดตั้งจาก wheel file

1. ไปที่ https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
2. ดาวน์โหลดไฟล์ที่ตรงกับ Python version ของคุณ
3. ติดตั้งด้วย: `pip install [ชื่อไฟล์ที่ดาวน์โหลด]`

## 🔧 การแก้ไขปัญหา AI

### ปัญหา Authentication Error

หากเจอข้อผิดพลาด "API key not valid":

1. **ตรวจสอบ API Key**: ตรวจสอบว่า API Key ขึ้นต้นด้วย "sk-" และถูกต้อง
2. **ทดสอบการเชื่อมต่อ**: รันไฟล์ทดสอบ:
   ```bash
   python test_openai.py
   ```
3. **ตรวจสอบ Quota**: ไปที่ [OpenAI Platform](https://platform.openai.com/usage) และตรวจสอบ quota
4. **อัปเดต Library**: อัปเดต openai:
   ```bash
   pip install --upgrade openai
   ```

### ปัญหา Rate Limit

หากเจอข้อผิดพลาด rate limit:

1. ไปที่ [OpenAI Platform](https://platform.openai.com/usage)
2. ตรวจสอบการใช้งานในแท็บ "Usage"
3. รอสักครู่แล้วลองใหม่
4. หรืออัปเกรดบัญชีเพื่อเพิ่ม rate limit

### ปัญหา Quota Exceeded

หากเจอข้อผิดพลาด quota:

1. ไปที่ [OpenAI Platform](https://platform.openai.com/usage)
2. ตรวจสอบการใช้งานในแท็บ "Usage"
3. เพิ่มเงินในบัญชีหรือรอให้ quota รีเซ็ต
4. หรือสร้าง API Key ใหม่

### ปัญหา Network Error

หากเจอปัญหาการเชื่อมต่อ:

1. ตรวจสอบการเชื่อมต่ออินเทอร์เน็ต
2. ตรวจสอบ Firewall และ Proxy
3. ลองใช้ VPN หรือเปลี่ยนเครือข่าย

### การทดสอบ AI แบบละเอียด

รันไฟล์ทดสอบเพื่อตรวจสอบการทำงานของ AI:

```bash
python test_openai.py
```

ไฟล์นี้จะ:

- ตรวจสอบ API Key
- ทดสอบการเชื่อมต่อ OpenAI API
- ทดสอบบุคลิกข้าวปั้น
- แสดงผลการทดสอบ

## การปรับแต่งเพิ่มเติม

### เปลี่ยนเสียงของบอท

แก้ไขใน `voice_handler.py`:

```python
self.tts_engine.setProperty('rate', 150)  # ความเร็ว
self.tts_engine.setProperty('volume', 0.9)  # ความดัง
```

### เพิ่มคำสั่ง AI ใหม่

เพิ่มใน `ai_handler.py`:

```python
@app_commands.command(name='คำสั่งใหม่', description='คำอธิบายคำสั่ง')
async def new_command(self, interaction: discord.Interaction, text: str):
    response = await self.ai_handler.get_response(interaction.user.id, text)
    await interaction.response.send_message(response)
```

### ปรับแต่ง AI Model

แก้ไขใน `config.py`:

```python
TEXT_MODELS = [
    "gpt-3.5-turbo",      # แนะนำสำหรับการใช้งานทั่วไป
    "gpt-4",              # รุ่นใหม่กว่า แต่ใช้ token มากกว่า
    "gpt-3.5-turbo-16k"   # รองรับข้อความยาว
]
```

### ปรับแต่งบุคลิกข้าวปั้น

แก้ไขใน `ai_handler.py` ในฟังก์ชัน `_create_onigiri_prompt`:

```python
def _create_onigiri_prompt(self, user_name: str, user_tag: str, message: str, context: str = "") -> str:
    # ปรับแต่งบุคลิกข้าวปั้นที่นี่
    return f"""คุณเป็นบอทดิสคอร์ดชื่อ 'ข้าวปั้น' ซึ่งเป็นหมาชิบะน่ารัก...
    """
```

## การตั้งค่า Environment Variables

สร้างไฟล์ `.env` ในโฟลเดอร์หลักของโปรเจค:

```env
# Discord Bot Token
DISCORD_TOKEN=your_discord_bot_token_here

# OpenAI API Key
OPENAI_API_KEY=sk-your_openai_api_key_here

# การตั้งค่าเพิ่มเติม (ไม่บังคับ)
DEBUG_MODE=False
LOG_LEVEL=INFO
```

## การรันบอท

### รันแบบปกติ

```bash
python bot.py
```

### รันแบบ Debug

```bash
DEBUG_MODE=True python bot.py
```

### รันแบบ Background (Linux/macOS)

```bash
nohup python bot.py > bot.log 2>&1 &
```

## การอัปเดตบอท

1. ดาวน์โหลดโค้ดล่าสุด:

   ```bash
   git pull origin main
   ```

2. อัปเดต dependencies:

   ```bash
   pip install -r requirements.txt --upgrade
   ```

3. รีสตาร์ทบอท

## การสำรองข้อมูล

### สำรองไฟล์สำคัญ

- `.env` - ไฟล์การตั้งค่า
- `config.py` - การตั้งค่าบอท
- ข้อมูลการตั้งค่าอื่นๆ ที่ปรับแต่งเอง

### การกู้คืน

1. คัดลอกไฟล์ `.env` กลับมา
2. รัน `pip install -r requirements.txt`
3. รัน `python bot.py`
