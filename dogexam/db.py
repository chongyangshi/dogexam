# The SQLite3 DB Manager for dogexam.

import os
import sqlite3

import dogexam.utils as utils

script_path = os.path.dirname(os.path.realpath(__file__))
default_db_path = os.path.join(script_path, 'data', 'exambot.db')

class ExamBotDB:

    def __init__(self, db_file=default_db_path):

        self.__db_file = db_file

        if not utils.check_file_exists(self.__db_file):
            raise NameError("The SQLite3 DB file cannot be found at " + db_file
                + ", not starting.")

        try:
            self.__db_conn = sqlite3.connect(self.__db_file,
             check_same_thread=False)
            self._db_cursor = self.__db_conn.cursor()

        except:
            print("Cannot establish a SQLite3 DB connection, not starting.")
            raise


    # Methods for maintenance use only, not for run-time use.
    def system_import_modules(self, module_list):
        """ Import modules into the database, the format is a list of 3-tuples:
            [(date, module_code, module_name)], where date is a YYYY-MM-DD date
            of each exam, module_code is the short code for an exam (e.g. SYST),
            and module_name is the full name of the exam. Multiple exams of the
            same module must use separate entries. Returns False if invalid
            input, True otherwise.
        """

        for module in module_list:

            if len(module) != 3:
                print("Error: Improperly formed module list.")
                return False

            if not utils.check_date_string(module[0]):
                print("Invalid date: " + module[0])
                return False

        self._db_cursor.executemany("INSERT INTO exams \
         VALUES (?, ?, ?)", module_list)
        self.__db_conn.commit()

        return True


    def system_clear_modules(self):
        """ Remove all modules from the database, useful for starting new exam
            season.
        """

        self._db_cursor.execute("DELETE FROM exams")
        self.__db_conn.commit()

        return True


    def system_clear_user_selections(self):
        """ Remove all user exam selection records from the databse, useful for
            starting new exam season.
        """

        self._db_cursor.execute("DELETE FROM users")
        self.__db_conn.commit()

        return True


    # Methods for run-time use.
    def add_modules(self, nickname, modules):
        """ Attach a list of modules identified by their short codes to a user
            identified by its nickname.
        """

        for module in modules:
            # First check whether the user has already set that module.
            db_cursor.execute("SELECT * FROM users WHERE nick = ? \
             AND module_code = ?", (nickname, module))
            data = db_cursor.fetchone()

            # If not, we add it.
            if data is None:
                self._db_cursor.execute("INSERT INTO users VALUES (?, ?)",
                 (nickname, module))

        self.__db_conn.commit()
        return True


    def delete_modules(self, nickname, modules):
        """ If the user identified by nickname has any module in the list of
            modules, they will be detached.
        """

        for module in modules:
            self._db_cursor.execute("DELETE FROM users WHERE nick = ? \
             AND module_code = ?", (nickname, module))

        self.__db_conn.commit()
        return True


    def get_exam_list(self):
        """ Return the current list of exams.
        """

        exam_list = [i[1].encode("unicode-escape") for i
         in self._db_cursor.execute("SELECT * FROM exams;")]

        return exam_list


    def get_modules(self, nickname):
        """ Return in a list of 3-element-list the upcoming exams for the user
            identified by nicknamem, ordered by date ascending.
        """

        exams = []
        rows = self._db_cursor.execute("SELECT users.module_code, exams.date,\
         exams.module_name FROM users LEFT JOIN exams ON \
         users.module_code = exams.module_code \
         WHERE nick = ? \
         ORDER BY date(exams.date) ASC", (nickname,))

        for row in rows:
            exams.append([row[0], row[1], row[2]])

        return exams
