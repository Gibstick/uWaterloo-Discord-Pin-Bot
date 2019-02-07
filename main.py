#--- Imports
import discord # Imports discord library.
import sys # Imports sys library. 

client = discord.Client() # Initializes bot as client.


@client.event 
async def on_ready(): # When the bot goes online, the following code is executed.
  print(str(client.user) + ' is online.') # Prints operaitonal message.
     
@client.event
async def on_message_edit(before, after): # The following code is executed on message edit even (whenever a message is pinned/edited).
  x = await client.pins_from(before.channel) # Returns list of pins as message objects.
  pinnedIds = [message.id for message in x]
  pinnedContent = [message.content for message in x] # List of strings for message objects in x. 
  attachments = before.attachments # Returns list of message attachments in dictionaries.

  if before.author != client.user and before.id in pinnedIds and before.author.bot == False and before.content != '': # If the message was not sent by a bot, and is the last pinned message in the channel, the following code is executed.
    name = before.author.display_name # Name as author of message.
    avatar = before.author.avatar_url # Avatar as avatar url of message author.
    pinContent = before.content # pinContent as string of pinned message.
    msgChannel = before.channel # msgChannel as channel name the message was pinned in.
   
    emb = discord.Embed(description = pinContent, color = 0xcf1c43) # Initalizes embed with description pinContent.
    emb.set_author(name=name, icon_url=avatar) # Sets author and avatar url of the author of pinned message.
    
    if attachments != []: # If the pinned message has an attachment, the following code is executed.
      imgContent = attachments[0]['url'] # Gets url of the attachment.
      emb.set_image(url=imgContent) # Sets image url as embed image.
      
    emb.set_footer(text='Sent in #{}'.format(msgChannel)) # Sets footer as the channel the message was sent and pinned in.
    await client.send_message(discord.Object(id='538545784497504276'), embed=emb) # Sends message containing embed to specified channel (presumably a log channel i.e #pins-archive).

@client.event
async def on_reaction_add(reaction, user):
  if reaction.emoji == '📌':
    if reaction.count == 1:
      try:
        await client.pin_message(reaction.message)
      except discord.errors.HTTPException:
        x = await client.pins_from(message.channel)
        pinnedIds = [message.id for message in x]
        oldestPin = await client.get_message(message.channel, pinnedIds[0])
        await client.unpin_message(oldestPin)
        await client.pin_message(reaction.message)
 
@client.event
async def on_message(message): # The following code is executed on message event, parameter message.
  userRoles = [role.name for role in message.author.roles]
  if message.author != client.user: # If the message is not from a bot, the following code is executed.
    if message.content.startswith('+lastpin'): # If a user enters a message starting with +lastpin, the following code is executed.
      x = await client.pins_from(message.channel) # Returns list of pins as message objects. 
      pinnedNames = [message.author.display_name for message in x] # list of names for message objects in x.
      pinnedAvatars = [message.author.avatar_url for message in x] # list of avatar urls for message objects in x.
      pinnedContent = [message.content for message in x] # list of message strings for message objects in x.
      attachments = [message.attachments for message in x]
     
      emb = discord.Embed(description = pinnedContent[0], color = 0xcf1c43) # Intilializes embed with description as index 0 of pinnedContent.
      emb.set_author(name=pinnedNames[0], icon_url=pinnedAvatars[0]) # Sets the embeds avatar and name that matches to the corresponding information in x.
      
      if attachments[0] != []: # If the pinned message has an attachment, the following code is executed.
        imgContent = attachments[0][0]['url'] # Gets url of the attachment.
        emb.set_image(url=imgContent) # Sets image url as embed image.
        
      await client.send_message(message.channel, embed=emb) # Sends message containing embed to channel message was executed in. 
    
    if message.content.startswith('+maintenance') and message.author.id == '357652932377837589': #If the message starts with +maintenance, and was made by user @Nitr0us#5090, the following code is executed:
      emb = discord.Embed(description = 'Pin Archiver is down for maintenance.', color = 0xcf1c43) # Initalizes embed with description pinContent.
      await client.send_message(discord.Object(id='538545784497504276'), embed=emb) # Sends message containing embed to specified channel (presumably a log channel i.e #pins-archive).
    
    if message.content == str('+status'): # If the message starts with +status, the following code is executed.
      emb = discord.Embed(description = 'Online.', color = 0xcf1c43) # Intilializes embed with online message.
      await client.send_message(message.channel, embed=emb) # Sends message containing embed to channel message was executed in. 
      
    if message.content.startswith('+del'): # If the message starts with +del, the following code is executed.
      if str('Administrator') in userRoles or str('Moderator') in userRoles or message.author.id == '357652932377837589': # If the user is an Administrator, Moderator or @Nitr0us#5090 the following code is executed.
        async for message in client.logs_from(discord.Object(id='538545784497504276'), limit = 1): # Fetches last message in the channel #pin-archive
          lastMessage = message # Variable for last message sent in #pin-archive
        await client.delete_message(lastMessage) # Deletes lastMessage.
    
    if message.content.startswith('+archive'):
      if str('Administrator') in userRoles or str('Moderator') in userRoles or message.author.id == '357652932377837589': # If the user is an Administrator, Moderator or @Nitr0us#5090 the following code is executed.
        try:
          msgIdToArchive = message.content.replace('+archive ', '')
          msg = await client.get_message(message.channel, msgIdToArchive)
          attachments = msg.attachments # Returns list of message attachments in dictionaries.

          name = msg.author.display_name # Name as author of message.
          avatar = msg.author.avatar_url # Avatar as avatar url of message author.
          pinContent = msg.content # pinContent as string of pinned message.
          msgChannel = msg.channel # msgChannel as channel name the message was pinned in.
   
          emb = discord.Embed(description = pinContent, color = 0xcf1c43) # Initalizes embed with description pinContent.
          emb.set_author(name=name, icon_url=avatar) # Sets author and avatar url of the author of pinned message.
    
          if attachments != []: # If the pinned message has an attachment, the following code is executed.
            imgContent = attachments[0]['url'] # Gets url of the attachment.
            emb.set_image(url=imgContent) # Sets image url as embed image.
      
          emb.set_footer(text='Sent in #{}'.format(msgChannel)) # Sets footer as the channel the message was sent and pinned in.
          await client.send_message(discord.Object(id='538545784497504276'), embed=emb) # Sends message containing embed to specified channel (presumably a log channel i.e #pins-archive).
        
        except discord.errors.HTTPException:
          emb = discord.Embed(description='Error: Message not found, try again.', color = 0xcf1c43)
          await client.send_message(message.channel, embed=emb)
        
    
    if message.content.startswith('+help'): # If the message starts with +help, the following code is executed.
      helpMsg = '''
       __**Information**__:
        
        This bot was made by @Nitr0us#5090, if you have any questions or require support please contact him.
        
       __**Features**__:
        
        **1)** Last Pinned Message:
        Usage: +lastpin 
        Purpose: Displays the last pinned message of the current channel.
        
        **2)** Archive Pinned Messages (Automatic):
        Usage: Automatic
        Purpose: To archive all pinned messages to #pin-archive. 
        
        **3)** Archive Messages (Manual)
        Usage: +archive <messageid>
        Permission: Administrators & Moderators
        Purpose: To archive a message to #pin-archive, regardless whether the message is pinned.
        
        **4)** Status:
        Usage: +status
        Purpose: Notifies you if the bot is online.
        
        **5)** Delete:
        Usage: +del
        Permission: Administrators & Moderators
        Purpose: To delete the last pinned message in #pin-archive.
        

      ''' 
      emb = discord.Embed(description=helpMsg, color = 0xcf1c43) # Intializes embed with help message as description.
      await client.send_message(message.channel, embed=emb) # Sends message containing embed to the channel the command was executed in.


  
client.run(sys.argv[1]) # Runs bot with token as system argument. 
client.close()
  
