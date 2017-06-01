# Maintenance script for removing recorded exams and/or user selections.

import db
DB = db.ExamBotDB('data/exambot.db')

if raw_input("Would you like to delete all exams\
 recorded by the system? [y/n]: ").lower() == "y":
    DB.system_clear_modules()
    print("Exams in the system cleared.")
else:
    print("Not clearing exams in the system.")

if raw_input("Would you like to delete all user exam selections?\
 [y/n]: ").lower() == "y":
    DB.system_clear_user_selections()
    print("User exam records cleared.")
else:
    print("Not clearing user exam records.")
