import sys

print("========== PYTHON PATH ==========")
print(sys.executable)
print("==================================")

import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
import datetime
import asyncio

# โหลด environment variables
load_dotenv()

# ตั้งค่า intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# สร้าง bot instance
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    """Event ที่ทำงานเมื่อบอทพร้อมใช้งาน"""
    print(f"บอท {bot.user} พร้อมใช้งานแล้ว!")
    print(f"เชื่อมต่อกับเซิร์ฟเวอร์ {len(bot.guilds)} เซิร์ฟเวอร์")

    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f"✅ Sync slash commands สำเร็จ: {len(synced)} คำสั่ง")
    except Exception as e:
        print(f"❌ ไม่สามารถ sync slash commands: {e}")

    # ตั้งสถานะของบอท
    await bot.change_presence(activity=discord.Game(name="/help เพื่อดูคำสั่ง"))


@bot.event
async def on_message(message):
    """Event ที่ทำงานเมื่อมีข้อความใหม่"""
    # ไม่ตอบกลับข้อความของตัวเอง
    if message.author == bot.user:
        return

    # ตรวจสอบคำสั่ง
    await bot.process_commands(message)


# Slash Commands
@bot.tree.command(name="สวัสดี", description="ทักทายข้าวปั้น")
async def hello(interaction: discord.Interaction):
    """คำสั่งทักทาย"""
    user_tag = getattr(interaction.user, "username", interaction.user.name)
    display_name = interaction.user.display_name

    if user_tag == "nanatsukisolrun":
        await interaction.response.send_message("ว่าไงแม่แม่! 🐶")
    elif user_tag == "homura2410":
        await interaction.response.send_message("ว่าไงพ่อพ่อสุดดื้อพุง! 🐶")
    else:
        await interaction.response.send_message(f"ว่าไง พี่{display_name}! 🐶")


@bot.tree.command(name="เวลา", description="แสดงเวลาปัจจุบัน")
async def time(interaction: discord.Interaction):
    """แสดงเวลาปัจจุบัน"""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    embed = discord.Embed(
        title="🕐 เวลาปัจจุบัน",
        description=f"**{current_time}**",
        color=discord.Color.blue(),
    )
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="ข้อมูล", description="แสดงข้อมูลเซิร์ฟเวอร์")
async def info(interaction: discord.Interaction):
    """แสดงข้อมูลเซิร์ฟเวอร์"""
    guild = interaction.guild
    embed = discord.Embed(
        title=f"📊 ข้อมูลเซิร์ฟเวอร์ {guild.name}", color=discord.Color.green()
    )
    embed.add_field(name="👥 จำนวนสมาชิก", value=guild.member_count, inline=True)
    embed.add_field(
        name="📅 สร้างเมื่อ", value=guild.created_at.strftime("%Y-%m-%d"), inline=True
    )
    embed.add_field(name="👑 เจ้าของ", value=guild.owner.mention, inline=True)
    embed.add_field(name="📝 จำนวนช่อง", value=len(guild.channels), inline=True)
    embed.add_field(name="🎭 จำนวนโรล", value=len(guild.roles), inline=True)

    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)

    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="สุ่ม", description="สุ่มตัวเลขระหว่างค่าที่กำหนด")
@app_commands.describe(min_num="ค่าต่ำสุด (ค่าเริ่มต้น: 1)", max_num="ค่าสูงสุด (ค่าเริ่มต้น: 100)")
async def random_number(
    interaction: discord.Interaction, min_num: int = 1, max_num: int = 100
):
    """สุ่มตัวเลขระหว่างค่าที่กำหนด"""
    import random

    if min_num > max_num:
        min_num, max_num = max_num, min_num

    result = random.randint(min_num, max_num)
    embed = discord.Embed(
        title="🎲 สุ่มตัวเลข", description=f"**{result}**", color=discord.Color.purple()
    )
    embed.add_field(name="ช่วง", value=f"{min_num} - {max_num}", inline=True)
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="ล้าง", description="ลบข้อความจำนวนที่กำหนด (ต้องมีสิทธิ์จัดการข้อความ)")
@app_commands.describe(amount="จำนวนข้อความที่ต้องการลบ (ค่าเริ่มต้น: 5)")
@app_commands.default_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, amount: int = 5):
    """ลบข้อความจำนวนที่กำหนด (ต้องมีสิทธิ์จัดการข้อความ)"""
    if amount > 100:
        amount = 100

    # ตรวจสอบสิทธิ์
    if not interaction.channel.permissions_for(interaction.user).manage_messages:
        await interaction.response.send_message("❌ คุณไม่มีสิทธิ์ใช้คำสั่งนี้", ephemeral=True)
        return

    deleted = await interaction.channel.purge(limit=amount)
    embed = discord.Embed(
        title="🗑️ ลบข้อความแล้ว",
        description=f"ลบข้อความ **{len(deleted)}** ข้อความ",
        color=discord.Color.red(),
    )
    await interaction.response.send_message(embed=embed, delete_after=5)


@bot.tree.command(name="ping", description="ตรวจสอบความเร็วการตอบสนองของบอท")
async def ping(interaction: discord.Interaction):
    """ตรวจสอบความเร็วการตอบสนองของบอท"""
    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"ความเร็วการตอบสนอง: **{latency}ms**",
        color=(
            discord.Color.green()
            if latency < 100
            else discord.Color.yellow() if latency < 200 else discord.Color.red()
        ),
    )
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="ช่วยเหลือ", description="แสดงคำสั่งที่มีอยู่")
async def help_custom(interaction: discord.Interaction):
    """แสดงคำสั่งที่มีอยู่"""
    embed = discord.Embed(
        title="🤖 คำสั่งบอทดิสคอร์ด",
        description="รายการคำสั่งที่สามารถใช้งานได้",
        color=discord.Color.blue(),
    )

    # คำสั่งพื้นฐาน
    basic_commands = [
        ("/สวัสดี", "ทักทายบอท"),
        ("/เวลา", "แสดงเวลาปัจจุบัน"),
        ("/ข้อมูล", "แสดงข้อมูลเซิร์ฟเวอร์"),
        ("/สุ่ม [min] [max]", "สุ่มตัวเลขระหว่างค่าที่กำหนด"),
        ("/ล้าง [จำนวน]", "ลบข้อความ (ต้องมีสิทธิ์)"),
        ("/ping", "ตรวจสอบความเร็วการตอบสนอง"),
    ]

    embed.add_field(
        name="📝 คำสั่งพื้นฐาน",
        value="\n".join([f"`{cmd}` - {desc}" for cmd, desc in basic_commands]),
        inline=False,
    )

    # คำสั่ง AI
    ai_commands = [
        ("/ถาม [คำถาม]", "ถามคำถามกับ AI"),
        ("/อธิบายรูป", "อธิบายรูปภาพที่แนบมา"),
        ("/ล้างประวัติ", "ล้างประวัติการสนทนากับ AI"),
        ("@บอท [ข้อความ]", "พูดคุยกับ AI โดยตรง"),
    ]

    embed.add_field(
        name="🤖 คำสั่ง AI",
        value="\n".join([f"`{cmd}` - {desc}" for cmd, desc in ai_commands]),
        inline=False,
    )

    # คำสั่งเสียง
    voice_commands = [
        ("/เข้าร่วม", "เข้าร่วมช่องเสียง"),
        ("/ออก", "ออกจากช่องเสียง"),
        ("/พูด [ข้อความ]", "ให้บอทพูดข้อความ"),
        ("/หยุด", "หยุดการพูด"),
        ("/เสียง", "แสดงสถานะการเชื่อมต่อเสียง"),
    ]

    embed.add_field(
        name="🎵 คำสั่งเสียง",
        value="\n".join([f"`{cmd}` - {desc}" for cmd, desc in voice_commands]),
        inline=False,
    )

    embed.set_footer(text="ใช้ /help เพื่อดูคำสั่งเพิ่มเติม")
    await interaction.response.send_message(embed=embed)


@bot.command(name="เวลา")
async def time_legacy(ctx):
    """แสดงเวลาปัจจุบัน (legacy)"""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    embed = discord.Embed(
        title="🕐 เวลาปัจจุบัน",
        description=f"**{current_time}**",
        color=discord.Color.blue(),
    )
    await ctx.send(embed=embed)


@bot.command(name="ข้อมูล")
async def info_legacy(ctx):
    """แสดงข้อมูลเซิร์ฟเวอร์ (legacy)"""
    guild = ctx.guild
    embed = discord.Embed(
        title=f"📊 ข้อมูลเซิร์ฟเวอร์ {guild.name}", color=discord.Color.green()
    )
    embed.add_field(name="👥 จำนวนสมาชิก", value=guild.member_count, inline=True)
    embed.add_field(
        name="📅 สร้างเมื่อ", value=guild.created_at.strftime("%Y-%m-%d"), inline=True
    )
    embed.add_field(name="👑 เจ้าของ", value=guild.owner.mention, inline=True)
    embed.add_field(name="📝 จำนวนช่อง", value=len(guild.channels), inline=True)
    embed.add_field(name="🎭 จำนวนโรล", value=len(guild.roles), inline=True)

    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)

    await ctx.send(embed=embed)


@bot.command(name="สุ่ม")
async def random_number_legacy(ctx, min_num: int = 1, max_num: int = 100):
    """สุ่มตัวเลขระหว่างค่าที่กำหนด (legacy)"""
    import random

    if min_num > max_num:
        min_num, max_num = max_num, min_num

    result = random.randint(min_num, max_num)
    embed = discord.Embed(
        title="🎲 สุ่มตัวเลข", description=f"**{result}**", color=discord.Color.purple()
    )
    embed.add_field(name="ช่วง", value=f"{min_num} - {max_num}", inline=True)
    await ctx.send(embed=embed)


@bot.command(name="ล้าง")
@commands.has_permissions(manage_messages=True)
async def clear_legacy(ctx, amount: int = 5):
    """ลบข้อความจำนวนที่กำหนด (legacy)"""
    if amount > 100:
        amount = 100

    deleted = await ctx.channel.purge(limit=amount + 1)  # +1 เพื่อรวมข้อความคำสั่ง
    embed = discord.Embed(
        title="🗑️ ลบข้อความแล้ว",
        description=f"ลบข้อความ **{len(deleted)-1}** ข้อความ",
        color=discord.Color.red(),
    )
    await ctx.send(embed=embed, delete_after=5)


@bot.command(name="ping")
async def ping_legacy(ctx):
    """ตรวจสอบความเร็วการตอบสนองของบอท (legacy)"""
    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"ความเร็วการตอบสนอง: **{latency}ms**",
        color=(
            discord.Color.green()
            if latency < 100
            else discord.Color.yellow() if latency < 200 else discord.Color.red()
        ),
    )
    await ctx.send(embed=embed)


@bot.command(name="ช่วยเหลือ")
async def help_custom_legacy(ctx):
    """แสดงคำสั่งที่มีอยู่ (legacy)"""
    embed = discord.Embed(
        title="🤖 คำสั่งบอทดิสคอร์ด",
        description="รายการคำสั่งที่สามารถใช้งานได้",
        color=discord.Color.blue(),
    )

    # คำสั่งพื้นฐาน
    basic_commands = [
        ("/สวัสดี", "ทักทายบอท"),
        ("/เวลา", "แสดงเวลาปัจจุบัน"),
        ("/ข้อมูล", "แสดงข้อมูลเซิร์ฟเวอร์"),
        ("/สุ่ม [min] [max]", "สุ่มตัวเลขระหว่างค่าที่กำหนด"),
        ("/ล้าง [จำนวน]", "ลบข้อความ (ต้องมีสิทธิ์)"),
        ("/ping", "ตรวจสอบความเร็วการตอบสนอง"),
    ]

    embed.add_field(
        name="📝 คำสั่งพื้นฐาน",
        value="\n".join([f"`{cmd}` - {desc}" for cmd, desc in basic_commands]),
        inline=False,
    )

    # คำสั่ง AI
    ai_commands = [
        ("/ถาม [คำถาม]", "ถามคำถามกับ AI"),
        ("/อธิบายรูป", "อธิบายรูปภาพที่แนบมา"),
        ("/ล้างประวัติ", "ล้างประวัติการสนทนากับ AI"),
        ("@บอท [ข้อความ]", "พูดคุยกับ AI โดยตรง"),
    ]

    embed.add_field(
        name="🤖 คำสั่ง AI",
        value="\n".join([f"`{cmd}` - {desc}" for cmd, desc in ai_commands]),
        inline=False,
    )

    # คำสั่งเสียง
    voice_commands = [
        ("/เข้าร่วม", "เข้าร่วมช่องเสียง"),
        ("/ออก", "ออกจากช่องเสียง"),
        ("/พูด [ข้อความ]", "ให้บอทพูดข้อความ"),
        ("/หยุด", "หยุดการพูด"),
        ("/เสียง", "แสดงสถานะการเชื่อมต่อเสียง"),
    ]

    embed.add_field(
        name="🎵 คำสั่งเสียง",
        value="\n".join([f"`{cmd}` - {desc}" for cmd, desc in voice_commands]),
        inline=False,
    )

    embed.set_footer(text="ใช้ /help เพื่อดูคำสั่งเพิ่มเติม")
    await ctx.send(embed=embed)


# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ คุณไม่มีสิทธิ์ใช้คำสั่งนี้")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ กรุณาระบุพารามิเตอร์ที่จำเป็น")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ พารามิเตอร์ไม่ถูกต้อง")
    else:
        await ctx.send(f"❌ เกิดข้อผิดพลาด: {error}")


# โหลด Cogs
async def load_extensions():
    """โหลด extensions ทั้งหมด"""
    try:
        await bot.load_extension("ai_handler")
        print("✅ โหลด AI Handler สำเร็จ")
    except Exception as e:
        print(f"❌ ไม่สามารถโหลด AI Handler: {e}")

    try:
        await bot.load_extension("voice_handler")
        print("✅ โหลด Voice Handler สำเร็จ")
    except Exception as e:
        print(f"❌ ไม่สามารถโหลด Voice Handler: {e}")
        try:
            await bot.load_extension("voice_handler_simple")
            print("✅ โหลด Simple Voice Handler สำเร็จ")
        except Exception as e2:
            print(f"❌ ไม่สามารถโหลด Simple Voice Handler: {e2}")


# รันบอท
async def main():
    """ฟังก์ชันหลักสำหรับรันบอท"""
    async with bot:
        await load_extensions()
        await bot.start(os.getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_TOKEN")
    if TOKEN:
        asyncio.run(main())
    else:
        print("กรุณาตั้งค่า DISCORD_TOKEN ในไฟล์ .env")
