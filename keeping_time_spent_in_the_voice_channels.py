import discord
from discord.ext import commands
import datetime

#Модулі програм
from config_work_func import ConfigReader

class keeping_time_spent_in_voice_channels:
    bot = None  # Атрибут класу для збереження об'єкта бота

    def __init__(self, voice_times = {}, massage_var = 0):
        self.voice_times = voice_times # Словник для збереження даних про час учасників у голосових каналах
        self.massage_var = massage_var
    
    async def on_voice_state_update(self, member, before, after):
        #config
        config_reader = ConfigReader()
        config = config_reader.config
        
        if before.channel != after.channel:
            # Перевіряємо, чи користувач не зайшов у AFK-канал
            if after.channel is not None and after.channel.id == config['afk_channel_id']:
                if member.id in self.voice_times:
                    duration = datetime.datetime.now() - self.voice_times[member.id]
                    del self.voice_times[member.id]
                    minutes = int(duration.total_seconds())
                    if minutes >= config['the_number_of_minutes_required_to_save']:
                        # Використовуємо атрибут класу bot для отримання об'єкта бота
                        channel_id = config['channel_sending_data_time_id']
                        channel = keeping_time_spent_in_voice_channels.bot.get_channel(channel_id)

                        self.massage_var = minutes

                        async for message in channel.history(limit=None):
                            if message.author == keeping_time_spent_in_voice_channels.bot.user:
                                if member.mention in message.content.lower():

                                    massage = message.content
                                    massage = massage.split('|')
                                    print(f'{member.mention}|{self.massage_var} + {int(massage[1])}')
                                    self.massage_var += int(massage[1])

                                    # Отримання об'єкта текстового каналу за його ID
                                    channel = keeping_time_spent_in_voice_channels.bot.get_channel(channel_id)
                                    # Отримання об'єкта повідомлення за його ID
                                    message = await channel.fetch_message(message.id)
                                    # Видалення повідомлення
                                    await message.delete()

                                    break

                        await channel.send(f"{member.mention}|{self.massage_var}")
                return
            
            # Учасник приєднався до голосового каналу
            if before.channel is None and after.channel is not None:
                self.voice_times[member.id] = datetime.datetime.now()


            # Учасник вийшов з голосового каналу
            elif before.channel is not None and after.channel is None:
                if member.id in self.voice_times:
                    duration = datetime.datetime.now() - self.voice_times[member.id]
                    del self.voice_times[member.id]
                    minutes = int(duration.total_seconds())
                    if minutes >= config['the_number_of_minutes_required_to_save']:
                        # Використовуємо атрибут класу bot для отримання об'єкта бота
                        channel_id = config['channel_sending_data_time_id']
                        channel = keeping_time_spent_in_voice_channels.bot.get_channel(channel_id)
                        
                        self.massage_var = minutes
                        
                        async for message in channel.history(limit=None):
                            if message.author == keeping_time_spent_in_voice_channels.bot.user:
                                if member.mention in message.content.lower():
                                    
                                    massage = message.content
                                    massage = massage.split('|')
                                    self.massage_var += int(massage[1])
                                    
                                    # Отримання об'єкта текстового каналу за його ID
                                    channel = keeping_time_spent_in_voice_channels.bot.get_channel(channel_id)
                                    # Отримання об'єкта повідомлення за його ID
                                    message = await channel.fetch_message(message.id)
                                    # Видалення повідомлення
                                    await message.delete()
                                    
                                    break
                        
                        await channel.send(f"{member.mention}|{self.massage_var}")
            # Блок для перевірки, чи користувач перейшов з AFK-каналу в будь-який інший канал
            elif before.channel is not None and before.channel.id == config['afk_channel_id'] and after.channel is not None:
                self.voice_times[member.id] = datetime.datetime.now()
