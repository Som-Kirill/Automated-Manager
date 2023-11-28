import discord

#Модулі програм
from config_work_func import ConfigReader

class clear_data:
    bot = None  # Атрибут класу для збереження об'єкта бота
    def __init__(self):
        pass
    async def clear(self, ctx):
        #config
        config_reader = ConfigReader()
        config = config_reader.config
        
        # Перевірка на наявність прав "Manage Messages" у бота та користувача
        if ctx.author.guild_permissions.manage_messages:
            # Знаходимо канал за ID
            channel = clear_data.bot.get_channel(config['channel_sending_data_time_id'])
            # Використовуємо метод purge() для очищення усього чату
            await channel.purge(limit=None)
            message = f'user-data ОЧИЩЕНО'
            embed = discord.Embed(description=message, color=0x008000)
            await ctx.send(embed=embed)
        else:
            message = f'У бота немає дозволу на виконання цієї команди.'
            embed = discord.Embed(description=message, color=0xFF0000)
            await ctx.send(embed=embed)
        