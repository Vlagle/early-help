#--------Ticket-Bot Config File--------#
#Created by WebTheDev#

#PLACE THE TOKEN FOR THE BOT IN THE TOKEN.JSON FILE!!!!#

import json

#Main Config:#
botStatusType = ''                                                   #Bot Status Type (Ex. Playing, Watching, Listening, or Streaming)
botStatusMessage = ''                                                #The message that is shown on the bots activity
guildID = 994209405908291727                                          #ID of the Guild the the bot is running in
ticketLogsChannelID = 1235267354498306169                             #ID of the Channel to send system logs to
ticketTranscriptChannelID = 1235267408852418654                    #ID of the Channel to send ticket transcripts to
databaseName = 'tickets.db'                                          #Leave set to default value unless if you want to use a different database name
debugLogSendID = 1235267502313967676                                #ID of the Bot Owner to send debug information to

#Ticket Creation/Options Config:#
IDOfChannelToSendTicketCreationEmbed = 1236028561136291870             #ID of the Channel to send the Create a ticket embed to
IDofMessageForTicketCreation = 1236645848327389275                       #This variable was automatically adjusted.
activeTicketsCategoryID = 1236028646733643879                     #ID of the active tickets category
onHoldTicketsCategoryID = 1235298152261746750                           #ID of the onhold tickets category
archivedTicketsCategoryID = 1235298217537699880             #ID of the archived tickets category

OptionsDict = {
    "Option 1": ("EARLY", "early", "EARLY - для ежедневных полковых боёв \n EARLY - for squadron battles "),                                      #This is the ticket options dictionary. It defines the different types of tickets that users can create.
    "Option 2": ("E4RLY", "e4rly", "E4RLY - русско-язычный полк для фарма техники и полковых боев"),                                #A ticket option definition should look something like this:  
    "Option 3": ("ENRLY", "enrly", "ENRLY - english-speaking squadron for farming equipment and squadron battles") ,
    "Option 4": ("Вопрос руководству / Question to the management", "qestion", "Вопрос руководству / Question to the management."),
    "Option 5": ("Отряд / team", "team", "Сбор отряда для полковых боев. Только после согласованеия с руководством или офицерами.") 
    #"Option #": ("Title of Option", "Type of Option", "Description of Option")
}                                                                                                             #Add a comma after every option definition except for the last one. 
                                                                                                              #If you only have one option then no comma is needed.


channelPerms = {                                                                                          #This is the ticket channel perms dictionary.
    "early": (994215060052381706, 994226835795746867),                                                                     #This dictionary defines what roles will have access to each type of Ticket Channel
    "e4rly": (994215060052381706, 1178285446158094386, 1213575945991102504),                                           #Each type can support multiple role IDS
    "enrly": (994215060052381706, 1230216013195513928, 1230216099228942489) ,
    "qestion": (994215060052381706, 1213575945991102504, 1230216099228942489),
    "team": (994215060052381706)
  
}                                                                                                                         #"Type of Option":(ROLEID1, ROLEID2)
                                                                                                          #Add a comma after every option definition except for the last one. 
                                                                                                          #If you only have one option then no comma is needed.
                                                                                                          #IMPORTANT: MAKE SURE THAT THE TYPE OF OPTION IS THE SAME AS THE TYPE OF OPTION THAT WAS
                                                                                                          #DEFINED IN THE TICKET OPTIONS DEFINITION
                                                                                                          #IF NOT, PERMISSIONS WILL NOT BE SET CORRECTLY AND THE BOT WILL NOT WORK RIGHT.


ticketTypeAllowedToCreatePrivateChannels = "staff"                         #Set this to be the type of option (roles) as defined in the ticket channel perms dictionary that can use the /create command.
multipleTicketsAllowed = True                                             #Set this to True if you would like members to be able to have multiple tickets open at once (otherwise set to False).
dmTicketCopies = False                                                      #Set this to True if you would like the bot to dm Ticket Creators transcript copies of their ticket.


#Embed Config:#
footerOfEmbeds = ''                                                        #Set a custom embed footer of all embedded messages here!
embedColor = 0xffffff                                                      #Set a custom hex color code for all embeds! Make sure to keep the 0x!


def get_token():                                                    
    tokenFile = open("./token.json")                                       #This definition pulls the token from the token.json file
    data = json.loads(tokenFile.read())                                    #Make sure to put your token in the token.json file where it says "PLACETOKENHERE"!                                     
    return (data['BotToken'])


firstRun = False               #This variable was automatically adjusted.



#Please create a new issue on github if you are having issues with using the bot or find any bugs!