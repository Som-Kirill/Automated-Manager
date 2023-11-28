import discord
from discord.ext import commands

#Модулі програм
from config_work_func import ConfigReader

class another_game_create:
    bot = None  # Атрибут класу для збереження об'єкта бота
    def __init__(self):
        pass
    async def on_voice_state_update_another_game(self, member, before, after):
        #config
        config_reader = ConfigReader()
        config = config_reader.config
        max_channels = config['max_another_game_channels']

        if after.channel and after.channel.category_id == config['channel_is_another_game_id']:
            category_channels = [channel for channel in after.channel.category.voice_channels if channel.name.startswith('Інша гра')]
            empty_channels = [channel for channel in category_channels if not channel.members]

            if len(category_channels) < max_channels and not empty_channels:
                new_channel_name = f'Інша гра'
                await after.channel.category.create_voice_channel(new_channel_name)

        if before.channel and before.channel.category_id == config['channel_is_another_game_id']:
            category_channels = [channel for channel in before.channel.category.voice_channels if channel.name.startswith('Інша гра')]
            empty_channels = [channel for channel in category_channels if not channel.members]

            if before.channel in empty_channels and len(empty_channels) > 1 and len(category_channels) > 1:
                await before.channel.delete()