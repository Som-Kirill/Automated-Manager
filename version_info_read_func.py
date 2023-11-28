import discord

#Модулі програм
from config_work_func import ConfigReader

class read_info_file:
    bot = None  # Атрибут класу для збереження об'єкта бота
    def __init__(self):
        pass
    async def read_info(self, ctx):
        #config
        config_reader = ConfigReader()
        config = config_reader.config
        
        channel = read_info_file.bot.get_channel(config['channel_of_sending_invites'])
        
        with open('version_info.txt', 'r', encoding='utf-8') as file:
            text_content = file.read()
        message = text_content
        embed = discord.Embed(description=message, color=0x808080)
        await channel.send(embed=embed)