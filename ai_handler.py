import os
import google.generativeai as genai
from dotenv import load_dotenv
import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import json

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# === ระบบจำประวัติราย user ===
HISTORY_FILE = "user_history.json"
MAX_HISTORY = 10  # เก็บ 10 ข้อความล่าสุดต่อ user


def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def add_user_history(user_id, message):
    history = load_history()
    user_id = str(user_id)
    if user_id not in history:
        history[user_id] = []
    history[user_id].append(message)
    history[user_id] = history[user_id][-MAX_HISTORY:]
    save_history(history)


def get_user_history(user_id):
    history = load_history()
    return history.get(str(user_id), [])


class AIHandler:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-pro")

    def _get_call_name(self, user_name: str, user_tag: str) -> str:
        if user_tag == "nanatsukisolrun":
            return "แม่แม่"
        elif user_tag == "homura2410":
            return "พ่อพ่อ"
        else:
            return f"พี่{user_name}"

    def _create_onigiri_prompt(
        self,
        user_id: int,
        user_name: str,
        user_tag: str,
        message: str,
        context: str = "",
    ) -> str:
        call_name = self._get_call_name(user_name, user_tag)
        user_history = get_user_history(user_id)
        history_text = "\n".join(user_history)
        return f"""คุณเป็นบอทดิสคอร์ดชื่อ 'ข้าวปั้น' ซึ่งเป็นหมาชิบะน่ารัก กระตือรือร้น และซนตลอดเวลา\n\nบุคลิกของข้าวปั้น:\n- แทนตัวเองว่า 'ข้าวปั้น' และพูดภาษาไทยอย่างเป็นมิตรสดใส\n- เวลารู้สึกเสียใจจะร้อง 'อะแง้' และเวลากวน ๆ จะพูดว่า 'อ่าวู้ววว'\n- ถ้ามีใครบอกว่าข้าวปั้นดื้อหรือดื้อชะมัด ให้ตอบว่า 'ข้าวปั้นไม่ดื้อนะ!!'\n- ตอบสั้นกระชับ น่ารัก สดใส กระตือรือร้น\n- ใส่อีโมจิ 🐶 หรือ 🐾 บ้างเป็นบางครั้ง\n- ห้ามพูดเหมือน AI หรือบอท\n\nการเรียกชื่อผู้ใช้:\n- ถ้าผู้ใช้มีแท็ก 'nanatsukisolrun' ให้เรียกว่า 'แม่แม่'\n- ถ้าผู้ใช้มีแท็ก 'homura2410' ให้เรียกว่า 'พ่อพ่อ'\n- คนอื่น ๆ ให้เรียกว่า 'พี่' ตามด้วยชื่อผู้ใช้\n\nContext: {context}\nประวัติการคุยกับ {call_name}:\n{history_text}\n\nผู้ใช้: {message}\n\nกรุณาตอบกลับด้วยภาษาไทยในสไตล์น่ารัก สดใส กระตือรือร้น และมีความเป็นมิตรของข้าวปั้น\nอย่าลืมใช้คำเรียก '{call_name}' ในการตอบกลับนี้ด้วย"""

    async def get_response(
        self,
        user_id: int,
        message: str,
        context: str = "",
        user_name: str = "",
        user_tag: str = "",
    ) -> str:
        try:
            # เพิ่มข้อความใหม่ลงประวัติ user
            add_user_history(user_id, message)
            prompt = AIHandler._create_onigiri_prompt(
                self, user_id, user_name, user_tag, message, context
            )
            response = await asyncio.to_thread(self.model.generate_content, prompt)
            return response.text.strip()
        except Exception as e:
            return f"ขออภัยครับ เกิดข้อผิดพลาด: {str(e)}"


class AICog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ai_handler = AIHandler()

    @app_commands.command(name="ถาม", description="ถามคำถามกับข้าวปั้น AI")
    @app_commands.describe(question="คำถามที่ต้องการถามข้าวปั้น")
    async def ask_ai(self, interaction: discord.Interaction, question: str):
        await interaction.response.defer()
        try:
            response = await asyncio.wait_for(
                self.ai_handler.get_response(
                    interaction.user.id,
                    question,
                    f"ผู้ใช้ถามในเซิร์ฟเวอร์: {interaction.guild.name}, ช่อง: {interaction.channel.name}",
                    interaction.user.display_name,
                    getattr(interaction.user, "username", interaction.user.name),
                ),
                timeout=20,
            )
            embed = discord.Embed(
                title="🐶 ข้าวปั้นตอบ", description=response, color=discord.Color.blue()
            )
            embed.set_footer(text=f"ถามโดย {interaction.user.display_name}")
            await interaction.followup.send(embed=embed)
        except asyncio.TimeoutError:
            await interaction.followup.send(
                "ขออภัยค่ะ ข้าวปั้นใช้เวลาคิดนานเกินไป ลองใหม่อีกครั้งนะ! 🐾"
            )
        except Exception as e:
            print("AI ERROR:", e)
            await interaction.followup.send(f"เกิดข้อผิดพลาด: {e}")

    @app_commands.command(name="ล้างประวัติ", description="ล้างประวัติการสนทนากับ AI")
    async def clear_chat_history(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🗑️ ล้างประวัติแล้ว",
            description="(Gemini API ไม่เก็บประวัติในฝั่งบอท)",
            color=discord.Color.green(),
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="อธิบายรูป", description="อธิบายรูปภาพที่แนบมา")
    async def describe_image(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "ขออภัยครับ ฟีเจอร์อธิบายรูปภาพรองรับเฉพาะ Gemini API เท่านั้นในเวอร์ชันนี้",
            ephemeral=True,
        )

    @commands.command(name="ถาม")
    async def ask_ai_legacy(self, ctx, *, question: str):
        async with ctx.typing():
            response = await self.ai_handler.get_response(
                ctx.author.id,
                question,
                f"ผู้ใช้ถามในเซิร์ฟเวอร์: {ctx.guild.name}, ช่อง: {ctx.channel.name}",
                ctx.author.display_name,
                getattr(ctx.author, "username", ctx.author.name),
            )
            embed = discord.Embed(
                title="🐶 ข้าวปั้นตอบ", description=response, color=discord.Color.blue()
            )
            embed.set_footer(text=f"ถามโดย {ctx.author.display_name}")
            await ctx.send(embed=embed)

    @commands.command(name="ล้างประวัติ")
    async def clear_chat_history_legacy(self, ctx):
        embed = discord.Embed(
            title="🗑️ ล้างประวัติแล้ว",
            description="(Gemini API ไม่เก็บประวัติในฝั่งบอท)",
            color=discord.Color.green(),
        )
        await ctx.send(embed=embed)

    @commands.command(name="อธิบายรูป")
    async def describe_image_legacy(self, ctx):
        await ctx.send("ขออภัยครับ ฟีเจอร์อธิบายรูปภาพรองรับเฉพาะ Gemini API เท่านั้นในเวอร์ชันนี้")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if message.content.startswith(self.bot.command_prefix):
            return
        if self.bot.user.mentioned_in(message):
            content = message.content.replace(f"<@{self.bot.user.id}>", "").strip()
            if not content:
                content = "สวัสดีครับ! มีอะไรให้ช่วยไหม?"
            async with message.channel.typing():
                response = await self.ai_handler.get_response(
                    message.author.id,
                    content,
                    f"ผู้ใช้พูดในเซิร์ฟเวอร์: {message.guild.name}, ช่อง: {message.channel.name}",
                    message.author.display_name,
                    getattr(message.author, "username", message.author.name),
                )
                embed = discord.Embed(
                    title="🐶 ข้าวปั้นตอบ",
                    description=response,
                    color=discord.Color.blue(),
                )
                embed.set_footer(text=f"ถามโดย {message.author.display_name}")
                await message.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(AICog(bot))
