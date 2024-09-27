import discord, datetime
import sys
import os
import fileinput
from discord import app_commands
from datetime import datetime
from discord.utils import get
from config import *
from database import *
from options import *
from create import *
from bot import *

ticket = app_commands.CommandTree(bot)


@bot.event
async def on_ready():
  await bot.wait_until_ready()
  databasecon = TicketData.connect()
  databasecur = TicketData.cursor(databasecon)
  if TicketData.verifylayout(databasecur) == True:
    print("------------------------------------")
    print("[MESSAGE]: Ticket Database found.")
  else:
    print("------------------------------------------------------")
    print("[WARN]: Ticket Database not found. Creating Database...")
    TicketData.createlayout(databasecon, databasecur)
  print("------------------------------------")
  print(f"Bot Name: {bot.user.name}#{bot.user.discriminator}")
  print(f"Bot ID: {bot.user.id}")
  print("Discord Version: " + discord.__version__)
  print("------------------------------------")
  if f'{botStatusType}' == 'Playing':
    activity1 = discord.Activity(type=discord.ActivityType.playing,
                                 name=f'{botStatusMessage}')
    await bot.change_presence(status=discord.Status.online, activity=activity1)
  elif f'{botStatusType}' == 'Streaming':
    activity1 = discord.Activity(type=discord.ActivityType.streaming,
                                 name=f'{botStatusMessage}')
    await bot.change_presence(status=discord.Status.online, activity=activity1)
  elif f'{botStatusType}' == 'Watching':
    activity1 = discord.Activity(type=discord.ActivityType.watching,
                                 name=f'{botStatusMessage}')
    await bot.change_presence(status=discord.Status.online, activity=activity1)
  elif f'{botStatusType}' == 'Listening':
    activity1 = discord.Activity(type=discord.ActivityType.listening,
                                 name=f'{botStatusMessage}')
    await bot.change_presence(status=discord.Status.online, activity=activity1)
  else:
    activity1 = discord.Activity(type=discord.ActivityType.playing,
                                 name=f'{botStatusMessage}')
    await bot.change_presence(status=discord.Status.online, activity=activity1)
    print(
        '''[WARN]: You have incorrectly specified the bot's activity type, the default has been selected. '''
    )
    print("----------------------------------------------------")
  if firstRun == True:
    print(
        "[MESSAGE]: First Run is set to true, syncing slash commands with discord and generating ticket creation embed..."
    )
    print(
        "--------------------------------------------------------------------------------"
    )
    await ticket.sync()
    tchannel = bot.get_channel(IDOfChannelToSendTicketCreationEmbed)
    embed = discord.Embed(
        title='''**Подать заявку в полк или задать вопрос руководству сервера / Submit an application or ask a question to the management**''',
        description=f'Чтобы подать заявку в полк или задать вопрос нажмите кнопку ниже! \n\nTo apply to the squadron or question to the management, click the button below!\n\n__**EARLY**__ - для ежедневных полковых боёв / for squadron battles \n __**E4RLY**__ - русско-язычный полк для фарма техники и полковых боев \n__**ENRLY**__ - english-speaking squadron for farming equipment and squadron battles\n __**Вопрос руководству / Question to the management**__ - Выберите этот пункт, если у вас есть вопрос к руководству сервера (полка) / Select this option if you have a question for the server management (squdrones)',
        color=embedColor)
    # embed.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
    nmessage = await tchannel.send(embed=embed, view=TicketCreation())
    try:
      for line in fileinput.input(("config.py"), encoding="utf8", inplace=1):
        if "IDofMessageForTicketCreation" in line:
          line = line.replace(
              line,
              f'IDofMessageForTicketCreation = {nmessage.id}                       #This variable was automatically adjusted.\n'
          )
        elif "firstRun" in line:
          line = line.replace(
              line,
              "firstRun = False               #This variable was automatically adjusted.\n"
          )
        sys.stdout.write(line)
    except Exception:
      for line in fileinput.input(("config.py"), inplace=1):
        if "IDofMessageForTicketCreation" in line:
          line = line.replace(
              line,
              f'IDofMessageForTicketCreation = {nmessage.id}                       #This variable was automatically adjusted.\n'
          )
        elif "firstRun" in line:
          line = line.replace(
              line,
              "firstRun = False               #This variable was automatically adjusted.\n"
          )
        sys.stdout.write(line)
    embed2 = discord.Embed(
        title='**__Embed Message ID Updated:__**',
        description=
        f'New Message ID is: `{nmessage.id}`\n **Please restart the bot if not restarted automatically**',
        color=embedColor)
    embed2.set_footer(text=f'{bot.user.name} | {bot.user.id}',
                      icon_url=f'{bot.user.display_avatar}')
    developer = bot.get_user(debugLogSendID)
    try:
      await developer.send(embed=embed2)
    except discord.HTTPException:
      await developer.send(
          f"**__Embed Message ID Updated:__**\nNew Message ID is: `{nmessage.id}`\n **Please restart the bot if not restarted automatically**"
      )
    await bot.close()
    print(
        "[WARN]: Embed Message Generated! Please restart the bot if not restarted automatically."
    )
    print(
        "--------------------------------------------------------------------------------"
    )
    os.execv(sys.argv[0], sys.argv)
  else:
    allTickets = []
    allTickets = TicketData.getall(databasecur, allTickets)
    for tickets in allTickets:
      channelID = int(tickets[0])
      messageID = int(tickets[6])
      tchannel = bot.get_channel(channelID)
      if tchannel != None:
        tmessage = await tchannel.fetch_message(messageID)
        await tmessage.edit(view=embedButtons(timeout=None))
      else:
        pass
    embed = discord.Embed(
        title='''**Подать заявку в полк или задать вопрос руководству сервера / Submit an application or ask a question to the management**''',
        description=f'Чтобы подать заявку в полк или задать вопрос нажмите кнопку ниже! \n\nTo apply to the squadron or question to the management, click the button below!\n\n__**EARLY**__ - для ежедневных полковых боёв / for squadron battles \n __**E4RLY**__ - русско-язычный полк для фарма техники и полковых боев \n__**ENRLY**__ - english-speaking squadron for farming equipment and squadron battles\n __**Вопрос руководству / Question to the management**__ - Выберите этот пункт, если у вас есть вопрос к руководству сервера (полка) / Select this option if you have a question for the server management (squdrones)', color=embedColor)
    # embed.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
    try:
      tchannel = bot.get_channel(IDOfChannelToSendTicketCreationEmbed)
      tmessage = await tchannel.fetch_message(IDofMessageForTicketCreation)
      await tmessage.edit(embed=embed, view=TicketCreation(timeout=None))
      print(
          "[MESSAGE]: Relinked to Ticket Creation Embed, standing by for ticket creation..."
      )
      print(
          "---------------------------------------------------------------------------------"
      )
    except Exception:
      print(
          "[ERROR]: Embed Message not found! Creating a new embed message, please restart the bot if not restarted automatically"
      )
      print(
          "--------------------------------------------------------------------------------"
      )
      nmessage = await tchannel.send(embed=embed, view=TicketCreation())
      try:
        for line in fileinput.input(("config.py"), encoding="utf8", inplace=1):
          if "IDofMessageForTicketCreation" in line:
            line = line.replace(
                line,
                f'IDofMessageForTicketCreation = {nmessage.id}                       #This variable was automatically adjusted.\n'
            )
          sys.stdout.write(line)
      except Exception:
        for line in fileinput.input(("config.py"), inplace=1):
          if "IDofMessageForTicketCreation" in line:
            line = line.replace(
                line,
                f'IDofMessageForTicketCreation = {nmessage.id}                       #This variable was automatically adjusted.\n'
            )
          sys.stdout.write(line)
      embed2 = discord.Embed(
          title='**__Embed Message ID Updated:__**',
          description=
          f'New Message ID is: `{nmessage.id}`\n **Please restart the bot if not restarted automatically**',
          color=embedColor)
      embed2.set_footer(text=f'{bot.user.name} | {bot.user.id}',
                        icon_url=f'{bot.user.display_avatar}')
      developer = bot.get_user(debugLogSendID)
      try:
        await developer.send(embed=embed2)
      except discord.HTTPException:
        await developer.send(
            f"**__Embed Message ID Updated:__**\nNew Message ID is: `{nmessage.id}`\n **Please restart the bot if not restarted automatically**"
        )
      await bot.close()
      os.execv(sys.argv[0], sys.argv)
  print("[MESSAGE]: Bot is up and running!")
  print("------------------------------------")
  TicketData.close(databasecon)


@ticket.command(name="sync",
                description="Syncs the Ticket Command Tree to Discord.")
async def self(interaction: discord.Interaction):
  author = interaction.user
  if author.id == debugLogSendID:
    embed1 = discord.Embed(description=f'Syncing Commands to Discord...',
                           color=embedColor)
    embed1.set_author(name=f'{author}', icon_url=f'{author.display_avatar}')
    embed1.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}",
                      icon_url=f'{bot.user.display_avatar}')
    await interaction.response.send_message(embed=embed1, ephemeral=True)
    try:
      await ticket.sync()
      embed2 = discord.Embed(description=f'Commands Synced...',
                             color=embedColor)
      embed2.set_author(name=f'{author}', icon_url=f'{author.display_avatar}')
      embed2.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}",
                        icon_url=f'{bot.user.display_avatar}')
      await interaction.edit_original_response(embed=embed2)
    except Exception as e:
      embed2 = discord.Embed(title="**__An Error Occured:__**",
                             description=f'Error: {e}',
                             color=embedColor)
      embed2.set_author(name=f'{author}', icon_url=f'{author.display_avatar}')
      embed2.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}",
                        icon_url=f'{bot.user.display_avatar}')
      await interaction.edit_original_response(embed=embed2)
  else:
    pass


@ticket.command(name="create", description="Создать приватную заявку/Creates a private ticket channel")
async def self(interaction: discord.Interaction, reason: str = 'Unspecified'):
  try:
    author = interaction.user
    guild = interaction.guild
    allowedAcess = False
    try:
      for allowedRoles in list(
          channelPerms[f"{ticketTypeAllowedToCreatePrivateChannels}"]):
        prole = discord.utils.get(guild.roles, id=allowedRoles)
        if prole in author.roles:
          allowedAcess = True
        else:
          pass
    except TypeError:
      prole = get(
          guild.roles,
          id=channelPerms[f"{ticketTypeAllowedToCreatePrivateChannels}"])
      if prole in author.roles:
        allowedAcess = True
      else:
        pass
    syslogc = discord.utils.get(guild.channels, id=ticketLogsChannelID)
    if allowedAcess == True:
      categoryn = activeTicketsCategoryID
      category = discord.utils.get(guild.categories, id=categoryn)
      overwrites = {
          guild.default_role:
          discord.PermissionOverwrite(read_messages=False),
          guild.me:
          discord.PermissionOverwrite(read_messages=True, send_messages=True),
          prole:
          discord.PermissionOverwrite(read_messages=True, send_messages=True)
      }
      nchannel = await guild.create_text_channel(
          f'private-{author.display_name}',
          category=category,
          overwrites=overwrites,
          topic=f'Reason: {reason} | Created by: {author}')
      embed3 = discord.Embed(
          description=f'Private Ticket Channel created: {nchannel.mention}',
          color=embedColor)
      embed3.set_author(name=f'{author}', icon_url=f'{author.display_avatar}')
      embed3.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}",
                        icon_url=f'{bot.user.display_avatar}')
      try:
        await interaction.response.send_message(embed=embed3, ephemeral=True)
      except discord.HTTPException:
        await interaction.response.send_message(
            f'Private Ticket Channel created: {nchannel.mention}. A member of our team will be with you shortly.',
            ephemeral=True)
      embed1 = discord.Embed(
          title='Ticket Created',
          description=f'{author.mention} has created a new private ticket',
          color=embedColor)
      embed1.add_field(name=f'Reason:', value=f'{reason}')
      try:
        embed1.set_thumbnail(url=f'{author.display_avatar}')
      except Exception:
        pass
      embed1.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}",
                        icon_url=bot.user.display_avatar)
      message10 = await nchannel.send(author.mention)
      await message10.delete()
      try:
        message3 = await nchannel.send(embed=embed1, view=embedButtons())
      except discord.HTTPException as y:
        message3 = await nchannel.send(
            f"Ticket Created by {author}, Reason: {reason}",
            view=embedButtons())
      await message3.pin()
      connection = TicketData.connect()
      cursor = TicketData.cursor(connection)
      now = datetime.now().strftime("%m-%d-%Y, %H:%M:%S")
      TicketData.add(connection, cursor, nchannel.id, author.id, f'{now} EST',
                     ticketTypeAllowedToCreatePrivateChannels, "active",
                     message3.id)
      TicketData.close(connection)
      embed2 = discord.Embed(
          title='Ticket Created',
          description=f'{author.mention} has created a new ticket',
          color=embedColor)
      embed2.add_field(name='Channel:',
                       value=f'{nchannel.mention}',
                       inline=False)
      embed2.add_field(name=f'Reason:', value=f'{reason}', inline=False)
      embed2.add_field(name='Type:', value='Private', inline=False)
      embed2.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}",
                        icon_url=f'{bot.user.display_avatar}')
      try:
        await syslogc.send(embed=embed2)
      except discord.HTTPException:
        await syslogc.send(f"Ticket Created by {author}, Reason: {reason}")
    else:
      embed5 = discord.Embed(
          description=f'''{author.mention}, you can't use that command! ❌''',
          color=embedColor)
      embed5.set_author(name=f'{author}', icon_url=f'{author.display_avatar}')
      embed5.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}",
                        icon_url=f'{bot.user.display_avatar}')
      try:
        await interaction.response.send_message(embed=embed5, ephemeral=True)
      except discord.HTTPException:
        await interaction.response.send_message(
            f'''{author.mention}, **you can't use that command! ❌**''',
            ephemeral=True)
  except Exception as e:
    message2 = await interaction.response.send_message(
        f'A unknown error has occurred, a copy of the error has been sent to the bot owner ❌',
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
    print(text)


@ticket.command(name="pipi",
                description="Показать опции канала с заявкой/Displays the options for a ticket channel")
async def options(interaction: discord.Interaction):
  try:
    guild = interaction.guild
    author = interaction.user
    tchannel = interaction.channel
    roleList = [994215060052381706, 994226835795746867, 1178285446158094386, 1213575945991102504, 1230216013195513928, 1230216099228942489]
    permissionGranted = False
    for roleids in channelPerms.values():
      roleList.append(roleids)
    for allowedRoles in roleList:
      arole = get(guild.roles, id=allowedRoles)
      if arole in author.roles:
        permissionGranted = True
      else:
        pass
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
            f'''🚩- Принять заявку/Claim a ticket\n\n👥- Добавить участника/Add a member to the ticket\n\n👋- Удалить участника/Remove a member from the ticket\n\n🟢- Поместить заявку в раздел активных/Mark a ticket as active\n\n✋- Поместить заявку в раздел замороженных/Mark a ticket as onhold\n\n📓- Переименовать канал заявки/Rename a ticket channel\n\n🗄️- поместить заявку в архив/Place a ticket in the archives **({acategoryc2})**\n\n📝- Сохранить и удалить заявку/Save and delete a ticket                      '''
        )
        embed3 = discord.Embed(title='''**Свойства заявки/Ticket Options**''',
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
        embed3.add_field(name="Информация о заявке/Ticket Infomation:", value=f"{text2}")
        embed3.set_author(name=f'{author}', icon_url=author.display_avatar)
        embed3.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}",
                          icon_url=f'{bot.user.display_avatar}')
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
            f'''Вы можете использовать эту команду только в канале подачи заявок! / You can only use this command in a ticket channel!''',
            color=embedColor)
        embed5.set_author(name=f'{author}',
                          icon_url=f'{author.display_avatar}')
        embed5.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}",
                          icon_url=f'{bot.user.display_avatar}')
        try:
          await interaction.response.send_message(embed=embed5, ephemeral=True)
        except discord.HTTPException:
          await interaction.response.send_message(
              f'''**Вы можете использовать эту команду только в канале подачи заявок! / You can only use this command in a ticket channel!****''')
    else:
      embed5 = discord.Embed(description=f'''Вы не можете использовать эту команду / You can't use that command!''',
                             color=embedColor)
      embed5.set_author(name=f'{author}', icon_url=f'{author.display_avatar}')
      embed5.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}",
                        icon_url=f'{bot.user.display_avatar}')
      try:
        await interaction.response.send_message(embed=embed5, ephemeral=True)
      except discord.HTTPException:
        await interaction.response.send_message(
            f'''**Вы не можете использовать эту команду / You can't use that command!****''')
  except Exception as e:
    message2 = await interaction.response.send_message(
        f'A unknown error has occurred, a copy of the error has been sent to the bot owner ❌',
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
    print(text)





try:
  bot.run(f"{get_token()}")
except discord.errors.LoginFailure as e:
  print('Login Failed, ERROR 401 Unauthorized')
