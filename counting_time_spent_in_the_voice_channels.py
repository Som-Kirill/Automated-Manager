import discord
from discord.ext import commands
from discord.utils import get

#Модулі програм
from config_work_func import ConfigReader

class counting_time_in_voice_channels:
    bot = None  # Атрибут класу для збереження об'єкта бота
    
    def __init__(self):
        pass
    
    async def show_total_time(self, ctx, user_tag=None):
        #config
        config_reader = ConfigReader()
        config = config_reader.config
        
        if user_tag is None:
            message = f'Спробуй: **!time @UserTag**'
            embed = discord.Embed(description=message, color=0xFF5733)
            await ctx.send(embed=embed)
            return

        data_channel = counting_time_in_voice_channels.bot.get_channel(config['channel_sending_data_time_id'])

        all_user_database = {}
        time_last_activity_database = {}
        async for message in data_channel.history(limit=None):
            if message.author == counting_time_in_voice_channels.bot.user:
                content = message.content.split('|')
                if content[0] in all_user_database:
                    all_user_database[content[0]] += int(content[1])
                else:
                    all_user_database[content[0]] = int(content[1])
                    message_time = message.created_at
                    time_last_activity_database[content[0]] = message_time.strftime("%d.%m.%Y")

        channel = counting_time_in_voice_channels.bot.get_channel(config['channel_of_sending_invites'])
        if user_tag in all_user_database:
            seconds = all_user_database[user_tag]
            hours, remainder = divmod(seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            
            if len(str(seconds)) < 2:
                seconds = '0'+str(seconds)
            if len(str(minutes)) < 2:
                minutes = '0'+str(minutes)
            if len(str(hours)) < 2:
                hours = '0'+str(hours)
            
            message = f"**Загальний час, який користувач {user_tag}** \nпровів у голосових каналах: **{hours}:{minutes}:{seconds}**\nОстання активність:**{time_last_activity_database[user_tag]}**"
            embed = discord.Embed(description=message, color=0xFF5733)
            await channel.send(embed=embed)
        else:
            message = f"Користувач з тегом {user_tag} **не має записів** про перебування в голосових каналах."
            embed = discord.Embed(description=message, color=0xFF0000)
            await channel.send(embed=embed)

    async def show_total_time_all_user(self, ctx):
        #config
        config_reader = ConfigReader()
        config = config_reader.config
        
        data_channel = counting_time_in_voice_channels.bot.get_channel(config['channel_sending_data_time_id'])
        channel = counting_time_in_voice_channels.bot.get_channel(config['channel_of_sending_invites'])
        
        all_user_database = {}
        time_last_activity_database = {}
        async for message in data_channel.history(limit=None):
            if message.author == counting_time_in_voice_channels.bot.user:
                content = message.content.split('|')
                if content[0] in all_user_database:
                    all_user_database[content[0]] += int(content[1])
                else:
                    all_user_database[content[0]] = int(content[1])
                    message_time = message.created_at
                    time_last_activity_database[content[0]] = message_time.strftime("%d.%m.%Y")
                    
        all_user_database = dict(sorted(all_user_database.items(), key=lambda item: item[1], reverse=True))
        items = all_user_database.items()
        
        good_user_database = {}
        normal_user_database = {}
        bad_user_database = {}
        
        good_user_message = ''
        normal_user_message = ''
        bad_user_message = ''
        
        good_counter = 0
        normal_counter = 0
        bad_counter = 0
        
        counter = 0
        
        for key, value in items:
            if value >= config['more_than_this_value_is_good']:
                good_user_database[key] = value
            if config['more_than_this_value_is_good'] > value >= config['more_than_this_value_is_normal']:
                normal_user_database[key] = value
            if config['more_than_this_value_is_normal'] > value >= config['more_than_this_value_is_bad']:
                bad_user_database[key] = value

        items = good_user_database.items()
        for key, value in items:
            good_counter += 1
            counter += 1
            if good_counter <= 25:
                seconds = good_user_database[key]
                hours, remainder = divmod(seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                
                if len(str(seconds)) < 2:
                    seconds = '0'+str(seconds)
                if len(str(minutes)) < 2:
                    minutes = '0'+str(minutes)
                if len(str(hours)) < 2:
                    hours = '0'+str(hours)
                good_user_message += f"\n**{counter})Загальний час, який користувач {key}** \nпровів у голосових каналах: **{hours}:{minutes}:{seconds}**\nОстання активність:**{time_last_activity_database[key]}**"
            else:
                embed = discord.Embed(description=good_user_database, color=0x008000)
                await channel.send(embed=embed)
                good_user_message = ''
                good_counter = 0
                seconds = good_user_database[key]
                hours, remainder = divmod(seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                
                if len(str(seconds)) < 2:
                    seconds = '0'+str(seconds)
                if len(str(minutes)) < 2:
                    minutes = '0'+str(minutes)
                if len(str(hours)) < 2:
                    hours = '0'+str(hours)
                good_user_message += f"\n**{counter})Загальний час, який користувач {key}** \nпровів у голосових каналах: **{hours}:{minutes}:{seconds}**\nОстання активність:**{time_last_activity_database[key]}**"
        if good_user_message != '':
            embed = discord.Embed(description=good_user_message, color=0x008000)
            await channel.send(embed=embed)


        items = normal_user_database.items()
        for key, value in items:
            normal_counter += 1
            counter += 1
            if normal_counter <= 25:
                seconds = normal_user_database[key]
                hours, remainder = divmod(seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                
                if len(str(seconds)) < 2:
                    seconds = '0'+str(seconds)
                if len(str(minutes)) < 2:
                    minutes = '0'+str(minutes)
                if len(str(hours)) < 2:
                    hours = '0'+str(hours)
                normal_user_message += f"\n**{counter})Загальний час, який користувач {key}** \nпровів у голосових каналах: **{hours}:{minutes}:{seconds}**\nОстання активність:**{time_last_activity_database[key]}**"
            else:
                embed = discord.Embed(description=normal_user_message, color=0xFFFF00)
                await channel.send(embed=embed)
                normal_user_message = ''
                normal_counter = 0
                seconds = normal_user_database[key]
                hours, remainder = divmod(seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                
                if len(str(seconds)) < 2:
                    seconds = '0'+str(seconds)
                if len(str(minutes)) < 2:
                    minutes = '0'+str(minutes)
                if len(str(hours)) < 2:
                    hours = '0'+str(hours)
                normal_user_message += f"\n**{counter})Загальний час, який користувач {key}** \nпровів у голосових каналах: **{hours}:{minutes}:{seconds}**\nОстання активність:**{time_last_activity_database[key]}**"
        if normal_user_message != '':
            embed = discord.Embed(description=normal_user_message, color=0xFFFF00)
            await channel.send(embed=embed)
            
            
        items = bad_user_database.items()
        for key, value in items:
            bad_counter += 1
            counter += 1
            if bad_counter <= 25:
                seconds = bad_user_database[key]
                hours, remainder = divmod(seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                
                if len(str(seconds)) < 2:
                    seconds = '0'+str(seconds)
                if len(str(minutes)) < 2:
                    minutes = '0'+str(minutes)
                if len(str(hours)) < 2:
                    hours = '0'+str(hours)
                bad_user_message += f"\n**{counter})Загальний час, який користувач {key}** \nпровів у голосових каналах: **{hours}:{minutes}:{seconds}**\nОстання активність:**{time_last_activity_database[key]}**"
            else:
                embed = discord.Embed(description=bad_user_message, color=0xFF0000)
                await channel.send(embed=embed)
                bad_user_message = ''
                bad_counter = 0
                seconds = bad_user_database[key]
                hours, remainder = divmod(seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                
                if len(str(seconds)) < 2:
                    seconds = '0'+str(seconds)
                if len(str(minutes)) < 2:
                    minutes = '0'+str(minutes)
                if len(str(hours)) < 2:
                    hours = '0'+str(hours)
                bad_user_message += f"\n**{counter})Загальний час, який користувач {key}** \nпровів у голосових каналах: **{hours}:{minutes}:{seconds}**\nОстання активність:**{time_last_activity_database[key]}**"    
        if bad_user_message != '':
            embed = discord.Embed(description=bad_user_message, color=0xFF0000)
            await channel.send(embed=embed)
        