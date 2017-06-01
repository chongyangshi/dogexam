# Maintenance script.
# Importing module exams from a CSV file into the database.
# For formatting example, see data/example.csv.

import os
import csv
import sys

import dogexam.utils as utils
import dogexam.db as db

script_path = os.path.dirname(os.path.realpath(__file__))
db_path = os.path.join(script_path, 'data', 'exambot.db')
DB = db.ExamBotDB(db_path)

if len(sys.argv) != 2:
    print("Usage: python -m dogexam.import_exams EXAM_LIST.csv")
    sys.exit()

exam_list_file = sys.argv[1]

if not utils.check_file_exists(exam_list_file):
    print("Error: " + exam_list_file + " does not exist.")
    sys.exit()

# Process the modules in the data file.
dataset = []
with open(exam_list_file, 'r') as csvfile:
    content = csv.reader(csvfile, delimiter=',')
    for line in content:
        dataset.append((line[0].strip(), line[1].strip(),
         line[2].strip().replace('"', '')))

# Confirm with the user.
print("The following exams will be imported:")
for row in dataset:
    print(row)
if raw_input("Confirm? [y/n]: ").lower() != "y":
    print("Cancelled.")
    sys.exit()

# Insert the exams.
if DB.system_import_modules(dataset):
    print("Exams have been imported.")
else:
    print("There are issues in the exam list CSV, please see the error messages\
     for more details.")
