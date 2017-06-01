# Maintenance script for removing recorded exams and/or user selections.

import os
import dogexam.db as db

script_path = os.path.dirname(os.path.realpath(__file__))
db_path = os.path.join(script_path, 'data', 'exambot.db')
DB = db.ExamBotDB(db_path)

if input("Would you like to delete all exams\
 recorded by the system? [y/n]: ").lower() == "y":
    DB.system_clear_modules()
    print("Exams in the system cleared.")
else:
    print("Not clearing exams in the system.")

if input("Would you like to delete all user exam selections?\
 [y/n]: ").lower() == "y":
    DB.system_clear_user_selections()
    print("User exam records cleared.")
else:
    print("Not clearing user exam records.")
