import json
from pprint import pprint

from kik_unofficial.client import KikClient
from kik_unofficial.callbacks import KikClientCallback
from kik_unofficial.datatypes.xmpp.chatting import IncomingChatMessage, IncomingGroupChatMessage, IncomingStatusResponse, IncomingGroupStatus
import kik_unofficial.datatypes.xmpp.chatting as chatting

# Fetch the credentials
with open('../credentials.json') as f:
    data = json.load(f)

username = data["username"]
password = data["password"]

# The main class
class Rip(KikClientCallback):
    def __init__(self):
        self.client = KikClient(self, username, password)

    def on_authenticated(self):
        self.client.request_roster()

    def on_chat_message_received(self, chat_message: chatting.IncomingChatMessage):
        if "Rip" in chat_message.body:
            self.client.send_chat_message(chat_message.from_jid, "Ribs in peas")
        if "rip" in chat_message.body:
            self.client.send_chat_message(chat_message.from_jid, "Ribs in peas")

    def on_group_message_received(self, chat_message: IncomingGroupChatMessage):
        print(chat_message.body);

        if "Rip" in chat_message.body:
            self.client.send_chat_message(chat_message.group_jid, "Ribs in peas")
        if "rip" in chat_message.body:
            self.client.send_chat_message(chat_message.group_jid, "Ribs in peas")


bot = Rip()
