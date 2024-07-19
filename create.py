import discord
import asyncio
import sys
from datetime import datetime
from discord.utils import get
from config import *
from database import *
from bot import *
from options import *


class TicketCreation(discord.ui.View):

  @discord.ui.button(label="Подать заявку (вопрос) / Submit an application (question)",
                     emoji="📩",
                     style=discord.ButtonStyle.blurple)
  async def presscreate(self, interaction: discord.Interaction,
                        button: discord.ui.button):
    author = interaction.user
    guild = interaction.guild
    
    embed2 = discord.Embed(
          description=
          f'\nПривет, {author.name}! Выберите полк, в который хотите подать заявку или пункт с вопросом к руководству. \n \n Hi {author.name}! Select the regiment you want to apply to or the point with a question to the management.\n',
          color=embedColor)
    embed2.set_author(name=f'{author}', icon_url=f'{author.display_avatar}')
      #embed2.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
    await interaction.response.send_message(embed=embed2,
                                              view=TicketCreationMenuUI(),
                                              ephemeral=True)



class TicketCreationMenu(discord.ui.Select):

  def __init__(self):

    def optionsList():
      listofOptions = list(OptionsDict.values())
      oList = []
      for presets in listofOptions:
        oList.append(
            discord.SelectOption(label=presets[0],
                                 value=presets[1],
                                 description=presets[2]))
      return oList

    super().__init__(placeholder="Выберите пункт / Choose  an item...",
                     options=optionsList(),
                     min_values=1,
                     max_values=1)

  async def callback(self, interaction: discord.Interaction):
    author = interaction.user
    x[interaction.user.display_name] = f"{self.values[0]}"
    await interaction.response.send_modal(TicketCreationModal())
    embed2 = discord.Embed(description=f'Вы можете выбрать опцию только один раз! / You can only select an option once!',
                           color=embedColor)
    embed2.set_author(name=f'{author}', icon_url=f'{author.display_avatar}')
    #embed2.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
    await interaction.edit_original_response(embed=embed2, view=None)


class TicketCreationMenuUI(discord.ui.View):

  def __init__(self):
    super().__init__()
    self.add_item(TicketCreationMenu())


class embedButtons(discord.ui.View):

  @discord.ui.button(label="Закрыть заявку / Close Ticket",
                     emoji="📝",
                     style=discord.ButtonStyle.red)
  async def closeTicket(self, interaction: discord.Interaction,
                        button: discord.Button):
    tchannel = interaction.channel
    author = interaction.user
    guild = interaction.guild
    connection = TicketData.connect()
    cursor = TicketData.cursor(connection)
    ticketInfo = TicketData.find(cursor, tchannel.id)
    TicketData.close(connection)
    ltype = (ticketInfo[4])
    allowedAccess = False
    try:
      for allowedRoles in list(channelPerms[f"{ltype}"]):
        prole = discord.utils.get(guild.roles, id=allowedRoles)
        if prole in author.roles:
          allowedAccess = True
        else:
          pass
    except TypeError:
      prole = get(guild.roles, id=channelPerms[f"{ltype}"])
      if prole in author.roles:
        allowedAccess = True
      else:
        pass
    if (allowedAccess == True) or (f"{ticketInfo[1]}" == f"{author.id}"):
      embed6 = discord.Embed(
          description=
          "Вы уверены, что хотите закрыть этот билет? В результате заявка будет удалена. \n\n Are you sure that you want to close this ticket? This will result in the ticket being deleted.",
          color=embedColor)
      embed6.set_author(name=f'{author}', icon_url=author.display_avatar)
      #embed6.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
      try:
        await interaction.response.send_message(
            embed=embed6, view=yesOrNoOption(timeout=None), ephemeral=True)
      except discord.HTTPException:
        await interaction.response.send_message(
            "Произошла ошибка, попробуйте еще раз. / Something weird happened here, try again.")
    else:
      embed5 = discord.Embed(
          description=f'''Только создатель заявки может закрыть ее! Only the author of the ticket can use this button!''',
          color=embedColor)
      embed5.set_author(name=f'{author}', icon_url=f'{author.display_avatar}')
      #embed5.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
      try:
        await interaction.response.send_message(embed=embed5, ephemeral=True)
      except discord.HTTPException:
        await interaction.response.send_message(
            f'''**Вы не можете использовать эту команду! You can't use that command!****''')

  @discord.ui.button(label="Опции / Options",
                     emoji="⚙️",
                     style=discord.ButtonStyle.green)
  async def ticketOptions(self, interaction: discord.Interaction,
                          button: discord.Button):
    try:
      guild = interaction.guild
      author = interaction.user
      roleList = [994215060052381706, 994226835795746867, 1178285446158094386, 1213575945991102504, 1230216013195513928, 1230216099228942489, 1262847259754631320]
      permissionGranted = False
      for roleids in channelPerms.values():
        roleList.append(roleids)
      for allowedRoles in roleList:
        arole = get(guild.roles, id=allowedRoles)
        if arole in author.roles:
          permissionGranted = True
        else:
          pass
      tchannel = interaction.channel
      if permissionGranted == True:
        connection = TicketData.connect()
        cursor = TicketData.cursor(connection)
        ticketInfo = TicketData.find(cursor, tchannel.id)
        TicketData.close(connection)
        if ticketInfo != None:
          acategory = discord.utils.get(guild.categories,
                                        id=archivedTicketsCategoryID)
          acategoryc = (50 - (len(acategory.channels)))
          if acategoryc == 0:
            acategoryc2 = str(f'{acategoryc} slots left (full)')
          elif acategoryc == 1:
            acategoryc2 = str(f'{acategoryc} slot left (almost full)')
          elif acategoryc <= 5:
            acategoryc2 = str(f'{acategoryc} slots left (almost full)')
          elif acategoryc >= 6:
            acategoryc2 = str(f'{acategoryc} slots left')
          text = str(
              f'''👥- Добавить участника/Add a member to the ticket\n\n👋- Удалить участника/Remove a member from the ticket\n\n📓- Переименовать канал заявки/Rename a ticket channel\n\n📝- Сохранить и удалить заявку/Save and delete a ticket                         '''
          )
          embed3 = discord.Embed(title='''**Опции заявки / Ticket Options**''',
                                 description=f'{text}',
                                 color=embedColor)
          try:
            lauthor2 = (ticketInfo[1])
            lauthor3 = (int(lauthor2))
            lauthor4 = get(guild.members, id=lauthor3)
            if lauthor4 == None:
              lauthor5 = await bot.fetch_user(lauthor3)
              if lauthor5 == None:
                lauthor = str("N/A")
              else:
                lauthor = lauthor5
            else:
              lauthor = lauthor4
          except IndexError:
            lauthor = str("N/A")
          try:
            ltype = (ticketInfo[4])
          except IndexError:
            ltype = str("N/A")
          try:
            lcreation = (ticketInfo[3])
          except IndexError:
            lcreation = str("N/A")
          try:
            lstatus = (ticketInfo[5])
          except IndexError:
            lstatus = str("N/A")
          if (ticketInfo[2]) != "No":
            lcstatus = (ticketInfo[2])
            lcstatus2 = int(lcstatus)
            claimer = await bot.fetch_user(lcstatus2)
            cstatus = str(f"**Claimed** ({claimer.mention})")
          else:
            cstatus = str(f'**Not Claimed**')
          if lauthor == 'N/A':
            text2 = str(
                f'''**__Автор/Author:__** {lauthor.mention}\n**__Полк/Squadron:__** {ltype}\n**__Статус/Status:__** {lstatus}\n**__Время созданияCreation time:__** {lcreation}\n**__Статус/Claim Status:__** {cstatus}'''
            )
          else:
            text2 = str(
                f'''**__Автор/Author:__** {lauthor.mention}\n**__Полк/Squadron:__** {ltype}\n**__Статус/Status:__** {lstatus}\n**__Время созданияCreation time:__** {lcreation}\n**__Статус/Claim Status:__** {cstatus}'''
            )
          embed3.add_field(name="Информация о заявке / Ticket Infomation:", value=f"{text2}")
          embed3.set_author(name=f'{author}', icon_url=author.display_avatar)
          #embed3.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
          try:
            await interaction.response.send_message(embed=embed3,
                                                    ephemeral=True,
                                                    view=optionsMenu())
          except discord.HTTPException:
            await interaction.response.send_message(
                "HTTP Error that I'm too lazy to type out. Try again.",
                ephemeral=True)
        else:
          embed5 = discord.Embed(
              description=
              f'''Вы можете использовать эту команду только в канале подачи заявок!/You can only use this command in a ticket channel!''',
              color=embedColor)
          embed5.set_author(name=f'{author}',
                            icon_url=f'{author.display_avatar}')
          #embed5.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
          try:
            await interaction.response.send_message(embed=embed5,
                                                    ephemeral=True)
          except discord.HTTPException:
            await interaction.response.send_message(
                f'''**Вы можете использовать эту команду только в канале подачи заявок!/You can only use this command in a ticket channel!****'''
            )
      else:
        embed5 = discord.Embed(description=f'''Вы не можете использовать эту команду/You can't use that command!''',
                               color=embedColor)
        embed5.set_author(name=f'{author}',
                          icon_url=f'{author.display_avatar}')
        #embed5.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
        try:
          await interaction.response.send_message(embed=embed5, ephemeral=True)
        except discord.HTTPException:
          await interaction.response.send_message(
              f'''**Вы не можете использовать эту команду/You can't use that command!****''')
    except Exception as e:
      message2 = await interaction.response.send_message(
          f'A unknown error has occurred, a copy of the error has been sent to the developer ❌',
          ephemeral=True)
      activity1 = discord.Activity(type=discord.ActivityType.playing,
                                   name=f'{botStatusMessage}')
      await bot.change_presence(status=discord.Status.dnd, activity=activity1)
      web = bot.get_user(debugLogSendID)
      text = str('''Error on line {}'''.format(sys.exc_info()[-1].tb_lineno))
      embed = discord.Embed(title='commands.options function fail',
                            description=f'{text}, {str(e)}',
                            color=embedColor)
      try:
        await web.send(embed=embed)
      except discord.HTTPException:
        await web.send("commands.options function fail" + str(e))
      print(str(e))


class TicketCreationModal(discord.ui.Modal, title=f"Заявка в полк (вопрос) /Application (qestion)"):
  answer = discord.ui.TextInput(
      label='Ваш никнейм / Your nickname...',
      style=discord.TextStyle.paragraph,
      required=True,
      max_length=128)

  async def on_submit(self, interaction: discord.Interaction):
    ticketType = (x.get(interaction.user.display_name))
    author = interaction.user
    ticketDescription = (self.children[0].value)
    guild = bot.get_guild(guildID)
    me = bot.get_user(bot.user.id)
    default_perms = {}
    default_perms[guild.default_role] = discord.PermissionOverwrite(
        read_messages=False)
    default_perms[me] = discord.PermissionOverwrite(read_messages=True,
                                                    send_messages=True)
    default_perms[author] = discord.PermissionOverwrite(read_messages=True,
                                                        send_messages=True)
    try:
      for allowedRoles in list(channelPerms[f"{ticketType}"]):
        prole = get(guild.roles, id=allowedRoles)
        default_perms[prole] = discord.PermissionOverwrite(read_messages=True,
                                                           send_messages=True)
    except TypeError:
      prole = get(guild.roles, id=channelPerms[f"{ticketType}"])
      default_perms[prole] = discord.PermissionOverwrite(read_messages=True,
                                                         send_messages=True)
    now = datetime.now().strftime("%m-%d-%Y, %H:%M:%S")
    category = discord.utils.get(guild.categories, id=activeTicketsCategoryID)
    tchannel = await guild.create_text_channel(
        name=f'{ticketType}-{author.display_name}',
        category=category,
        overwrites=default_perms,
        topic=f"Nickname: {ticketDescription} | Created by: {author}")
    embed3 = discord.Embed(
        description=
        f'Ваша {ticketType} заявка создана, {tchannel.mention}. Руководство и офицеры скоро рассмотрят её. / Your {ticketType} ticket has been created, {tchannel.mention}. A member of our team will be with you shortly.',
        color=embedColor)
    embed3.set_author(name=f'{author}', icon_url=f'{author.display_avatar}')
    #embed3.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
    try:
      await interaction.response.send_message(embed=embed3, ephemeral=True)
    except discord.HTTPException:
      await interaction.response.send_message(
          f'Ваша {ticketType} заявка создана, {tchannel.mention}. Руководство и офицеры скоро рассмотрят её. / Your {ticketType} ticket has been created, {tchannel.mention}. A member of our team will be with you shortly.',
          ephemeral=True)
    messageString = ""
    try:
      for rolesToPing in list(channelPerms[f"{ticketType}"]):
        prole = get(guild.roles, id=rolesToPing)
        messageString = messageString + (f" {prole.mention}")
      await tchannel.send(messageString)
    except TypeError:
      prole = get(guild.roles, id=channelPerms[ticketType])
      await tchannel.send(f'{prole.mention}')
    embed1 = discord.Embed(
        title='[Внутрисерверная] Новая заявка / Ticket Created',
        description=f'{author.mention} создал новую {ticketType} заявку в полк / {author.mention} has created a new {ticketType} ticket',
        color=embedColor)
    embed1.add_field(name=f'Игровой никнейм:', value=f'{ticketDescription}')
    try:
      embed1.set_thumbnail(url=f'{author.display_avatar}')
    except Exception:
      pass
    #embed1.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=bot.user.display_avatar)
    try:
      message2 = await tchannel.send(embed=embed1,
                                     view=embedButtons(timeout=None))
    except discord.HTTPException as y:
      message2 = await tchannel.send(
          f"Заявка от {author}, Игровой никнейм: {ticketDescription} / Ticket Created by {author}, Reason: {ticketDescription}",
          view=embedButtons(timeout=None))
    await message2.pin()
    connection = TicketData.connect()
    cursor = TicketData.cursor(connection)
    TicketData.add(connection, cursor, tchannel.id, author.id, f"{now} UTC",
                   ticketType, "Active", message2.id)
    TicketData.close(connection)
    embed2 = discord.Embed(
        title='[Внутрисерверная] Новая заявка / Ticket Created',
        description=f'{author.mention} создал новую {ticketType} заявку в полк / {author.mention} has created a new {ticketType} ticket',
        
        color=embedColor)
    embed2.add_field(name='Канал/Channel:',
                     value=f'{tchannel.mention}',
                     inline=False)
    embed2.add_field(name=f'Никнейм в игре/Nickname:',
                     value=f'{ticketDescription}',
                     inline=False)
    embed2.add_field(name='Полк/Squadron:', value=f'{ticketType}', inline=False)
    embed2.add_field(name="**__ID автора:__**", value=f"{author.id}", inline=True)
    #embed2.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=bot.user.display_avatar)
    syslogc = await bot.fetch_channel(ticketLogsChannelID)
    try:
      message3 = await syslogc.send(embed=embed2)
    except discord.HTTPException:
      message3 = await syslogc.send(
          f"Заявка от {author}, Игровой никнейм: {ticketDescription} / Ticket Created by {author}, Reason: {ticketDescription}")
    del x[interaction.user.display_name]

    
    if channelPerms[ticketType] == (994215060052381706, 994226835795746867 ):   #Для EARLY
      
      
      await tchannel.send(f'{author.mention}, заполните заявку / Fill out the ticket: \n\n👇ПРИМЕР ЗАПОЛНЕНИЯ ЗАЯВКИ👇 \n (чтобы писать на следующей строчке нажмите Shift + Enter) \n 1) Название полка в который вступаете (сделать выбор): \n EARLY - для ежедневных полковых боев \n 2) Никнейм в игре, Имя, возраст, уровень аккаунта, кол-во сыгранных боев в РБ, КД в РБ за последний месяц \n 3) Как относишься к полковым боям? Готов ли часто принимать в них участие (ПБ - главная цель полка early, фарм полк пб по желанию) \n  4) Полки в которых состояли ранее \n 5) Откуда ты (город и часовой пояс), примерный прайм тайм \n 6) Предпочтительный режим игры: АБ, РБ или СБ \n 7) Предпочтительный вид техники в ПБ (наземный, воздушный) \n 8) Максимальный бр по технике: авиа, танки (не премы) \n 9) Как о нас узнал или где нашел? \n ———————————————————————————— \n 👇EXAMPLE OF COMPLETING AN APPLICATION👇 \n 1) Name of the squadron you are joining (make a choice):  \n EARLY - for daily squadron battles \n 2) Nickname in the game, name, age, account level, number of battles played in RB, K/D in RB over the past month \n 3) How do you feel about squadron battles? Are you ready to take part in them often (SQB is the main goal of the squadron) \n 4) The squadrons in which you were previously a member \n 5) Where are you from (city and time zone), approximate prime time \n 6) Preferred game mode: AB, RB or SB \n 7) Preferred type of equipment in the SQB (ground, air) \n 8) Max BR: aviation, tanks (not premium) \n 9) How did you hear about us or where did you find us?    ')
    
    if channelPerms[ticketType] == (994215060052381706, 1178285446158094386, 1213575945991102504):   #Для E4RLY
      await tchannel.send(f'{author.mention}, заполните заявку: \n\n👇ПРИМЕР ЗАПОЛНЕНИЯ ЗАЯВКИ👇 \n (чтобы писать на следующей строчке нажмите Shift + Enter) \n 1) Название полка в который вступаете (сделать выбор): \n ⬥E4RLY - для фарма техники и совместной игры \n 2) Никнейм в игре, Имя, возраст, уровень аккаунта, кол-во сыгранных боев в РБ, КД в РБ за последний месяц \n 3) Как относишься к полковым боям? Готов ли часто принимать в них участие (ПБ - главная цель полка early, фарм полк пб по желанию) \n  4) Полки в которых состояли ранее \n 5) Откуда ты (город и часовой пояс), примерный прайм тайм \n 6) Предпочтительный режим игры: АБ, РБ или СБ \n 7) Предпочтительный вид техники в ПБ (наземный, воздушный) \n 8) Максимальный бр по технике: авиа, танки (не премы) \n 9) Как о нас узнал или где нашел?')
    if channelPerms[ticketType] == (994215060052381706, 1230216013195513928, 1230216099228942489):   #Для ENRLY

       await tchannel.send(f'{author.mention}, Fill out the ticket: \n\n👇EXAMPLE OF COMPLETING AN APPLICATION👇 \n 1) Name of the squadron you are joining (make a choice):  \n ★ ENRLY - for farm equipment, co-op play and squadron battles \n 2) Nickname in the game, name, age, account level, number of battles played in RB, K/D in RB over the past month \n 3) How do you feel about squadron battles? Are you ready to take part in them often (SQB is the main goal of the squadron) \n 4) The squadrons in which you were previously a member \n 5) Where are you from (city and time zone), approximate prime time \n 6) Preferred game mode: AB, RB or SB \n 7) Preferred type of equipment in the SQB (ground, air) \n 8) Max BR: aviation, tanks (not premium) \n 9) How did you hear about us or where did you find us? ')

    if channelPerms[ticketType] == (994215060052381706, 1213575945991102504, 1230216099228942489):   #Для вопросов
        
      await tchannel.send(f'{author.mention}, задайте свой вопрос в этом канале. / Ask your question in this channel.')
    
    if channelPerms[ticketType] == (994215060052381706):   #Для отряда
        
      await tchannel.send(f'{author.mention}, добавьте игроков в свой отряд. Для этого необходимо получить роль <@&1262847259754631320>')


x = dict()
