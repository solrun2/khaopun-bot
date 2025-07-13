import discord
from discord.ext import commands
import asyncio
import os
import tempfile
import pyttsx3
from dotenv import load_dotenv

load_dotenv()


class SimpleVoiceHandler:
    def __init__(self):
        self.voice_clients = {}

        # ตั้งค่า Text-to-Speech
        try:
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty("rate", 150)  # ความเร็วในการพูด
            self.tts_engine.setProperty("volume", 0.9)  # ความดัง
            self.tts_available = True
        except Exception as e:
            print(f"ไม่สามารถเริ่มต้น TTS engine: {e}")
            self.tts_available = False

    def text_to_speech(self, text: str, filename: str):
        """แปลงข้อความเป็นเสียง"""
        if not self.tts_available:
            return False

        try:
            self.tts_engine.save_to_file(text, filename)
            self.tts_engine.runAndWait()
            return True
        except Exception as e:
            print(f"ข้อผิดพลาดในการแปลงข้อความเป็นเสียง: {e}")
            return False


class SimpleVoiceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_handler = SimpleVoiceHandler()

    @commands.command(name="เข้าร่วม")
    async def join_voice(self, ctx):
        """เข้าร่วมช่องเสียง"""
        if not ctx.author.voice:
            await ctx.send("❌ คุณต้องอยู่ในช่องเสียงก่อน")
            return

        voice_channel = ctx.author.voice.channel

        try:
            voice_client = await voice_channel.connect()
            self.voice_handler.voice_clients[ctx.guild.id] = voice_client

            embed = discord.Embed(
                title="🎵 เข้าร่วมช่องเสียงแล้ว",
                description=f"เข้าร่วมช่อง: **{voice_channel.name}**",
                color=discord.Color.green(),
            )
            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"❌ ไม่สามารถเข้าร่วมช่องเสียงได้: {e}")

    @commands.command(name="ออก")
    async def leave_voice(self, ctx):
        """ออกจากช่องเสียง"""
        if ctx.guild.id not in self.voice_handler.voice_clients:
            await ctx.send("❌ บอทไม่ได้อยู่ในช่องเสียง")
            return

        voice_client = self.voice_handler.voice_clients[ctx.guild.id]
        await voice_client.disconnect()
        del self.voice_handler.voice_clients[ctx.guild.id]

        embed = discord.Embed(title="👋 ออกจากช่องเสียงแล้ว", color=discord.Color.red())
        await ctx.send(embed=embed)

    @commands.command(name="พูด")
    async def speak(self, ctx, *, text: str):
        """ให้บอทพูดข้อความที่กำหนด"""
        if ctx.guild.id not in self.voice_handler.voice_clients:
            await ctx.send("❌ บอทไม่ได้อยู่ในช่องเสียง กรุณาใช้คำสั่ง `!เข้าร่วม` ก่อน")
            return

        if not self.voice_handler.tts_available:
            await ctx.send("❌ ระบบ TTS ไม่พร้อมใช้งาน กรุณาติดตั้ง pyttsx3")
            return

        voice_client = self.voice_handler.voice_clients[ctx.guild.id]

        # สร้างไฟล์เสียงชั่วคราว
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            temp_filename = temp_file.name

        # แปลงข้อความเป็นเสียง
        success = self.voice_handler.text_to_speech(text, temp_filename)

        if success:
            try:
                # เล่นเสียง
                voice_client.play(discord.FFmpegPCMAudio(temp_filename))

                embed = discord.Embed(
                    title="🗣️ กำลังพูด",
                    description=f"**{text}**",
                    color=discord.Color.blue(),
                )
                await ctx.send(embed=embed)

                # รอให้เล่นเสร็จแล้วลบไฟล์
                while voice_client.is_playing():
                    await asyncio.sleep(1)

                os.unlink(temp_filename)

            except Exception as e:
                await ctx.send(f"❌ ข้อผิดพลาดในการเล่นเสียง: {e}")
                if os.path.exists(temp_filename):
                    os.unlink(temp_filename)
        else:
            await ctx.send("❌ ไม่สามารถแปลงข้อความเป็นเสียงได้")

    @commands.command(name="หยุด")
    async def stop_speaking(self, ctx):
        """หยุดการพูด"""
        if ctx.guild.id not in self.voice_handler.voice_clients:
            await ctx.send("❌ บอทไม่ได้อยู่ในช่องเสียง")
            return

        voice_client = self.voice_handler.voice_clients[ctx.guild.id]
        if voice_client.is_playing():
            voice_client.stop()
            embed = discord.Embed(title="⏹️ หยุดการพูดแล้ว", color=discord.Color.orange())
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ ไม่มีการพูดอยู่")

    @commands.command(name="เสียง")
    async def voice_status(self, ctx):
        """แสดงสถานะการเชื่อมต่อเสียง"""
        if ctx.guild.id in self.voice_handler.voice_clients:
            voice_client = self.voice_handler.voice_clients[ctx.guild.id]
            channel_name = voice_client.channel.name
            is_playing = voice_client.is_playing()

            embed = discord.Embed(title="🎵 สถานะเสียง", color=discord.Color.green())
            embed.add_field(name="ช่อง", value=channel_name, inline=True)
            embed.add_field(
                name="กำลังเล่น", value="ใช่" if is_playing else "ไม่", inline=True
            )
            embed.add_field(name="เชื่อมต่อ", value="ใช่", inline=True)
            embed.add_field(
                name="TTS พร้อม",
                value="ใช่" if self.voice_handler.tts_available else "ไม่",
                inline=True,
            )
        else:
            embed = discord.Embed(
                title="🎵 สถานะเสียง",
                description="ไม่ได้เชื่อมต่อกับช่องเสียง",
                color=discord.Color.red(),
            )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(SimpleVoiceCog(bot))
