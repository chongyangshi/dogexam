# Use this script to start the bot after configuring dogexam/config/config.json,
# copying dogexam/data/exambot-original.db to dogexam/data/exambot.db,
# and importing the modules with import_exams.py
# Usage: python run.py dogexam/config/config.json

import sys
import dogexam.bot

if len(sys.argv) < 2:
    print("Usage: python run.py dogexam/config/config.json")
    sys.exit()

dogexam.bot.make_bot(sys.argv[1])
