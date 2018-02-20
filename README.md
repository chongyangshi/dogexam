dogexam
===================
**dogexam** is an IRC bot to store and provide exam information. It is a good tool against procrastination on IRC if you have an exam to do. It has been running as an independent bot on the freenode #cs-york channel for one year, albeit with a less presentable closed codebase, since it was originally hacked together in a few hours during an exam season.

As I have finally found time to refactor the codebase into a presentable state, this is the open source version of the bot, MIT licensed.

**dogexam** requires Python 3.3+ and the [irc](https://pypi.python.org/pypi/irc) library, as well as SQLite3.

# Setup #
Clone this repository, and copy the following example files:

 - `dogexam/config/config-example.json` to `dogexam/config/config.json`
 -  `dogexam/data/exambot-original.db` to `dogexam/data/exambot.db`

Make sure that `exambot.db` is writable by the Python interpreter.

Install the [irc](https://pypi.python.org/pypi/irc) library:

    pip install irc

You may wish to run it under a virtual environment. Take care *not* to run it on Python 2, as due to changes in text encoding, certain functions may not work under Python 2. Make sure that SQLite is available on your system; the Python binding for which is part of the standard library, so no installation is needed.

Edit the configuration under `dogexam/config/config.json` to provide information such as the bot's nickname and nickserv password, the IRC server, and the channels the bot is to connect to.

An example CSV list of exams can be found in `dogexam/data/example.csv`, format your list of exams according to this file, and import the exams into the database by running:

    python -m dogexam.import_exams PATH/TO/EXAMS.csv

Finally, start the bot:

    python -m dogexam.bot

# Post-season Cleanup #
You should run the following script to clean out the list of exams and user selections after each season, otherwise the wrong exam may come up on user requests in the next exam season:

    python -m dogexam.clear_records
    # and follow the prompts

# Feedback, Issues, and Pull Requests #

Any feedback, issues and pull requests are very welcome, if I can find time to get to them.
