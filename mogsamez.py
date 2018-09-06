import json
import discord
import pydle
import asyncio
import decks
import random
import randomorg
import pyimgur
import math
from PIL import Image
import os
from tornado.platform.asyncio import AsyncIOMainLoop
AsyncIOMainLoop().install()


#                                                                                                                                                                                     
#                                                                                                                                                                                     
#                                                                                                                                                                                     
#                                                                                                                                                                                     
#      MMMMMMM$      MMMMMMM                                                                                                                                                          
#      MMMMMM        $MMMMMM                                                                                                                                                          
#      MMMMMM        :MMMMMM        MMMMMDZNMMMMMM,       MMMMMMMMMMMN           ~MMMMMMMMM      ,DMMMMMN :MMMMM      ZMMMMM     +MMMMM              =DMMMMM      : :8MMMM,           
#      MMMMMMD       OMMMMMM        :MMMMM   MMMM         MM     +MMM,             ZMZ   DM$         MM,    MM,       DMMMM       MMMMM                  IMM         MM?              
#      MMMMMMM       MMMMMMM        MMMM?     MMMM        M        MMM,              NM   =M         MM    MM         MMMMM?      MMMMM                   ?M       MMMMMMD~           
#      MMM  8MM     MM  MMMM        MMMM       MMMN                MMMM      =:       MN            DMD    M          MMMMMM     OMMMMM                    M       8MMMMMM:           
#      MM,   ,MM   MM   7MMM       +MMM        7MMM                +MMM       ~MMMMMMMNM           ZMM=    M          MM8  MM   +M  MMM      :             M        MMMMMM            
#      MM     ,MMMMM     MMM       NMM$   MMI   MMM                 MMM         IMMM MMM?          MMM,    M          MM    MM IM,  MMM      M            =M        MMMMM             
#      MM        MD      MMM       MMM    MMM   MMM                 MMM           8MM  8          7MMM                DM     ?MN    ZMM      MM=         ZMM        ,MMMM             
#      MO                MMM,      MMM    MMO   =MM                 MM,            :MM             MMM                78            ~MM      MMMMMMMMMMMMMMM         MMMO             
#      IN                MMM,      =MM          ,MM                7MM               MM            $MM,                N            ~MM      MMM?        ~MM         OMM,             
#       M                MMM        MM           MM                MM                 MM            NM8                N            :MM      MM            M          MM              
#                        MMM        OM           MM                M+                  M$            MM                             :MM      MM                       MM              
#                        MMM         M7          MM               MI                   ZM             MM                            ~MM      MM                       MM              
#                        MMN          M          M,              MM                     M              M~  :,                       ZM:      MM                       NM              
#                        MM           ,M        MN             ,M8                      M              :M  M                        MM       MMZ                      ,M              
#                       :MM            ,M      DM              MZ                       M                MM                         M$       MMMM                      M              
#                       NM:                   ?I             ,M                        M                  M                        M7        MMMMMMMMMMMMMM            M              
#                       MM                   7              M:                        N                                           M                                    I              
#                      MM                                                           =  ,                                                                                              
#                     M?                                                                                                                                                              
#                                                                                                                                                                                     
#                                                                                                                                                                                     
#                                                                                                                                                                                     
#                                                                                                                                                                                     
#                                                                                                                                                                                     


imagenamecounter = 0

with open("client_data.json", "r") as f:
  clientdata = json.load(f)

global wordlist
with open("words", "r") as f:
    wordlist = f.read().split("\n")

def celticcross():
  cardwidth = 280
  cardheight = 417
  horizontalspace = 10
  verticalspace = 10

  squaresize = cardwidth*2 + cardheight + horizontalspace*4
  maxheight = cardheight*4 + verticalspace*5
  squareheight = (maxheight - squaresize)/2

  image = Image.new("RGB", (squaresize + cardwidth + horizontalspace, maxheight), color=(0, 0, 0))

  cardfiles = ["thoth/{}.jpg".format(c) for c in random.sample(range(1, len(decks.THOTH)), 10)]
  cards = [Image.open(c) for c in cardfiles]

  image.paste(cards[0], (int(squaresize/2-cardwidth/2), int(maxheight/2-cardheight/2)))
  image.paste(cards[1].rotate(90, expand=True), (int(squaresize/2-cardheight/2), int(maxheight/2-cardwidth/2)))
  image.paste(cards[2], (int(squaresize/2-cardwidth/2), int(maxheight-squareheight-cardheight/2)))
  image.paste(cards[3], (int(horizontalspace), int(maxheight/2-cardheight/2)))
  image.paste(cards[4], (int(squaresize/2-cardwidth/2), int(squareheight-cardheight/2)))
  image.paste(cards[5], (int(squaresize-horizontalspace-cardwidth), int(maxheight/2-cardheight/2)))

  for i in range(4):
      image.paste(cards[6+i], (int(squaresize), int(verticalspace + i*(cardheight+verticalspace))))

  global imagenamecounter
  image.save("{}.png".format(imagenamecounter))
  imgurclient = pyimgur.Imgur(clientdata["imgurid"])
  upload = imgurclient.upload_image(os.getcwd()+"/{}.png".format(imagenamecounter))
  os.remove(os.getcwd()+"/{}.png".format(imagenamecounter))
  imagenamecounter += 1
  return upload.link

def containsflag(message, flag):
  msg = message.lower()
  if flag in msg:
    if msg.index(flag) > 0:
      if msg[msg.index(flag)-1].isalnum():
        return False
    try:
      if msg[msg.index(flag)+len(flag)].isalnum():
        return False
    except IndexError:
      pass
    return True
  return False

def selectresponse(message, medium):
  if containsflag(message, "trng"):
    try:
      random.seed(randomorg.rrandom())
    except Exception as err:
      return err

  if containsflag(message, "words"):
    nwords = random.randint(1, 5)
    sentence = " ".join([random.choice(wordlist) for n in range(nwords)]).capitalize() + "."
    return sentence

  if containsflag(message, "celtic cross"):
    link = celticcross()
    if medium == "irc":
      return "Cast cards: {0} (Meanings: https://goo.gl/ZEwmwd".format(link)
    elif medium == "discord":
      return "Cast cards: <{0}> (Meanings: <https://goo.gl/ZEwmwd>".format(link)
    else:
      raise("Unknown medium flag:", medium)

  if containsflag(message, "haindl"):
    deck = decks.HAINDL
  elif containsflag(message, "rw"):
    deck = decks.RW_DECK
  else:
    deck = decks.THOTH

  if containsflag(message, "spread"):
    cards = random.sample(deck, 3)
  else:
    cards = [random.choice(deck)]
  if medium == "irc":
    return " ".join([card[0] + " { " + card[1] + " }" for card in cards])
  elif medium == "discord":
    return " ".join(["{0} <{1}>".format(card[0], card[1]) for card in cards])
  else:
    raise("Unknown medium flag:", medium)



discordclient = discord.Client()

@discordclient.event
@asyncio.coroutine
def on_message(message):
  if containsflag(message.content, "mog")  or containsflag(message.content, "mogsamez")\
      or discordclient.user.mentioned_in(message=message) or isinstance(message.channel, discord.PrivateChannel)\
      and not message.author.bot:
    try:
      response = message.author.mention + ": " + selectresponse(message.content, "discord")
      yield from discordclient.send_message(message.channel, response)
    except discord.errors.Forbidden:
      pass

class IRCClient(pydle.Client):
  def on_connect(self):
    self.join('#/div/ination')

  def on_channel_message(self, channel, nick, message):
    if containsflag(message, "mog") or containsflag(message, "mogsamez"):
      response = nick + ": " + selectresponse(message, "irc")
      self.message(channel, response)

  def on_private_message(self, nick, message):
    response = nick + ": " + selectresponse(message, "irc")
    self.message(nick, response)

ircclient = IRCClient('Mogsamez', realname='Mogsamez')
ircclient.connect('irc.us.sorcery.net', 6667)


discordclient.run(clientdata["token"])