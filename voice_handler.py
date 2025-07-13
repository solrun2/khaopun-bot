import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import os
import tempfile
import speech_recognition as sr
import pyttsx3
import threading
import queue
from dotenv import load_dotenv

load_dotenv()


class VoiceHandler:
    def __init__(self):
        self.voice_clients = {}
        self.audio_queue = queue.Queue()
        self.is_speaking = False

        # ตั้งค่า Text-to-Speech
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty("rate", 150)  # ความเร็วในการพูด
        self.tts_engine.setProperty("volume", 0.9)  # ความดัง

        # ตั้งค่า Speech Recognition
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True

    def text_to_speech(self, text: str, filename: str):
        """แปลงข้อความเป็นเสียง"""
        try:
            self.tts_engine.save_to_file(text, filename)
            self.tts_engine.runAndWait()
            return True
        except Exception as e:
            print(f"ข้อผิดพลาดในการแปลงข้อความเป็นเสียง: {e}")
            return False

    async def speech_to_text(self, audio_data) -> str:
        """แปลงเสียงเป็นข้อความ"""
        try:
            # บันทึกไฟล์เสียงชั่วคราว
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                temp_file.write(audio_data)
                temp_file_path = temp_file.name

            # ใช้ Speech Recognition
            with sr.AudioFile(temp_file_path) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio, language="th-TH")

            # ลบไฟล์ชั่วคราว
            os.unlink(temp_file_path)
            return text

        except sr.UnknownValueError:
            return "ไม่สามารถเข้าใจเสียงได้"
        except sr.RequestError as e:
            return f"ข้อผิดพลาดในการประมวลผลเสียง: {e}"
        except Exception as e:
            return f"ข้อผิดพลาด: {e}"


class VoiceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_handler = VoiceHandler()

    # Slash Commands
    @app_commands.command(name="เข้าร่วม", description="เข้าร่วมช่องเสียง")
    async def join_voice(self, interaction: discord.Interaction):
        """เข้าร่วมช่องเสียง"""
        if not interaction.user.voice:
            await interaction.response.send_message(
                "❌ คุณต้องอยู่ในช่องเสียงก่อน", ephemeral=True
            )
            return

        voice_channel = interaction.user.voice.channel

        try:
            voice_client = await voice_channel.connect()
            self.voice_handler.voice_clients[interaction.guild.id] = voice_client

            embed = discord.Embed(
                title="🎵 เข้าร่วมช่องเสียงแล้ว",
                description=f"เข้าร่วมช่อง: **{voice_channel.name}**",
                color=discord.Color.green(),
            )
            await interaction.response.send_message(embed=embed)

        except Exception as e:
            await interaction.response.send_message(
                f"❌ ไม่สามารถเข้าร่วมช่องเสียงได้: {e}", ephemeral=True
            )

    @app_commands.command(name="ออก", description="ออกจากช่องเสียง")
    async def leave_voice(self, interaction: discord.Interaction):
        """ออกจากช่องเสียง"""
        if interaction.guild.id not in self.voice_handler.voice_clients:
            await interaction.response.send_message(
                "❌ บอทไม่ได้อยู่ในช่องเสียง", ephemeral=True
            )
            return

        voice_client = self.voice_handler.voice_clients[interaction.guild.id]
        await voice_client.disconnect()
        del self.voice_handler.voice_clients[interaction.guild.id]

        embed = discord.Embed(title="👋 ออกจากช่องเสียงแล้ว", color=discord.Color.red())
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="พูด", description="ให้บอทพูดข้อความที่กำหนด")
    @app_commands.describe(text="ข้อความที่ต้องการให้บอทพูด")
    async def speak(self, interaction: discord.Interaction, text: str):
        """ให้บอทพูดข้อความที่กำหนด"""
        if interaction.guild.id not in self.voice_handler.voice_clients:
            await interaction.response.send_message(
                "❌ บอทไม่ได้อยู่ในช่องเสียง กรุณาใช้คำสั่ง `/เข้าร่วม` ก่อน", ephemeral=True
            )
            return

        voice_client = self.voice_handler.voice_clients[interaction.guild.id]

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
                await interaction.response.send_message(embed=embed)

                # รอให้เล่นเสร็จแล้วลบไฟล์
                while voice_client.is_playing():
                    await asyncio.sleep(1)

                os.unlink(temp_filename)

            except Exception as e:
                await interaction.followup.send(
                    f"❌ ข้อผิดพลาดในการเล่นเสียง: {e}", ephemeral=True
                )
                if os.path.exists(temp_filename):
                    os.unlink(temp_filename)
        else:
            await interaction.response.send_message(
                "❌ ไม่สามารถแปลงข้อความเป็นเสียงได้", ephemeral=True
            )

    @app_commands.command(name="หยุด", description="หยุดการพูด")
    async def stop_speaking(self, interaction: discord.Interaction):
        """หยุดการพูด"""
        if interaction.guild.id not in self.voice_handler.voice_clients:
            await interaction.response.send_message(
                "❌ บอทไม่ได้อยู่ในช่องเสียง", ephemeral=True
            )
            return

        voice_client = self.voice_handler.voice_clients[interaction.guild.id]
        if voice_client.is_playing():
            voice_client.stop()
            embed = discord.Embed(title="⏹️ หยุดการพูดแล้ว", color=discord.Color.orange())
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ ไม่มีการพูดอยู่", ephemeral=True)

    @app_commands.command(name="เสียง", description="แสดงสถานะการเชื่อมต่อเสียง")
    async def voice_status(self, interaction: discord.Interaction):
        """แสดงสถานะการเชื่อมต่อเสียง"""
        if interaction.guild.id in self.voice_handler.voice_clients:
            voice_client = self.voice_handler.voice_clients[interaction.guild.id]
            channel_name = voice_client.channel.name
            is_playing = voice_client.is_playing()

            embed = discord.Embed(title="🎵 สถานะเสียง", color=discord.Color.green())
            embed.add_field(name="ช่อง", value=channel_name, inline=True)
            embed.add_field(
                name="กำลังเล่น", value="ใช่" if is_playing else "ไม่", inline=True
            )
            embed.add_field(name="เชื่อมต่อ", value="ใช่", inline=True)
        else:
            embed = discord.Embed(
                title="🎵 สถานะเสียง",
                description="ไม่ได้เชื่อมต่อกับช่องเสียง",
                color=discord.Color.red(),
            )

        await interaction.response.send_message(embed=embed)

    # Legacy prefix commands (สำหรับการใช้งานแบบเก่า)
    @commands.command(name="เข้าร่วม")
    async def join_voice_legacy(self, ctx):
        """เข้าร่วมช่องเสียง (legacy)"""
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
    async def leave_voice_legacy(self, ctx):
        """ออกจากช่องเสียง (legacy)"""
        if ctx.guild.id not in self.voice_handler.voice_clients:
            await ctx.send("❌ บอทไม่ได้อยู่ในช่องเสียง")
            return

        voice_client = self.voice_handler.voice_clients[ctx.guild.id]
        await voice_client.disconnect()
        del self.voice_handler.voice_clients[ctx.guild.id]

        embed = discord.Embed(title="👋 ออกจากช่องเสียงแล้ว", color=discord.Color.red())
        await ctx.send(embed=embed)

    @commands.command(name="พูด")
    async def speak_legacy(self, ctx, *, text: str):
        """ให้บอทพูดข้อความที่กำหนด (legacy)"""
        if ctx.guild.id not in self.voice_handler.voice_clients:
            await ctx.send("❌ บอทไม่ได้อยู่ในช่องเสียง กรุณาใช้คำสั่ง `!เข้าร่วม` ก่อน")
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
    async def stop_speaking_legacy(self, ctx):
        """หยุดการพูด (legacy)"""
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
    async def voice_status_legacy(self, ctx):
        """แสดงสถานะการเชื่อมต่อเสียง (legacy)"""
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
        else:
            embed = discord.Embed(
                title="🎵 สถานะเสียง",
                description="ไม่ได้เชื่อมต่อกับช่องเสียง",
                color=discord.Color.red(),
            )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(VoiceCog(bot))
