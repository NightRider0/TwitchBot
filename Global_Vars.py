import time
import socket
import sys
import array

    

# Socket base
s = socket.socket()

# Twitch info
HOST = "irc.chat.twitch.tv"
PORT = 6667


#global vars
MESSAGECOUNT = 0 #Messages since the bot last restarted, used in auto messages and !msgcount command
ucommands = {} # starting point for user added commands
commandsfile = "ucommands.txt" # file we saves user created commands too
