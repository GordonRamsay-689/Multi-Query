import api_session
import google.generativeai
import threading
# import time

from constants import * ## Global constants

class RequestHandler:
    def __init__(self, console_lock):
        self.console_lock = console_lock
        self.requests_lock = threading.Lock()

        self.sessions = []
        self.requests = []

    def stop_threads(self): # Not in use yet
        for request in self.requests:
            request.stop()

    def submit_requests(self, query):
        for session in self.sessions:
            session.client.query = query 

            # Create Request() and append to list of active requests
            request = Request(session, self)
            with self.requests_lock:
                self.requests.append(request)

            thread = threading.Thread(target=request.main, daemon=True)
            request.thread = thread            
            request.thread.start()
        
    def join_requests(self): # For use when run with args
        for request in self.requests:
            request.thread.join()
            

class Request:
    def __init__(self, session, parent):
        self._stop_event = threading.Event()
        self.session = session
        self.parent = parent

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def remove_from_requests(self):
        with self.parent.requests_lock:
            try:
                self.parent.requests.remove(self)
            except ValueError:
                pass

    def main(self):
        try:
            successful_request = self.session.client.send_request()
        except Exception as e:
            successful_request = False

        if not successful_request:
            if not self.stopped():
                with self.parent.console_lock:
                    print("failed to receive response")
                    print(self.session.name)
                    pass # send to UI that failed   
        
            self.remove_from_requests()
            return
        
        self.session.client.format_response()

        if not self.stopped():
            with self.parent.console_lock:
                print(self.session.client.response)
                pass # send self.session.client.response to UI
        
        self.remove_from_requests()
        return

def main(query, aliases, config_path):
    # only in use when script run directly

    sessions = []
    clients = []
    for alias in aliases:
        client_id = ALIAS_TO_CLIENT[alias]
        clients.append(client_id)
        
    configure_clients(clients, config_path)

    for client_id in clients:
        session = api_session.Session(client_id)
        sessions.append(session)

    cli_lock = threading.Lock()
    handler = RequestHandler(cli_lock)
    handler.sessions = sessions

    with cli_lock:
        print("\nSending queries...\n")
    
    handler.submit_requests(query)
    handler.join_requests()

def configure_clients(clients, config_path):
    configured_gemini = False

    for client_id in clients:
        if CLIENT_ID_TO_TYPE[client_id] == TYPE_GEMINI:
            if not configured_gemini:
                with open(config_path, "r") as config:
                    contents = config.read()

                contents = contents.splitlines()
                google.generativeai.configure(api_key=contents[0])
                configured_gemini = True

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

if __name__ == '__main__':
    import os, sys

    if len(sys.argv) < 2:
        print(CLI_ERROR_NO_ARGS)
        print(CLI_EXAMPLE_USAGE)
        sys.exit()

    script_dir = get_script_dir()
    config_path = get_config_path(script_dir)
    
    if sys.argv[1] == "-setup":
        setup(config_path)
        sys.exit()
    elif len(sys.argv) < 3:
        print(f"\nDefaulting to {GEMINI_FLASH_ID}")
        main(sys.argv[1], ["gflash"], config_path)
    else:
        main(sys.argv[1], sys.argv[2:], config_path)

    
