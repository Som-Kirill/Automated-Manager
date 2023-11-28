import discord
from discord.ext import commands
import logging

#Модулі програм
from config_work_func import ConfigReader
from keeping_time_spent_in_the_voice_channels import keeping_time_spent_in_voice_channels
from counting_time_spent_in_the_voice_channels import counting_time_in_voice_channels
from help_func import send_help_comand
from thunder_skills_func import parser_thunder_skill
from version_info_read_func import read_info_file
from clear_func import clear_data
from another_game_create_func import another_game_create

def start_logging():
    # Налаштовуємо рівень логування 
    logging.basicConfig(level=logging.INFO)

    # Створюємо обробник для збереження логів у файл
    file_handler = logging.FileHandler(filename='bot.log')
    file_handler.setLevel(logging.INFO)

    # Створюємо логгер і додаємо обробники
    logger = logging.getLogger('discord')
    logger.addHandler(file_handler)
    print('='*70)
    print(f'Logging почато...')
    print('='*70)

#запуск модулю зчитування з config.cfg
config = {}
def main():
    global config
    config_reader = ConfigReader()
    config_reader.read_config()
    config = config_reader.config
    print('='*70)
    print(f'Config зчитано результат:')
    print('='*70)
    print(config)
    print('='*70)

if __name__ == "__main__":
    main()
    start_logging()


# Створюємо об'єкт інтентів
intents = discord.Intents.default()
intents.message_content = True

# Встановлюємо префікс команд
bot = commands.Bot(command_prefix=config['prefix'], intents=intents, help_command=None)
@bot.event
async def on_ready():
    print('='*70)
    print(f'Бот запущений, підключився як {bot.user.name}')
    print('='*70)
    # Змінюємо статус бота
    activity = "Реліз v1.5"
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=activity))

@bot.event
async def on_voice_state_update(member, before, after):
    time_keeper = keeping_time_spent_in_voice_channels()
    keeping_time_spent_in_voice_channels.bot = bot
    await time_keeper.on_voice_state_update(member, before, after)
    create_func = another_game_create()
    another_game_create.bot = bot
    await create_func.on_voice_state_update_another_game(member, before, after)

@bot.command(name='time', help="Показує загальний час користувача в голосових каналах.", usage="!time <@тег_користувача>")
async def show_total_time(ctx, user_tag=None):
    if ctx.channel.id == config['channel_of_sending_invites']:
        time_counting = counting_time_in_voice_channels()
        counting_time_in_voice_channels.bot = bot
        await time_counting.show_total_time(ctx, user_tag)

@bot.command(name='alltime', help="Показує загальний час користувачів в голосових каналах.")
async def show_total_time_all_user(ctx):
    if ctx.channel.id == config['channel_of_sending_invites']:
        time_counting = counting_time_in_voice_channels()
        counting_time_in_voice_channels.bot = bot
        await time_counting.show_total_time_all_user(ctx)

@bot.command(name='help', help="Команда для отримання допомоги з використання та отримання додаткової інформації про команди")
async def help(ctx, command=None):
    if ctx.channel.id == config['channel_of_sending_invites']:
        help_comand = send_help_comand()
        send_help_comand.bot = bot
        await help_comand.help_comand(ctx, command)

@bot.command(name='skill', help="Команда для отримання посилання на сайт ThunderSkill по тегу")
async def parser_skill(ctx, user_tag=None):
    if user_tag == None:
        message = f'Спробуй: !skill @user_tag або !skill UMMA'
        embed = discord.Embed(description=message, color=0x0000ff)
        await ctx.send(embed=embed)
        return
    if user_tag == 'UMMA':
        message = f'Профіль полка **UMMA** \nна сайті ThunderSkill: https://thunderskill.com/ru/squad/%5EUMMA%5E'
        embed = discord.Embed(description=message, color=0x0000ff)
        await ctx.send(embed=embed)
        return
    if user_tag != None:
        parser_skil = parser_thunder_skill()
        parser_thunder_skill.bot = bot
        await parser_skil.parser_skill_comand(ctx, user_tag)

@bot.command(name='vinfo', help="Команда для отримання інформації про версію бота")
async def read_info(ctx):
    if ctx.channel.id == config['channel_of_sending_invites']:
        info_comand = read_info_file()
        read_info_file.bot = bot
        await info_comand.read_info(ctx)    

@bot.command(name='clear', help="Команда для очишення data-time")
@commands.has_role(config['role_clear_id'])
async def clear(ctx):
    if ctx.channel.id == config['channel_of_sending_invites']:
        clear_comand = clear_data()
        clear_data.bot = bot
        await clear_comand.clear(ctx)

# Запускаємо бота з токеном
bot.run(config['token'])
print('='*70)
