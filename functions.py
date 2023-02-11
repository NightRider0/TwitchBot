import socket
import os
import openai
import requests
import json
import time
import sys

from Global_Vars import MESSAGECOUNT, start_time, message_counter, commandsfile, ucommands, HOST, PORT,s
from  Creds import NICK,PASS,CHAN,OPENAPI


a_message = {}
a_time = {}
a_count = {}
a_message['test'] = "auto meassage testing"
a_time['test'] = 5
a_count['test'] = 3

def twitch_connect():
    s.connect((HOST, PORT))
    s.send("CAP REQ :twitch.tv/commands twitch.tv/tags\n".encode("utf-8"))
    s.send(f"PASS {PASS}\n".encode("utf-8"))
    s.send(f"NICK {NICK}\n".encode("utf-8"))
    s.send(f"JOIN #{CHAN}\n".encode("utf-8"))
    print

with open(commandsfile, "r") as file:
    lines = file.readlines()
    for line in lines:
     words = line.strip().split()
     text = " ".join(words[1:])
     ucommands[words[0]] = text

def auto_anouncments():
    MESSAGECOUNT
    unix_time = int(time.time())
    a_intervalC = {}
    a_intervalT = {}
    for key, a_msg in a_message.items():
        a_intervalC[key] = a_count[key]
        a_intervalT[key] = a_time[key]
        a_count[key] = MESSAGECOUNT + a_count[key]
        a_time[key] = unix_time + a_time[key]
    
    while True:
        for key, a_msg in a_message.items():
            unix_time = int(time.time())
            if unix_time >= a_time[key] and MESSAGECOUNT >= a_count[key]:
                send_message(a_msg)
                print(a_msg)
                a_count[key] = a_intervalC[key] + MESSAGECOUNT
                a_time[key] = a_intervalT[key] + unix_time
                time.sleep(10)                
            elif unix_time >= a_time[key] and MESSAGECOUNT <= a_count[key]:
               a_time[key] = a_intervalT[key] / 2 + unix_time
               time.sleep(1)
            else:
                time.sleep(1)

# Respond to chat messages
def respond_to_chat_messages():
    while True:
        message = input("~~>")
        s.send(f"PRIVMSG #{CHAN} :{message}\n".encode("utf-8"))

def send_message(message):
    # Function to send a message to Twitch chat
    global message_counter, start_time

    current_time = time.time()
    if current_time - start_time >= 10:
        message_counter = 0
        start_time = current_time

    if message_counter < 30:
        s.send(f"PRIVMSG #{CHAN} :{message}\r\n".encode("utf-8"))
        message_counter += 1
    else:
        print("sending messages paused -- Rate limiting!!!")
        pass


def add_cmd(message):
     
    words = message.split()
    text = " ".join(words[2:])
    if words[1] in ucommands:
        send_message(words[1]+" -- already exist, plesase use \"!upcmd "+words[1]+" "+text+"\"")
    else:
        ucommands[words[1]] = text
        send_message(words[1]+" was created!")
        with open(commandsfile, "w") as file:
            for key, value in ucommands.items():
                file.write(key + " " + value + "\n")

def update_cmd(message):
     
    words = message.split()
    text = " ".join(words[2:])
    if words[1] not in ucommands:
        send_message(words[1]+" -- does not exist, plesase use \"!addcmd "+words[1]+" "+text+"\"")
    else:
        ucommands[words[1]] = text
        send_message(words[1]+" was updated!")
        with open(commandsfile, "w") as file:
            for key, value in ucommands.items():
                file.write(key + " " + value + "\n")

def del_cmd(message):
    try:
        words = message.split()
        del ucommands[words[1]]
        send_message(words[1]+" was deleted")

        with open(commandsfile, "w") as file:
            for key, value in ucommands.items():
                file.write(key + " " + value + "\n")

    except:
        send_message(words[1]+" did not exist")

def ask_openai(message):
    try:
     openai.api_key = OPENAPI
     response = openai.Completion.create(
       engine="text-davinci-003",
       prompt=message,
       temperature=0,
       max_tokens=64,
       top_p=1,
       frequency_penalty=0,
       presence_penalty=0,
       stop=["{}"]
     )
     return response.choices[0].text
    except:
        return "Sorry try agagin in a few minutes"
    
