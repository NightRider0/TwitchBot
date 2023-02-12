import socket
import os
import openai
import requests
import json
import time
import sys
from Global_Vars import MESSAGECOUNT, commandsfile, ucommands,s
from Creds import NICK, CHAN, PASS
from functions import auto_anouncments, send_message, respond_to_chat_messages, add_cmd, del_cmd, update_cmd,add_auto, ask_openai, twitch_connect

with open(commandsfile, "r") as file:
    lines = file.readlines()
    for line in lines:
     print(line)
     words = line.strip().split()
     text = " ".join(words[1:])
     ucommands[words[0]] = text


# Connect to Twitch IRC
twitch_connect()

# Receive messages from Twitch IRC
def receive_messages():
    buffer = ""
    import Global_Vars 
    while True:
        buffer += s.recv(1024).decode("utf-8")
        lines = buffer.split("\r\n")
        buffer = lines.pop()

        for line in lines:
            if line.startswith("PING"):
                s.send("PONG\n".encode("utf-8"))
            elif "PRIVMSG" in line:
                #print(line)
                #username = line.split("!", 1)[0][1:]
                username = line.split(";")[4].split("=")[1].lower()
                message = line.split("PRIVMSG #" + CHAN + " :", 1)[1]
                tags_section = line.split(" ", 2)[0][1:]
                tags = tags_section.split(";")
                tags_dict = {}
                for tag in tags:
                 key, value = tag.split("=")
                 tags_dict[key] = value

                if username.strip() == "":
                    username = tags_dict['display-name'].lower()

                permitted = "night_rider0, daycarlyon, smilinsarahk, thorkull, mscuppykate, jodankgames, sketch"
                Mod = ""
                global MESSAGECOUNT
                #print(tags_dict)
                
                if tags_dict['mod'] == '1':
                    Mod = "MOD: "
                
                if username == CHAN:
                    tags_dict['mod'] = '1'
                    Mod = "BROADCASTER: "
       
                if "hello" in message.lower().split() and NICK != username:
                    send_message("Hello "+username)
                
                if "hi" in message.lower().split() and NICK != username:
                    send_message("Hi "+username)
                
                if "bye" in message.lower().split() and NICK != username:
                    send_message("See you later "+username)

                if "q." in message.lower().split() and username in permitted:
                    reply = ask_openai(message)
                    send_message(username+" "+reply.strip('\n\n'))
                
                if "!msgcount" in message.lower().split():
                    send_message("There have been "+str(Global_Vars.MESSAGECOUNT)+" messages sent in chat since my last restart")

                if "!lurk" in message.lower().split():
                    send_message("I appreciate you "+username+", enjoy the lurk!")
                
                if message.lower() in ucommands:
                    send_message(ucommands[message])

                if "!addcmd" in message.lower().split() and tags_dict['mod'] == '1':
                    add_cmd(message)
                
                if "!delcmd" in message.lower().split() and tags_dict['mod'] == '1':
                    del_cmd(message)
                
                if "!rmcmd" in message.lower().split() and tags_dict['mod'] == '1':
                    del_cmd(message)
                
                if "!upcmd" in message.lower().split() and tags_dict['mod'] == '1':
                    update_cmd(message)
                
                if "!lscmd" in message.lower().split() and tags_dict['mod'] == '1':
                    keys = list(ucommands.keys())
                    keys_stirng =", ".join(keys)
                    send_message("the following commands exist: "+keys_stirng)
                
                if "!addauto" in message.lower().split() and tags_dict['mod'] == '1':
                    add_auto(message)
                    
                print(f"{Mod}{username}: {message}")
                              
                Global_Vars.MESSAGECOUNT = Global_Vars.MESSAGECOUNT + 1

            elif "USERNOTICE" in line:
                print(line)

# Start both threads
import threading
receive_thread = threading.Thread(target=receive_messages)
anouncments_thread = threading.Thread(target=auto_anouncments)
respond_thread = threading.Thread(target=respond_to_chat_messages)
receive_thread.start()
anouncments_thread.start()
respond_thread.start()

#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
#org-FPdRCttTbXKVJP1dx7vaLhXt
