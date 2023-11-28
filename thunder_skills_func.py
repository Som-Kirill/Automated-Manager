import discord
from discord.ext import commands

class parser_thunder_skill:
    bot = None  # Атрибут класу для збереження об'єкта бота
    
    def __init__(self):
        pass
    def escape_markdown(text):
        # Замінюємо символи Markdown на еквіваленти з бекслешем перед ними
        # Додаємо бекслеш перед символами _*, `~
        return text.replace('_', r'\_').replace('*', r'\*').replace('`', r'\`').replace('~', r'\~')
    async def parser_skill_comand(self, ctx, user_tag):
        try:
            user = await parser_thunder_skill.bot.fetch_user(int(user_tag.strip('<@!>')))
            member = await ctx.guild.fetch_member(user.id)
            
            nickname = parser_thunder_skill.escape_markdown(member.nick) if member.nick else 'Не встановлено'
            nickname = nickname[:nickname.index('(')]
            nickname = nickname.replace('\_', r'_').replace('\*', r'*').replace('\`', r'`').replace('~', r'~').replace(' ', r'')
            
            url = 'https://thunderskill.com/en/stat/'+nickname
            nickname.replace('_', r'\_').replace('*', r'\*').replace('`', r'\`').replace('~', r'\~')
            message = f'Профіль гравця: **{nickname}** \nна сайті ThunderSkill: {url}'
            embed = discord.Embed(description=message, color=0x0000ff)
            await ctx.send(embed=embed)
        except ValueError:
            message = f'Невідповідний формат нікнейму має бути [нікнейм в грі(ім`я)]'
            embed = discord.Embed(description=message, color=0x0000ff)
            await ctx.send(embed=embed)

#https://thunderskill.com/ru/squad/%5EUMMA%5E