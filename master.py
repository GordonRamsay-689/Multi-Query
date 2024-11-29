import api_session
import google.generativeai
import request_handler
import re
import threading
import os 
import sys
import ui

from constants import * ## Global constants


def setup(config_path):
    with open(config_path, "w") as config:
        config.write("")

    for type in REQUIRES_KEY:
        print(f"Enter API key for {type.capitalize()}")
        print("WARNING! This will be stored localy in plain text.")
        key = input("> ")

        with open(config_path, "a") as config:
            config.write(key)
    
    with open(config_path, "r") as config:
        contents = config.read()
        
    if contents:
        print("Keys saved to config file")
    else:
        print("Failed to save keys to config file")

def get_script_dir():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    except Exception:
        print(ERROR_SCRIPT_DIR)
        sys.exit()

    return script_dir

def get_config_path(script_dir):
    config_path = os.path.join(script_dir, CONFIG_FILENAME)
    return config_path

class Master:
    def __init__(self, config_path):
        self._stop_event = threading.Event()

        cli_lock = threading.Lock()

        self.handler = request_handler.RequestHandler(cli_lock)

        self.config_path = config_path

        self.configured_gemini = False

        self.clients = []
        self.sessions = []
        self.query = ''
        self.persistent_chat = True

    def reset(self):
        self._stop_event.clear()
        self.query = ''

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
    
    def configure(self, aliases=None):
        if not aliases:
            aliases = self.select_clients()
        
        self.populate_clients(aliases)
        self.configure_clients()
        self.populate_sessions()
        self.handler.sessions = self.sessions

    def configure_clients(self):
        with open(self.config_path, "r") as config:
            contents = config.read()

        if contents:
            contents = contents.splitlines()
        else:
            setup()
            return self.configure_clients()

        for client_id in self.clients:
            if CLIENT_ID_TO_TYPE[client_id] == TYPE_GEMINI:
                if not self.configured_gemini:
                    google.generativeai.configure(api_key=contents[0])
                    self.configured_gemini = True
        
    def populate_clients(self, aliases):
        while True:
            for alias in aliases:
                try:
                    client_id = ALIAS_TO_CLIENT[alias]
                except KeyError:
                    continue
                self.clients.append(client_id)
            
            if self.clients:
                return
            else:
                if not self.query:
                    self.query = input("")
            
    def populate_sessions(self):
        for client_id in self.clients:
            session = api_session.Session(client_id)
            self.sessions.append(session)

    def get_query(self):
        with self.cli_lock:
            self.query = ui.c_in()
        
        if self.query:
            self.extract_flags()
    
    def extract_flags(self):
        query = self.query

        pattern_add_client = r"--add:(\S+)"
        matches = re.findall(pattern_add_client, query)
        if matches:
            self.add_models(matches)
        query = re.sub(pattern_add_client, '', query)

        pattern_remove_client = r"--rm:(\S+)"
        matches = re.findall(pattern_remove_client, query)
        if matches:
            self.remove_models(matches)
        query = re.sub(pattern_remove_client, '', query)

        if query:
            self.query = query

    def main(self):
        while True:
            while not self.query:
                with self.cli_lock:
                    ui.c_out("Enter your query (triple click enter to submit):")
                self.get_query()
            


            if self.persistent_chat:
                self.reset()
                continue
            else:
                sys.exit()


def fatal_error(error_message):
    print(f"{SCRIPT_NAME}:")
    print("\tError: ")
    print(f"\t{error_message}")
    sys.exit()

def parse_arguments(args):
    commands = []
    client_aliases = []

    if args[0] not in VALID_COMMANDS and args[0] not in ALIAS_TO_CLIENT.keys():
        query = args.pop(0)
    else:
        query = None

    while args:
        arg = args.pop(0)
        arg = arg.lower()

        if arg.startswith('-'):
            if arg in VALID_COMMANDS:
                commands.append(arg)
            else:
                fatal_error(f"Unknown command: {arg}")
        elif arg.lower() in ALIAS_TO_CLIENT.keys():
            client_aliases.append(arg)
        else:
            fatal_error(f"Unknown command: {arg}")
    
    if not client_aliases:
        print("No client alias provided.")
        print(f"\nDefaulting to {GEMINI_FLASH_ID}.")
        client_aliases.append("gflash")   

    return query, commands, client_aliases

if __name__ == '__main__':
    script_dir = get_script_dir()
    config_path = get_config_path(script_dir)

    master = Master(config_path)

    if len(sys.argv) < 2:
        master.configure()
        master.persistent_chat = True
    else: 
        query, commands, client_aliases = parse_arguments(sys.argv[1:])

        for command in commands:
            if command == "-setup":
                setup(config_path)
                sys.exit()
            elif command == 'help':
                print(CLI_HELP)
                sys.exit()
            elif command == '-c':
                master.persistent_chat = True

        master.configure(client_aliases)
    
    master.main()