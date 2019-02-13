import json
import pprint
# kik_unofficial API
from kik_unofficial.client import KikClient
from kik_unofficial.callbacks import KikClientCallback
from kik_unofficial.datatypes.xmpp.chatting import IncomingChatMessage, IncomingGroupChatMessage, IncomingStatusResponse, IncomingGroupStatus
import kik_unofficial.datatypes.xmpp.chatting as chatting

# Fetch the credentials
with open('../credentials.json') as f:
    credentials = json.load(f)

# Helper methods
def dump(obj):
    print(type(obj))
    print(dir(obj))
    print(id(obj))
    print(callable(obj))

def jid_to_username(jid): return jid.split('@')[0][0:-4]

# The main class
class Rip(KikClientCallback):
    def __init__(self):
        self.client = KikClient(self, credentials["username"], credentials["password"])

    def on_authenticated(self):
        self.client.request_roster()

    def on_chat_message_received(self, chat_message: chatting.IncomingChatMessage):
        print(jid_to_username(chat_message.from_jid) + " (PM): " + chat_message.body) 
        self.client.send_chat_message(chat_message.from_jid, "You said: " + chat_message.body)

    def on_group_message_received(self, chat_message: IncomingGroupChatMessage):
        ban_text = "Pepe and the fisher man says"

        # The health check
        if(chat_message.body.lower() == "rip"):
            self.client.send_chat_message(chat_message.group_jid, "Ribs in peas")

        # Help text
        if(chat_message.body.lower() == "help"):
            help_text = ":$ Commands of RIP :$\n\n\
:$ \"RIP\" -> \"Ribs in peas\", for checking if the bot is up - \
if not, Saku is probably on drunk and peed on the laptop which runs this bot, -or something  \n\n\
:$ \"" + ban_text + "\" and i will kick your butt ...I mean for real. I will remove you from the group\
 and try to ban you. (I can't do it if there is already 50 banned peeps) :$\n\n\
:$ I will have something fancier later :$"
            self.client.send_chat_message(chat_message.group_jid, help_text)

        # Should we copy this feature from rage bot?
        if" -> " in chat_message.body: self.client.send_chat_message(chat_message.group_jid, "Should I do also Trigger - Response? : $")

        # For logging purpose
        if "Last lurking activity:" in chat_message.body: print(chat_message.body)
        if "saku" in chat_message.body.lower(): print(chat_message.body)

        # The illegal phrase check
        ban_text = "Pepe and the fisher man says"
        if "Pepe and the fisher man says".lower() in  chat_message.body.lower():
            self.client.remove_peer_from_group(chat_message.group_jid, chat_message.from_jid)
            self.client.ban_member_from_group(chat_message.group_jid, chat_message.from_jid)
            self.client.send_chat_message(chat_message.group_jid, "Removed user with JID '" + chat_message.from_jid + "' because the user used an illegal phrase '" + ban_text + "' in the message.")

# Main
bot = Rip()

# Note to myself
"""
    chat_message: IncomingGroupChatMessage
        '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__',
        'body', 
        'from_jid',
        'group_jid', 
        'is_typing', 
        'message_id', 
        'metadata', 'preview', 
        'raw_element', 
        'request_delivered_receipt', 
        'request_read_receipt', 
        'status', 
        'to_jid'
"""