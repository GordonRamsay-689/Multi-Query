import api_session
import request_handler
import re
import threading
import os 
import sys
import ui

## Optional
try:
    import google.generativeai
    google_generativeai_imported = True
except ModuleNotFoundError:
    google_generativeai_imported = False

try:
    import openai
    openai_imported = True
except ModuleNotFoundError:
    openai_imported = False

## Global constants
from constants import * 

def get_script_dir():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    except Exception:
        fatal_error(ERROR_SCRIPT_DIR)

    return script_dir

class Master:
    def __init__(self):
        self._finished = threading.Event()

        self.cli_lock = threading.Lock()

        self.handler = request_handler.RequestHandler(self.cli_lock, self)

        self.configured_gemini = False
        self.configured_openai = False
        self.configured_deepseek = False

        self.clients = []
        self.sessions = []
        self.query = ''
        self.persistent_chat = False
        self.stream_enabled = False
        self.active_stream = False
        self.format = True

    def reset(self):
        for session in self.sessions:
            session.client.reset()
        self.query = ''

    def configure(self, aliases, sys_message):        
        self.populate_clients(aliases)
        self.configure_clients()
        self.init_sessions(sys_message)
        self.handler.sessions = self.sessions

    def api_key_exists(self, type, client_id):
        if type == TYPE_OPENAI:
            name = "OpenAI"
            key = "OPENAI_API_KEY"
        elif type == TYPE_GEMINI:
            name = "Gemini"
            key = "GEMINI_API"
        elif type == TYPE_DEEPSEEK:
            name = "OpenRouter"
            key = "OPENROUTER_API"

        try:
            os.environ[key]
        except KeyError:
            with self.cli_lock:
                ui.c_out(f"No {name} API key found when trying to acces environment variable '{key}'.\nPlease set an environment variable with 'export {key}=YOUR_KEY' in order to use {name} models.", 
                        color=DRED,
                        isolate=True)
            self.remove_client(client_id)
            
            return False    
        return True

    def is_imported(self, type, client_id):
        if type == TYPE_OPENAI:
            imported = openai_imported
            module = "openai"
        elif type == TYPE_GEMINI:
            imported = google_generativeai_imported
            module = "google.generativeai"
        elif type == TYPE_DEEPSEEK:
            imported = openai_imported
            module = "openai"
        
        if not imported:
            with self.cli_lock:
                ui.c_out(f"Could not locate module '{module}'.", 
                            color=DRED,
                            isolate=True)
            
            self.remove_client(client_id)
            return False
        return True

    def configure_clients(self):
        for client_id in self.clients.copy():
            client_type = CLIENT_ID_TO_TYPE[client_id]

            args = (client_type, client_id)

            if client_type == TYPE_GEMINI:
                if not self.configured_gemini:

                    if not self.is_imported(*args) or not self.api_key_exists(*args):
                        continue
                
                    google.generativeai.configure(api_key=os.environ["GEMINI_API"])
                    self.configured_gemini = True
            elif client_type == TYPE_OPENAI:
                if not self.configured_openai:

                    if not self.is_imported(*args) or not self.api_key_exists(*args):
                        continue

                    self.configured_openai = True
            elif client_type == TYPE_DEEPSEEK:
                if not self.configured_deepseek:
                    
                    if not self.is_imported(*args) or not self.api_key_exists(*args):
                        continue

                    self.configured_deepseek = True
            elif client_type == TYPE_GOOGLE:
                with self.cli_lock:
                    ui.c_out(f"Currently unsupported: ", 
                            color=DRED, 
                            endline='', 
                            top_margin=True)
                    ui.c_out(f"googleapi", 
                             bottom_margin=True)
                    
                self.remove_client(client_id)
                continue
                
    def populate_clients(self, aliases):
        for alias in aliases:
            client_id = ALIAS_TO_CLIENT[alias]

            if client_id not in self.clients:
                self.clients.append(client_id)
            
    def init_sessions(self, sys_message):
        for client_id in self.clients:
            session = api_session.Session(client_id, sys_message=sys_message)

            if self.stream_enabled and session.type in STREAM_SUPPORT:
                if not self.active_stream:
                    session.client.stream_enabled = True
                    self.active_stream = True

            self.sessions.append(session)

    def alias_to_session(self, alias):
        if alias not in ALIAS_TO_CLIENT.keys():
            with self.cli_lock:
                ui.c_out(f"Invalid alias provided: {alias}", 
                         color=DRED,
                         isolate=True)
                
            return False
        
        for session in self.sessions:
            if session.client.name == ALIAS_TO_CLIENT[alias]:
                return session  
        
        return ALIAS_TO_CLIENT[alias]

    def toggle_stream(self, alias):
        session = self.alias_to_session(alias)

        if not session or isinstance(session, str):
            with self.cli_lock:
                ui.c_out(f"No active session matches the alias provided ('{alias}') with flag '{STREAM_FLAG}'.", 
                         color=DRED,
                         isolate=True)
                
            return

        if session.type in STREAM_SUPPORT:
            if self.active_stream and not session.client.stream_enabled: # Disable stream for all other sessions.
                self.stream_enabled = False
                self.active_stream = False

                for s in self.sessions:
                    if s.type in STREAM_SUPPORT and s.client.stream_enabled:
                        s.client.stream_enabled = False
                
                        with self.cli_lock:
                            ui.c_out(f"Stream disabled for {s.client.name}", 
                                     color=LBLUE)

            session.client.stream_enabled = not self.active_stream
            self.stream_enabled = not self.active_stream
            self.active_stream = not self.active_stream

            state = "enabled" if self.active_stream else "disabled"

            with self.cli_lock:
                ui.c_out(f"Stream {state} for {session.client.name}", 
                         color=LBLUE,
                         isolate=True)
        else:
            with self.cli_lock:
                ui.c_out(f"{session.client.name} does not support streamed responses.", 
                         color=DRED,
                         isolate=True)

    def clear(self):
        with self.cli_lock:
            ui.c_out("Reinitializing all sessions...", 
                     color=LBLUE,
                     isolate=True)
            
        clients = self.clients.copy()

        self.remove_all_clients()

        for client_id in clients:
            self.add_client(client_id, None)

    def remove_all_clients(self):
        for client_id in self.clients.copy():
            self.remove_client(client_id)

    def remove_client(self, alias):
        session = self.alias_to_session(alias)

        if not session: # User is informed of invalid alias by self.alias_to_session
            return

        if isinstance(session, str):
            client_id = session
        else:
            if self.active_stream and session.client.name in STREAM_SUPPORT:
                if session.client.stream_enabled:
                    self.active_stream = False
                    self.stream_enabled = False

            self.sessions.remove(session)
            
            client_id = session.client.name

        if client_id in self.clients:
            self.clients.remove(client_id)

            with self.cli_lock:
                ui.c_out(f"Removed {client_id} from active sessions", 
                         color=LBLUE)
        else:
            with self.cli_lock:
                ui.c_out(f"{client_id} not an active session", 
                         color=DRED)

    def add_client(self, alias, sys_message):
        try:
            client_id = ALIAS_TO_CLIENT[alias]
        except KeyError:
            with self.cli_lock:
                ui.c_out(f"Invalid alias provided: {alias}",
                         color=DRED,
                         isolate=True)
            return

        if client_id not in self.clients:
            self.clients.append(client_id)

            with self.cli_lock:
                ui.c_out(f"Adding {client_id} to active sessions..",
                         color=LBLUE)
            
            self.configure_clients() # If unable to configure, informs user and removes client_id from self.clients

            if client_id in self.clients:
                session = api_session.Session(client_id, sys_message=sys_message)
                self.sessions.append(session)

    def extract_flags(self, flags): # split into functions, lots of repetition here
        if not self.query:
            return

        query = self.query

        patterns = {}
        patterns[ADD_FLAG] = rf"{ADD_FLAG}(\S+)"
        patterns[REMOVE_FLAG] = rf"{REMOVE_FLAG}(\S+)"
        patterns[STREAM_FLAG] = rf"{STREAM_FLAG}(\S+)"
        patterns[DISPLAY_FLAG] = DISPLAY_FLAG
        patterns[SYSMSG_FLAG] = rf'{SYSMSG_FLAG}"(.*?)"'
        patterns[CLEAR_FLAG] = CLEAR_FLAG

        for flag in patterns:
            pattern = patterns[flag]
            
            # Display and clear flag handled first as they do not have any options
            if flag == DISPLAY_FLAG:
                if DISPLAY_FLAG in query:
                    flags[DISPLAY_FLAG] = True
            elif flag == CLEAR_FLAG:
                if CLEAR_FLAG in query:
                    flags[CLEAR_FLAG] = True
            else:
                matches = re.findall(pattern, query)

                for match in matches:
                    flags[flag].append(match)

                    if flag == SYSMSG_FLAG:
                        if len(matches) > 1:
                            with self.cli_lock:
                                ui.c_out("You can only provide one system message at a time. \nUsing first message provided.",
                                        color=DRED,
                                        isolate=True)
                        break

            query = re.sub(pattern, '', query)
        
        self.query = query

    def execute_flags(self, flags):
        if flags[CLEAR_FLAG]:
            self.clear()

        if flags[DISPLAY_FLAG]:
            with self.cli_lock:
                display_aliases()

        for match in flags[REMOVE_FLAG]:
            if match == "all":
                self.remove_all_clients()
            else:
                self.remove_client(match)

        sys_message = flags[SYSMSG_FLAG][0] if flags[SYSMSG_FLAG] else None

        if sys_message:
            self.update_system_message(sys_message)

        for match in flags[ADD_FLAG]:
            self.add_client(match, sys_message)

        for match in flags[STREAM_FLAG]:
            self.toggle_stream(match)

    def update_system_message(self, match):
        for session in self.sessions:
            if hasattr(session.client, "previous_sys_message"):
                session.client.sys_message = session.client.create_message("system", match)

    def get_query(self):
        with self.cli_lock:
            ui.c_out("Enter your query (triple click enter to submit):")
            self.query = ui.c_in()

    def init_flags_dict(self):
        flags = {}

        for flag in VALID_FLAGS:
            flags[flag] = []
        
        return flags

    def main(self):
        while True:
            while not self.query:
                flags = self.init_flags_dict()

                with self.cli_lock:
                    ui.c_out(f"Active clients: {self.clients}")
                
                self.get_query()
                self.extract_flags(flags)
                self.execute_flags(flags)

            if self.sessions:
                with self.cli_lock:
                    ui.c_out("Submitting requests...",
                             isolate=True)
            else:
                with self.cli_lock:
                    ui.c_out("No active sessions.",
                             isolate=True)
            
            self.handler.submit_requests(self.query)
            self.handler.monitor_requests()

            if self.persistent_chat:
                self.reset()
            else:
                sys.exit() 

def fatal_error(error_message):
    ui.c_out("Error: ",
             color=DRED,
             endline=False)
    ui.c_out(f"{error_message}",
             indent=1)
    sys.exit()

def select_aliases():
    aliases = []

    while not aliases:
        ui.c_out("Please enter the clients you wish to use:")

        display_aliases()

        user_in = input("> ")
        
        if user_in in sorted(ALIAS_TO_CLIENT.keys()):
            aliases.append(user_in)

    return aliases

def display_aliases():
    l = max([len(key) for key in ALIAS_TO_CLIENT.keys()])

    ui.c_out(f"{"Alias":^{l}}   {"Client":^{l}}",
             top_margin=True,
             indent=1)
    ui.c_out("-"*(3+l*2),
             indent=1)

    for alias in sorted(ALIAS_TO_CLIENT.keys()):
        ui.c_out(f"{alias:{l}}",
                 indent=1,
                 endline=False)
        ui.c_out(" > ",
                 endline=False)
        ui.c_out(ALIAS_TO_CLIENT[alias])
    
    ui.c_out("")

def execute_commands(commands, master):
    for command in commands:
        if command == HELP_COMMAND:
            ui.c_out(CLI_HELP)
            sys.exit()
        elif command == ALIASES_COMMAND:
            display_aliases()
            sys.exit()
        elif command == CHAT_COMMAND:
            master.persistent_chat = True
        elif command == STREAM_COMMAND:
            master.stream_enabled = True
        elif command == NOFORMAT_COMMAND:
            master.format = False

def parse_arguments(args):
    commands = []
    client_aliases = []
    sys_message = None

    # If first argument is not a client or command, assume it is a query.
    if args[0] not in VALID_COMMANDS and args[0] not in ALIAS_TO_CLIENT.keys():
        query = args.pop(0)
    else:
        query = None

    if len(args) != len(set(args)):
        fatal_error("Duplicate arguments provided.")

    while args:
        arg = args.pop(0)
        arg = arg.lower()

        if arg.startswith('-'):
            if arg in VALID_COMMANDS:
                if arg == SYS_COMMAND:
                    try:
                        sys_message = args.pop(0)
                    except IndexError:
                        fatal_error(f"No sys message provided after arg {SYS_COMMAND}.")

                    if sys_message in VALID_COMMANDS or sys_message in ALIAS_TO_CLIENT.keys():
                        fatal_error(f"No sys message provided after arg {SYS_COMMAND}.")
                else:
                    commands.append(arg)
            else:
                fatal_error(f"Unknown command: {arg}")          
        elif arg.lower() in ALIAS_TO_CLIENT.keys():
            client_aliases.append(arg)
        else:
            fatal_error(f"Unknown argument: {arg}")

    return query, commands, client_aliases, sys_message

if __name__ == '__main__':
    script_dir = get_script_dir() # Currently not in use. For logging/chat history

    master = Master()

    if len(sys.argv) < 2:
        client_aliases = select_aliases()
        master.persistent_chat = True
        sys_message = None
    else: 
        query, commands, client_aliases, sys_message = parse_arguments(sys.argv[1:])

        execute_commands(commands, master)

        if not client_aliases:
            ui.c_out("No client alias provided.")
            ui.c_out(f"\nDefaulting to {GEMINI_FLASH_ID}.")
            client_aliases.append("gflash")   

        if not query:
            master.persistent_chat = True

        master.query = query
    
    master.configure(client_aliases, sys_message)
    master.main()
