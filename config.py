# Configuration สำหรับ AI Models
import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Model Configuration
TEXT_MODELS = [
    "gpt-3.5-turbo",  # แนะนำสำหรับการใช้งานทั่วไป
    "gpt-4",  # รุ่นใหม่กว่า แต่ใช้ token มากกว่า
    "gpt-3.5-turbo-16k",  # รองรับข้อความยาว
]

# AI Settings
MAX_TOKENS = 200  # จำกัดความยาวการตอบกลับ
DEFAULT_TIMEOUT = 30
TEMPERATURE = 0.8  # ความสร้างสรรค์ในการตอบ (0.0-1.0)

# Error Messages
ERROR_MESSAGES = {
    "model_not_found": "ขออภัยครับ มีปัญหากับการเชื่อมต่อ AI model กรุณาลองใหม่อีกครั้ง หรือติดต่อผู้ดูแลระบบ",
    "quota_exceeded": "ขออภัยครับ AI quota หมดแล้ว กรุณาลองใหม่ในภายหลัง",
    "api_key_invalid": "ขออภัยครับ มีปัญหากับ OpenAI API Key กรุณาตรวจสอบการตั้งค่า",
    "network_error": "ขออภัยครับ มีปัญหาการเชื่อมต่อเครือข่าย กรุณาลองใหม่อีกครั้ง",
    "vision_not_available": "ขออภัยครับ ไม่สามารถวิเคราะห์รูปภาพได้ เนื่องจาก vision model ไม่พร้อมใช้งาน",
    "image_download_failed": "ขออภัยครับ ไม่สามารถดาวน์โหลดรูปภาพได้",
    "ai_not_ready": "❌ AI ไม่พร้อมใช้งาน กรุณาตรวจสอบการตั้งค่า",
}

# Bot Settings
BOT_PREFIX = "!"
BOT_STATUS = "/help เพื่อดูคำสั่ง"

# Voice Settings
VOICE_RATE = 150  # ความเร็วในการพูด
VOICE_VOLUME = 0.9  # ความดัง
VOICE_ENERGY_THRESHOLD = 4000

# Permissions
REQUIRED_PERMISSIONS = [
    "Send Messages",
    "Read Message History",
    "Use Slash Commands",
    "Embed Links",
    "Connect",
    "Speak",
    "Use Voice Activity",
    "Manage Messages",
]

# Development Settings
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
