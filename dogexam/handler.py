# The command handler for dogexam.

import datetime
import time
from collections import OrderedDict

import dogexam.db as db
import dogexam.utils as utils

class ExamBotCommandHandler:

    def __init__(self, help_text, nickname):

        self._dbm = db.ExamBotDB()
        self._help_text = help_text
        self._module_list = self._dbm.get_exam_list()
        self._module_list_full = self._dbm.get_full_exam_list() # Legacy reasons.
        self.nickname = nickname


    def do_command(self, cmd, source_nick):
        """ The handler for user commands. Return a string to be sent by the
            bot instance through channel notice.
        """

        nick = source_nick

        if cmd == "help":
            # Print help text.
            return self._help_text

        elif cmd == "date":
            # Print the bot's date, used for server timezone check.
            return "Today is " + time.strftime("%Y-%m-%d") + "."

        elif cmd.startswith("add "):
            # Add a list of modules, either separated by comma or space.

            try:
                # Process command.
                cmdsplit = cmd.split(" ", 1)
                module_names = cmdsplit[1].split(",")
                if len(module_names) <= 1:
                    module_names = cmdsplit[1].split()

                # Validate module names.
                all_valid = True
                some_valid = False
                add_set = []
                for module_name in module_names:
                    module_name = "".join(module_name.split())
                    if module_name not in self._module_list:
                        all_valid = False
                    else:
                        some_valid = True
                        add_set.append(module_name)

                # Respond depends on if any of the inputs are valid additions.
                if some_valid == True:
                    self._dbm.add_modules(nick, add_set)
                    if all_valid == False:
                        return self.nickname + ": Although some of your inputs are valid modules with an exam coming up and have been successfully added, some others are either invalid module names or do not have an exam coming up -- these modules have not been added. To check all added exams, use the 'all' command in the public channel. (Private message replies not monitored.)"
                    else:
                        return self.nickname + ": All modules you have specified have been successfully added. (Private message replies not monitored.)"
                else:
                    return self.nickname + ": All of your inputs are not valid modules or without upcoming exams, therefore none added. (Private message replies not monitored.)"

            except IndexError:
                return ""

            return ""

        elif cmd.startswith("delete "):
            # Delete a list of modules, if any is currently selected by the user.

            try:
                # Process command.
                cmdsplit = cmd.split(" ", 1)
                module_names = cmdsplit[1].split(",")
                if len(module_names) <= 1:
                    module_names = cmdsplit[1].split()

                # Validate module names.
                all_valid = True
                some_valid = False
                delete_set = []
                for module_name in module_names:
                    module_name = "".join(module_name.split())
                    if module_name not in self._module_list:
                        all_valid = False
                    else:
                        some_valid = True
                        delete_set.append(module_name)

                # Respond depends on if any valid deletions can be made.
                if some_valid == True:
                    self._dbm.delete_modules(nick, delete_set)
                    return self.nickname + ": If you have set these modules, they are now deleted. (Private message replies not monitored.)"
                else:
                    return self.nickname + ": None of the inputs are valid, therefore none deleted. (Private message replies not monitored.)"

            except IndexError:
                return ""

            return ""

        elif cmd == "all":
            # List all exams the user has selected that will happen in the future.

            modules = self._dbm.get_modules(nick)
            exam_count = 0
            current_date = datetime.datetime.strptime(time.strftime("%Y-%m-%d"), "%Y-%m-%d")

            # Get all future exams for the user.
            responses = OrderedDict({})
            for i in range(0, len(modules)):
                exam_time = datetime.datetime.strptime(modules[i][1], "%Y-%m-%d")
                if exam_time.date() > current_date.date():
                    exam_count += 1
                    if modules[i][0] in responses:
                        responses[modules[i][0]].append(modules[i][1])
                    else:
                        responses[modules[i][0]] = [modules[i][1]]

            # Format the response.
            if exam_count == 0:
                response = "You have no exams set."
            else:
                response = "Your remaining exams: "
                for rsp in responses:
                    response += rsp + " ("
                    for d in range(len(responses[rsp])):
                        response += responses[rsp][d]
                        if (d + 1) < len(responses[rsp]):
                            response += ", "
                    response += "); "
                if response.endswith("; "):
                    response = response[:-2] + "."

            return response

        elif cmd == "next":
            # Get the next exam for the user.

            modules = self._dbm.get_modules(nick)
            current_date = datetime.datetime.strptime(time.strftime("%Y-%m-%d"), "%Y-%m-%d")
            today_exam_checked = False
            today_exam_count = 0;
            response = ""
            response_today = ""
            response_next = ""
            pretext_processed = False
            pretext_time_left = None

            for i in range(0, len(modules)):
                exam_time = datetime.datetime.strptime(modules[i][1], "%Y-%m-%d")

                #Process today's exams.
                if (exam_time.date() == current_date.date()) and (not today_exam_checked):
                    today_exam_checked = True
                    today_exams = [x[0] for x in modules if x[1] == time.strftime("%Y-%m-%d")]
                    today_exam_count = len(today_exams)
                    for i in range(0, len(today_exams)):
                        response_today += str(today_exams[i])
                        if (i < (len(today_exams) - 1)):
                            response_today += ", "
                    response_today += "."

                #Process future exams.
                elif exam_time.date() > current_date.date():
                    time_left = str((exam_time.date() - current_date.date()).days)
                    if pretext_time_left is not None:
                        if time_left != pretext_time_left:
                            break # Already processed a day's worth, no more.
                    if not pretext_processed:
                        if int(time_left) == 1:
                            response_next += "One day "
                        else:
                            response_next += time_left + " days "
                        response_next += "left! On " + datetime.datetime.strftime(datetime.datetime.strptime(modules[i][1], "%Y-%m-%d"), "%d/%m/%Y") + " you have "
                        pretext_processed = True
                        pretext_time_left = time_left
                    response_next += modules[i][2] + " (" + modules[i][0] + "); "

            if response_next.endswith("; "):
                response_next = response_next[:-2] + "."

            # Empty string means no exam in that section.
            if response_today == "":
                if response_next == "":
                    response += "You have no future exams recorded."
                else:
                    response += response_next

            # Formatting plurals and current day's exam(s)
            else:
                if today_exam_count == 1:
                    response += "Exam today: "
                elif today_exam_count > 1:
                    response += "Exams today: "
                if response_next == "":
                    response += response_today
                else:
                    response += response_today + " Coming up: " + response_next

            return response

        elif cmd.startswith("time "):
            # Return the time until that exam. Does not require the user having
            # selected that module.

            try:
                cmdsplit = cmd.split(" ", 1)
                module_in_question = cmdsplit[1]

                # A module may have multiple exams, so we take the nearest one.
                exams = [i for i in self._module_list_full if i[1] == module_in_question]
                if len(exams) > 0:
                    for exam in exams:

                        current_date = datetime.datetime.strptime(time.strftime("%Y-%m-%d"), "%Y-%m-%d")
                        exam_time = datetime.datetime.strptime(exam[0], "%Y-%m-%d")
                        response_next = ""

                        if exam_time.date() >= current_date.date():
                            time_left = str((exam_time.date() - current_date.date()).days)
                            if int(time_left) == 1:
                                response_next += "One day left!"
                            elif int(time_left) == 0:
                                response_next += "It is today!"
                            else:
                                response_next += time_left + " days left!"
                            response_next += " The exam is " + exam[2] + " (" + exam[1] + ") on " + exam[0] + "."

                            return response_next

            except IndexError:
                return ""

            return ""

        elif cmd == "reload":
            # Reload the current exam list, useful for non-interrupting module addition.
            self._module_list = self._dbm.get_exam_list()
            self._module_list_full = self._dbm.get_full_exam_list() # Legacy reasons.
            return ""

        else:
            return ""
