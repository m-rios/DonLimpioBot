import sys
import telepot
from telepot.loop import MessageLoop
import time
from pprint import pprint
from telepot.delegate import pave_event_space, per_chat_id, create_open


class Session(telepot.helper.ChatHandler):
    start = "You're ready to go now! You can set up a new game using the custom keyboard or just sit back and wait " \
            "for a friend to invite you!"
    off = "Ooh. Sad to see you leave :(. If you ever feel like coming back use /start"
    start_new_game = "Let's setup a new game. To invite players you can share their contact information with me.\n" \
                     "To add rooms or weapons, use the custom keyboard."
    add_weapon = "Tell me the name of the weapon."
    add_room = "Tell me the name of the room."

    def __init__(self, seed_tuple, **kwargs):
        super(Session, self).__init__(seed_tuple, **kwargs)
        self.to_delete = []

    def on__idle(self, event):
        for msg in self.to_delete:
            self.bot.deleteMessage(telepot.message_identifier(msg))
        self.close()

    def on_chat_message(self, msg):
        pprint(msg)
        content_type, chat_type, chat_id = telepot.glance(msg)

        if content_type == 'game':
            self.to_delete.append(msg)


if __name__ == "__main__":

    TOKEN = sys.argv[1]  # get token from command-line

    bot = telepot.DelegatorBot(TOKEN, [
        pave_event_space()(
            per_chat_id(), create_open, Session, timeout=30),
    ])

    MessageLoop(bot).run_as_thread()

    while 1:
        time.sleep(10)
