import discord
from discord.ext import commands
import datetime

class send_help_comand:
    bot = None  # Атрибут класу для збереження об'єкта бота
    
    def __init__(self):
        pass
    async def help_comand(self, ctx, command=None):
        if command is None:
            message = "**Список команд:**\n!time @TagUser\n!alltime\n!skill @TagUser або UMMA\n!vinfo\n!clear\n**Якщо потрібна детальна інформація про команду:**\n!help command"
            embed = discord.Embed(description=message, color=0xFF5733)
            await ctx.send(embed=embed)
            return
        if command == 'time':
            message = "**Команда !time:**\n**Синтаксис:**!time @Тег-гравця інформацію про якого потрібно розрахувати\n**Команда необхідна для** розрахунку загальної кількості годин гравця\n@тег якого введений після !time інформація береться з чату\n**data-time** та підраховуєтся."
            embed = discord.Embed(description=message, color=0xFF5733)
            await ctx.send(embed=embed)
            return
        if command == 'alltime':
            message = "**Команда !alltime:**\n**Синтаксис:**!time @Тег-гравця інформацію про якого потрібно розрахувати\n**Команда необхідна для** розрахунку загальної кількості годин всіх гравців\n для команди !alltime інформація береться з чату\n**data-time** та підраховуєтся."
            embed = discord.Embed(description=message, color=0xFF5733)
            await ctx.send(embed=embed)
            return
        if command == 'skill':
            message = "**Команда !skill:**\n**Синтаксис:**!skill @Тег-гравця посилання на профіль сайту Thunder Skill\n якого треба отримати або якщо після !skill введено UMMA то буде дано посилання\nна загальну статистику гравців полку."
            embed = discord.Embed(description=message, color=0xFF5733)
            await ctx.send(embed=embed)
            return
        if command == 'vinfo':
            message = "**Команда !vinfo:**\n**Синтаксис:**!vinfo \nНадає інформацію про версію бота."
            embed = discord.Embed(description=message, color=0xFF5733)
            await ctx.send(embed=embed)
            return
        if command == 'clear':
            message = "**Команда !clear:**\n**Синтаксис:**!clear \nОчищює чат data-time **Потрібен дозвіл на використання**."
            embed = discord.Embed(description=message, color=0xFF5733)
            await ctx.send(embed=embed)
            return