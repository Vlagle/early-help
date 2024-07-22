import discord
import asyncio
import io
import chat_exporter
from discord.utils import get
from config import *
from database import *
from bot import *

class addMemberModal(discord.ui.Modal, title="Добавить / Add"):
    answer = discord.ui.TextInput(label='ID участника / Member ID ', style=discord.TextStyle.short, required=True, max_length=128)

    async def on_submit(self, interaction: discord.Interaction):
        tchannel = interaction.channel
        author = interaction.user
        guild = interaction.guild
        connection = TicketData.connect()
        cursor = TicketData.cursor(connection)
        ticketInfo = TicketData.find(cursor, tchannel.id)
        TicketData.close(connection)
        try:
            ltype = (ticketInfo[4])
        except IndexError:
            ltype = str("N/A")
        
        try:
            amember = discord.utils.get(guild.members, id=int(self.children[0].value))
        except Exception:
            amember = None
        if amember == None:
            embed = discord.Embed(description=f'''Не найден этот участник. Результат / This participant was not found. Result: {self.children[0].value}''', color=embedColor)
            #embed.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
            embed.set_author(name=f'{author}', icon_url=author.display_avatar)
            try:
                await interaction.response.send_message(embed=embed, ephemeral=True)
            except discord.HTTPException:
                await interaction.response.send_message(f'''Не найден этот участник. Результат / This participant was not found. Result: {self.children[0].value}''', ephemeral=True)
        elif amember != None:
            allowedAccess = False
            try:
                for allowedRoles in list(channelPerms[f"{ltype}"]):
                    prole = discord.utils.get(guild.roles, id=allowedRoles)
                    if prole in amember.roles:
                        allowedAccess = True
                        break
                    else:
                        pass
            except TypeError:
                prole = get(guild.roles, id=channelPerms[f"{ltype}"])
                if prole in amember.roles:
                    allowedAccess = True
                else:
                    pass
            if (allowedAccess == True):
                embed2 = discord.Embed(description=f'''Я не могу добавить этого участника! / I can't add that member!''', color=embedColor)
                #embed2.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
                embed2.set_author(name=f'{author}', icon_url=author.display_avatar)
                try:
                    await interaction.response.send_message(embed=embed2, ephemeral=True)
                except discord.HTTPException:
                    await interaction.response.send_message(f'''Я не могу добавить этого участника! / I can't add that member!`''', ephemeral=True)
            else:
                await tchannel.set_permissions(amember, send_messages=True, read_messages=True)
                embed2 = discord.Embed(description=f'''Добавлен участник / Member added ✅''', color=embedColor)
                #embed2.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
                embed2.set_author(name=f'{author}', icon_url=author.display_avatar)
                try:
                    await interaction.response.send_message(embed=embed2, ephemeral=True)
                except discord.HTTPException:
                    await interaction.response.send_message(f'''Добавлен участник / Member added ✅''', ephemeral=True)
                embed3 = discord.Embed(title="**__Добавлен участник / Member Added__**", description=f'''{amember.mention} был добавлен в заявку пользователем {author.mention} / {amember.mention} has been added to the ticket by {author.mention} ''', color=embedColor)
                embed3.set_thumbnail(url=f'{amember.avatar}')
                #embed3.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
                try:
                    await tchannel.send(embed=embed3)
                except discord.HTTPException:
                    await tchannel.send(f'{amember.mention} **был добавлен в заявку пользователем** {author.mention} / {amember.mention} **has been added to the ticket by** {author.mention}')

class removeMemberModal(discord.ui.Modal, title="Удалить / Remove "):
    answer = discord.ui.TextInput(label='ID участника / Member ID', style=discord.TextStyle.short, required=True, max_length=128)

    async def on_submit(self, interaction: discord.Interaction):
        tchannel = interaction.channel
        author = interaction.user
        guild = interaction.guild
        connection = TicketData.connect()
        cursor = TicketData.cursor(connection)
        ticketInfo = TicketData.find(cursor, tchannel.id)
        TicketData.close(connection)
        try:
            ltype = (ticketInfo[4])
        except IndexError:
            ltype = str("N/A")
        
        try:
            amember = discord.utils.get(guild.members, id=int(self.children[0].value))
        except Exception:
            amember = None
        if amember == None:
            embed = discord.Embed(description=f'''Не найден этот участник. Результат / This participant was not found. Result:  {self.children[0].value}''', color=embedColor)
            #embed.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
            embed.set_author(name=f'{author}', icon_url=author.display_avatar)
            try:
                await interaction.response.send_message(embed=embed, ephemeral=True)
            except discord.HTTPException:
                await interaction.response.send_message(f'''Не найден этот участник. Результат / This participant was not found. Result:  {self.children[0].value}''', ephemeral=True)
        elif amember != None:
            allowedAccess = False
            try:
                for allowedRoles in list(channelPerms[f"{ltype}"]):
                    prole = discord.utils.get(guild.roles, id=allowedRoles)
                    if prole in amember.roles:
                        allowedAccess = True
                        break
                    else:
                        pass
            except TypeError:
                prole = get(guild.roles, id=channelPerms[f"{ltype}"])
                if prole in amember.roles:
                    allowedAccess = True
                else:
                    pass
            if (allowedAccess == True):
                embed2 = discord.Embed(description=f'''Я не могу удалить этого участника! / I can't remove that member!''', color=embedColor)
                #embed2.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
                embed2.set_author(name=f'{author}', icon_url=author.display_avatar)
                try:
                    await interaction.response.send_message(embed=embed2, ephemeral=True)
                except discord.HTTPException:
                    await interaction.response.send_message(f'''Я не могу удалить этого участника! / I can't remove that member!`''', ephemeral=True)
            else:
                await tchannel.set_permissions(amember, send_messages=False, read_messages=False)
                embed2 = discord.Embed(description=f'''Участник удален / Member removed ✅''', color=embedColor)
                #embed2.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
                embed2.set_author(name=f'{author}', icon_url=author.display_avatar)
                try:
                    await interaction.response.send_message(embed=embed2, ephemeral=True)
                except discord.HTTPException:
                    await interaction.response.send_message(f'''Участник удален / Member removed. ✅''', ephemeral=True)

class renameChannelModal(discord.ui.Modal, title="Переименовать / Rename"):
    answer = discord.ui.TextInput(label='Имя канала / Channel Name:', style=discord.TextStyle.short, required=True, max_length=32)
    async def on_submit(self, interaction: discord.Interaction):
        tchannel = interaction.channel
        author = interaction.user
        if f"{self.children[0].value}" == '':
            embed4 = discord.Embed(description=f'''You didn't provide a valid answer! Please try again. I got {self.children[0].value}''', color=embedColor)
            embed4.set_author(name=f'{author}', icon_url=author.display_avatar)
            #embed4.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
            try:
                await interaction.response.send_message(embed=embed4, ephemeral=True)
            except discord.HTTPException:
                await interaction.response.send_message(f'''You didn't provide a valid answer! Please try again. I got {self.children[0].value}''', ephemeral=True)
        else:
            embed2 = discord.Embed(description=f'Канал переименова / Channel Renamed ✅', color=embedColor)
            embed2.set_author(name=f'{author}', icon_url=author.display_avatar)
            #embed2.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
            await tchannel.edit(name=self.children[0].value)
            await interaction.response.send_message(embed=embed2, ephemeral=True)


    

    
class optionsMenu(discord.ui.View):
    
    @discord.ui.button(label="Добавить участника/Add a member", emoji="👥", style=discord.ButtonStyle.gray)
    async def addmember(self, interaction:discord.Interaction, button: discord.ui.button):
        await interaction.response.send_modal(addMemberModal())
        author = interaction.user
        embed2 = discord.Embed(description=f'Вы можете нажать на кнопку только один раз! / You can only select a button once! \n\nСообщение будет удалено через 30 секунд. / The message will be deleted after 30 seconds.', color=embedColor)
        embed2.set_author(name=f'{author}', icon_url=f'{author.display_avatar}')
        #embed2.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')  
        await interaction.edit_original_response(embed=embed2, view=None)
        await asyncio.sleep(30)
        await interaction.message.delete()
    

    @discord.ui.button(label="Удалить участника/Remove a member", emoji="👋", style=discord.ButtonStyle.gray)
    async def removemember(self, interaction:discord.Interaction, button: discord.ui.button):
        await interaction.response.send_modal(removeMemberModal())
        author = interaction.user
        embed2 = discord.Embed(description=f'Вы можете нажать на кнопку только один раз! / You can only select a button once! \n\nСообщение будет удалено через 30 секунд. / The message will be deleted after 30 seconds.', color=embedColor)
        embed2.set_author(name=f'{author}', icon_url=f'{author.display_avatar}')
        #embed2.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')  
        await interaction.edit_original_response(embed=embed2, view=None)
        await asyncio.sleep(30)
        await interaction.message.delete()

    
    @discord.ui.button(label="Переименовать/Rename", emoji="✏️", style=discord.ButtonStyle.gray)
    async def rename(self, interaction:discord.Interaction, button: discord.ui.button):
        await interaction.response.send_modal(renameChannelModal())
        author = interaction.user
        embed2 = discord.Embed(description=f'Вы можете нажать на кнопку только один раз! / You can only select a button once! \n\nСообщение будет удалено через 30 секунд. / The message will be deleted after 30 seconds.', color=embedColor)
        embed2.set_author(name=f'{author}', icon_url=f'{author.display_avatar}')
        #embed2.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')  
        await interaction.edit_original_response(embed=embed2, view=None)
        await asyncio.sleep(30)
        await interaction.message.delete()
        
   
    @discord.ui.button(label="Сохранить и удалить/Save and delete", emoji="📝", style=discord.ButtonStyle.green)
    async def transcribe(self, interaction:discord.Interaction, button: discord.ui.button):
        author = interaction.user
        embed6 = discord.Embed(description="Вы уверены, что хотите закрыть этот билет? В результате заявка будет удалена. \n\n Are you sure that you want to close this ticket? This will result in the ticket being deleted.", color=embedColor)
        embed6.set_author(name=f'{author}', icon_url=author.display_avatar)
        #embed6.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
        try:
            await interaction.response.edit_message(embed=embed6, view=yesOrNoOption(timeout=None))
        except discord.HTTPException:
            await interaction.response.edit_message("Something weird happened here, try again.")

    @discord.ui.button(label="Закрыть / Close", emoji="👥", style=discord.ButtonStyle.gray)
    async def button_callback(self, button, interaction):
        
        await asyncio.sleep(30)
        await interaction.message.delete()

   



class yesOrNoOption(discord.ui.View):
    @discord.ui.button(label="Да", style=discord.ButtonStyle.green)
    async def yes(self, interaction:discord.Interaction, button: discord.ui.button):
        tchannel = interaction.channel
        lchannel = bot.get_channel(ticketTranscriptChannelID)
        author = interaction.user
        guild = interaction.guild
        connection = TicketData.connect()
        cursor = TicketData.cursor(connection)
        ticketInfo = TicketData.find(cursor, tchannel.id)
        syslogc = get(guild.channels, id=ticketLogsChannelID)
        embed4 = discord.Embed(description=f'Сохранение тикета / Transcribing Ticket...', color=embedColor)
        embed4.set_author(name=f'{author}', icon_url=author.display_avatar)
        #embed4.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
        try:
            await interaction.response.edit_message(embed=embed4, view=None)
        except discord.HTTPException:
            await interaction.response.edit_message(f"Сохранение тикета / Transcribing Ticket...", )
        connection = TicketData.connect()
        cursor = TicketData.cursor(connection)
        embed3 = discord.Embed(title=f'Заявка закрыта / Ticket Closed', description=f'{author.mention} закрыл эту заявку, канал будет удалён через 5 секунд. / {author.mention} has closed this ticket, it will be logged and deleted within 5 seconds.', color=embedColor)
        #embed3.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
        try:
            await tchannel.send(embed=embed3)
        except discord.HTTPException:
            await tchannel.send(f"{author.mention} закрыл эту заявку, канал будет удалён через 5 секунд. / {author.mention} has closed this ticket, it will be logged and deleted within 5 seconds.")
        await asyncio.sleep(2)
        transcript = await chat_exporter.export(tchannel)
        transcript_file = discord.File(io.BytesIO(transcript.encode()),
                                       filename=f"transcript-{tchannel.name}_{tchannel.id}.html") 
        transcript_message = await lchannel.send(file=transcript_file)
        
        tauthor = await bot.fetch_user(int(ticketInfo[1]))
        embed2 = discord.Embed(title=f'[Внутрисерверная] Заявка сохранена и закрыта / The application has been saved and closed', description=f'Заявка была закрыта, сохранена и удалена участником: {author.mention}. / A open ticket has been marked as closed by {author.mention}, it has been logged and deleted.', color=embedColor)
        embed2.set_thumbnail(url="https://static-00.iconduck.com/assets.00/memo-emoji-1948x2048-bgnk0vsq.png")
        embed2.set_author(name=author, icon_url=author.display_avatar)
        #embed2.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
        embed2.add_field(name='**__Channel Name:__**', value=f'#{tchannel.name}', inline=True)
        embed2.add_field(name="**__Author:__**", value=f"{tauthor.mention}", inline=True)
        embed2.add_field(name="**__Squadron/qestion:__**", value=f"{ticketInfo[4]}", inline=True)
        embed2.add_field(name="**__ID автора:__**", value=f"{tauthor.id}", inline=True)
        if dmTicketCopies == True:    # Дублирование автору заявки
            try:
                transcript_file1 = discord.File(io.BytesIO(transcript.encode()),
                                       filename=f"transcript-{tchannel.name}_{tchannel.id}.html") 
                transcript_message1 = await tauthor.send(file=transcript_file1)
                embed3 = discord.Embed(title="Ticket Copy", description=f"Hi {tauthor.mention}!\n Thank you for creating a ticket with us. Attached to this message is a copy of your ticket for your records.\n\nPlease note, any media sent in your ticket will not load in the copy after a couple of days.\n \n ", color=embedColor)
                embed3.add_field(name="**__Jump/Download Link:__**", value=f"{transcript_message1.jump_url}", inline=True)
                transcript_url1 = ("http://v927477t.beget.tech/chat-exporter/?url="+ transcript_message1.attachments[0].url)
                embed3.add_field(name="**__View Link:__**", value=f"[Click here!]({transcript_url1})", inline=True)
                embed3.set_thumbnail(url="https://static-00.iconduck.com/assets.00/memo-emoji-1948x2048-bgnk0vsq.png")
                try:
                    await tauthor.send(embed=embed3)
                except discord.HTTPException:
                    await tauthor.send(f"Hi {tauthor.mention}!\n Thank you for creating a ticket with us. Attached to this message is a copy of your ticket for your records.\nPlease note, any media sent in your ticket will not load in the copy after a couple of days.\n**__Jump/Download Link:__{transcript_message.jump_url}\n**__View Link:__**[Click here!]({transcript_url1})")
                embed2.add_field(name="**__Copy Status:__**", value="A copy of the ticket was successfully delivered to the ticket creator. ✅")
            except Exception:
                embed2.add_field(name="**__Copy Status:__**", value="The copy failed to be delivered to the ticket creator. This is most likely due to their dms being off. ❌")
        else:
            pass
        embed2.add_field(name="**__Время создания/Time created:__**", value=f"{ticketInfo[3]}", inline=False)
        embed2.add_field(name="**__Сохраненная переписка:__**", value=f"\n{transcript_message.jump_url}", inline=True)
        transcript_url = ("http://v927477t.beget.tech/chat-exporter/?url="+ transcript_message.attachments[0].url)
        embed2.add_field(name="**__Ссылка:__**", value=f"\n[Click here!]({transcript_url})", inline=True)
        try:
            message3 = await syslogc.send(embed=embed2)
        except discord.HTTPException:
            message3 = await syslogc.send(f"Канал заявки **{tchannel.mention}** закрыт офицером {author.mention}, он был сохранен и удален.")
        await tchannel.delete()
        TicketData.delete(connection, cursor, tchannel.id)
        TicketData.close(connection)
    @discord.ui.button(label="Нет", style=discord.ButtonStyle.red)
    async def no(self, interaction:discord.Interaction, button: discord.ui.button):
        author = interaction.user
        embed4 = discord.Embed(description="Отмена...", color=embedColor)
        embed4.set_author(name=f'{author}', icon_url=author.display_avatar)
        # embed4.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
        try:
            await interaction.response.edit_message(embed=embed4, view=None)
        except discord.HTTPException:
            await interaction.response.edit_message("Отмена...", view=None)

class ticketArchiveyesOrNoOption(discord.ui.View):
    @discord.ui.button(label="Да", style=discord.ButtonStyle.green)
    async def yes(self, interaction:discord.Interaction, button: discord.ui.button):
        tchannel = interaction.channel
        author = interaction.user
        guild = interaction.guild
        syslogc = get(guild.channels, id=ticketLogsChannelID)
        connection = TicketData.connect()
        cursor = TicketData.cursor(connection)
        ticketInfo = TicketData.find(cursor, tchannel.id)
        categoryn = archivedTicketsCategoryID
        embed4 = discord.Embed(description=f'Присвоение заявке статуса `Архивировано`/Setting Ticket to `Archived` status...', color=embedColor)
        embed4.set_author(name=f'{author}', icon_url=author.display_avatar)
        #embed4.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
        try:
            message3 = await interaction.response.edit_message(embed=embed4, view=None)
        except discord.HTTPException:
            message3 = await interaction.response.edit_message(f"Присвоение заявке статуса `Архивировано`/Setting Ticket to `Archived` status...", view=None)
        category = discord.utils.get(guild.categories, id=categoryn)
        await tchannel.edit(category=category)
        TicketData.edit(connection, cursor, ticketInfo, ticketInfo[2], "Archived")
        embed1 = discord.Embed(title='__**Статус заявки изменен/Ticket Status Changed**__', description=f'Статус изменен на `архивировано`/This ticket has been set to `Archived` ✅', color=embedColor)
        embed1.set_author(name=f'{author}', icon_url=author.display_avatar)
        #embed1.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
        try:
            message3 = await tchannel.send(embed=embed1)
        except discord.HTTPException:
            message3 = await tchannel.send(f"**Статус изменен на `Архивировано`/This ticket has been set to `Archived` ✅**")
        embed2 = discord.Embed(title='Заявка помещена в архив/Ticket set to Archived', description=f'Ticket {tchannel.mention} has been set to `Archived` by {author.mention} / Заявка {tchannel.mention} была архивирована пользователем {author.mention}', color=embedColor)
        #embed2.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
        try:
            await syslogc.send(embed=embed2)
        except discord.HTTPException:
            await syslogc.send(f"Ticket {tchannel.mention} has been set to `Archived` by {author.mention} / Заявка {tchannel.mention} была архивирована пользователем {author.mention}")   
        TicketData.delete(connection, cursor, tchannel.id)
        TicketData.close(connection)
    @discord.ui.button(label="Нет", style=discord.ButtonStyle.red)
    async def no(self, interaction:discord.Interaction, button: discord.ui.button):
        author = interaction.user
        embed4 = discord.Embed(description="Отмена...", color=embedColor)
        embed4.set_author(name=f'{author}', icon_url=author.display_avatar)
        #embed4.set_footer(text=f"{footerOfEmbeds} | {bot.user.id}", icon_url=f'{bot.user.display_avatar}')
        try:
            await interaction.response.edit_message(embed=embed4, view=None)
        except discord.HTTPException:
            await interaction.response.edit_message("Отмена...", view=None)