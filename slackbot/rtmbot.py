import sys
import os

from rtmbot import RtmBot

# load args with config path
bot = RtmBot(os.environ)
try:
    bot.start()
except KeyboardInterrupt:
    sys.exit(0)
