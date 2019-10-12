VERSION = "1.0.0"

def write_database(database):
    database.sort()
    database_file = open("words.txt", "w+")
    for word in database:
        print(word, file=database_file)
    database_file.close()

def load_database():
    database = []
    try:
        database_file = open("words.txt", "r")
        for line in database_file:
            database.append(line.rstrip())
        database_file.close()
        database.sort()
    except:
        open("words.txt", "w+").close()
    return database

def find_by_length(database, length):
    results = []
    for word in database:
        if len(word) == length:
            results.append(word)
    return results

def match_simple(data, query):
    if len(data) != len(query):
        return False
    else:
        match = True
        for i in range(0, len(query)):
            data_char = data[i]
            query_char = query[i]
            if query_char != '_' and query_char != data_char:
                match = False
                break
        return match
            
def find(database, simple_query):
    results = []
    for word in database:
        if match_simple(word, simple_query):
            results.append(word)
    return results

def print_results(results):
    if len(results) == 0:
        print("No matches")
    else:
        biggest = len(max(results, key=len))
        num_results = str(len(results)) + " Result"
        if len(results) > 1:
            num_results = num_results + "s"
        if len(num_results) > biggest:
            biggest = len(num_results)
        print("\n\n" + ('-'*(biggest + 4)))
        print('| ' + num_results + (' ' * (biggest - len(num_results))) + ' |')
        print('-'*(biggest + 4))
        for word in results:
            print("| " + word + (' ' * (biggest - len(word))) + " |")
        print('-'*(biggest + 4) + "\n\n")

def add_word(database, word):
    word = word.lower()
    try:
        database.index(word)
        print("[!] Already in database")
    except:
        database.append(word)
        print("[+] Added " + word)
    database.sort()

def remove_word(database, word):
    word = word.lower()
    try:
        database.remove(word)
        print("[-] " + word + " removed!")
    except:
        print("[!] " + word + " does not exist in database")

class Command:

    def __init__(self):
        self.name = "command"
        self.description = "A default command. You should not see this in the program!"

    def execute(self, args):
        print("This is a default command")

    def help(self, args):
        print("Need some help?")

commands = {}

def register_command(name, command):
    commands[name] = command

def try_register_command(name, command):
    try:
        commands[name] = command
        return True
    except:
        return False

aliases = {}

def register_alias(alias, command):
    aliases[alias] = command

def try_register_alias(name, command):
    try:
        aliases[alias] = command
        return True
    except:
        return False

###################
#                 #
#    COMMANDS     #
#                 #
###################

class HelpCommand(Command):

    def __init__(self):
        self.name = "Help"
        self.description = "Need some help?"

    def execute(self, args):
        if len(args) == 0:
            for command in commands:
                print(commands[command].name + ":")
                print("\t" + commands[command].description)
                if commands[command] in aliases.values():
                    found = []
                    for alias in aliases:
                        if aliases[alias] == commands[command]:
                            found.append(alias)
                    found.sort()
                    print("\tAliases: " + ", ".join(found))
        else:
            try:
                print()
                commands[args].help(args)
                print()
            except:
                print("That command doesn't exist")

    def help(self, args):
        print("This is the help command. Run it to get a list of commands and their descriptions")
        print("You can also run help <command> to get help specific to that command, if it offers it")

class AddCommand(Command):

    def __init__(self):
        self.name = "Add"
        self.description = "Add a word to the database"

    def execute(self, args):
        print("Adding " + arguments + "...")
        add_word(database, arguments)
        write_database(database)

    def help(self, args):
        print("Syntax: add <word>")

class RemoveCommand(Command):

    def __init__(self):
        self.name = "Remove"
        self.description = "Remove an existing word from the database"

    def execute(self, args):
        print("Removing " + arguments + "...")
        remove_word(database, arguments)
        write_database(database)

    def help(self, args):
        print("Syntax: remove <word>")

class LengthCommand(Command):

    def __init__(self):
        self.name = "Length"
        self.description = "Get words by length"

    def execute(self, args):
        try:
            print_results(find_by_length(database, int(arguments)))
        except:
            print("Please enter a number")

    def help(self, args):
        print("Syntax: length <number>")

class SearchCommand(Command):

    def __init__(self):
        self.name = "Search"
        self.description = "Search for words using Draw My Thing format"

    def execute(self, args):
        print_results(find(database, arguments))

    def help(self, args):
        print("Syntax: search <word>")
        print("Search for a word using Draw My Thing format. Type the hint as you see it.")
        print("Do not put spaces between the enderscores. Only put spaces between words.")
        print("Example: if the hint is _ _ _ l e, input _____ (5 underscores, no spaces)")
        print("If the hint is _ a _ _   a _ _   p _ p p _ r, then input _s__ a__ p_pp_r (Note: only two spaces)")

class InfoCommand(Command):

    def __init__(self):
        self.name = "Info"
        self.description = "Get program and database info"

    def execute(self, args):
        print("\n\nDraw My Cheats by AlgoRythm")
        print("Words in database: " + str(len(database)))
        print("Program version: " + VERSION + "\n\n")

    def help(self, args):
        print("Non-interactive, just run the command")

###################
#                 #
#      MAIN       #
#                 #
###################

if __name__ == "__main__":

    print("Loading database...")
    database = load_database()
    print("Done. Found " + str(len(database)) + " words")

    # Register commands
    help_command = HelpCommand()
    register_command("help", help_command)
    register_alias("?", help_command)
    register_command("add", AddCommand())
    remove_command = RemoveCommand()
    register_command("remove", remove_command)
    register_alias("delete", remove_command)
    register_alias("drop", remove_command)
    length_command = LengthCommand()
    register_command("length", length_command)
    register_alias("l", length_command)
    search_command = SearchCommand()
    register_command("search", search_command)
    register_alias("s", search_command)
    register_command("info", InfoCommand())


    command = ""
    while command != "exit":
        # Get next command
        command = input(">> ").lower()
        arguments = ""
        if command.find(" ") != -1:
            arguments = command[command.find(" ") + 1:]
            command = command[:command.find(" ")]

        if command in commands:
            commands[command].execute(arguments)
        elif command in aliases:
            aliases[command].execute(arguments)
        else:
            if command != "exit":
                print("Type \"help\" for help, or \"exit\" to exit")
