import json

# kik_unofficial API
from kik_unofficial.client import KikClient
from kik_unofficial.callbacks import KikClientCallback
from kik_unofficial.datatypes.xmpp.chatting import IncomingChatMessage, IncomingGroupChatMessage, IncomingStatusResponse, IncomingGroupStatus
import kik_unofficial.datatypes.xmpp.chatting as chatting

# local files
from database import db_context

# Fetch the credentials
with open('../config.json') as f:
    config = json.load(f)

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
        self.client = KikClient(self, config["credentials"]["kik-username"], config["credentials"]["kik-password"])

    def on_authenticated(self):
        self.client.request_roster()

    def on_chat_message_received(self, chat_message: chatting.IncomingChatMessage):
        print(jid_to_username(chat_message.from_jid) + " (PM): " + chat_message.body) 
        self.client.send_chat_message(chat_message.from_jid, "You said: " + chat_message.body)

    def on_group_message_received(self, chat_message: IncomingGroupChatMessage):
        msg = chat_message.body.lower()

        # The health check
        if(msg == "rip"): self.client.send_chat_message(chat_message.group_jid, "Ribs in peas")

        # TODO: Create a usage - test (similar than in rage)

        # Should we copy this feature from rage bot?
        elif " -> " in msg: self.client.send_chat_message(chat_message.group_jid, "Should I do also Trigger - Response? : $")

        # For logging purpose
        elif "last lurking activity:" in msg: print(chat_message.body)
        elif "saku" in msg: print(chat_message.body)
        else:
            print("opening the the database connection...")
            with db_context(config) as ctx:
                phrases = ctx.list_illegal_phrases(chat_message.group_jid)

                if msg == "list phrases":
                    if phrases:
                        self.client.send_chat_message(chat_message.group_jid, ", ".join(phrases))
                    else:
                        self.client.send_chat_message(chat_message.group_jid, "No phrases. You can add them by saying \"Add phrase\" and then the phrase you want")

                elif msg.startswith("add phrase "):
                    phrase = chat_message.body[11:]
                    print("Adding new phrase: " + phrase)
                    ctx.add_illegal_phrase(chat_message.group_jid, phrase)
                    self.client.send_chat_message(chat_message.group_jid, "A new phrase added: " + phrase)
                else:
                    print("Comparing phrase with: " + ", ".join(phrases))
                    for phr in phrases:
                        phrase = phr.lower()
                        if phrase in chat_message.body:
                            print("Removing the user '{0}'. The message body matched with a phrase '{1}' The message:".format(chat_message.from_jid, phrase))
                            print(chat_message.body)
                            self.client.remove_peer_from_group(chat_message.group_jid, chat_message.from_jid)
                            self.client.ban_member_from_group(chat_message.group_jid, chat_message.from_jid)
                            self.client.send_chat_message(chat_message.group_jid, "Removed user with JID '{0}' because the user used an illegal phrase '{1}' in the message.".format(chat_message.from_jid, ban_text))

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