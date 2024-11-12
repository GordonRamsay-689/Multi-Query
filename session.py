import threading
import time
import re
from googleapi import google as google_web
import google.generativeai as genai

# From project folder
from constants import *

class Session:
    def __init__(self, client_name):
        self._stop_event = threading.Event()
        self.name = client_name
        self.type = ENGINE_TO_TYPE[self.name] # CHANGE ENGINE_TO_TYPE to NAME_TO_TYPE or CLIENT_TO_TYPE

        if self.type == TYPE_GEMINI:
            self.client = GeminiClient(self.name)
        elif self.type == TYPE_GOOGLE:
            self.client = GoogleClient()
        else:
            self.client = None

    def get_response(self):
        self.client.query = self.query
        return self.client.get_response()

    def format_response(self):
        self.client.format_response()

class GeminiClient:
    def __init__(self, name):
        self.query = None
        self.response = None
        self.output = ''
        self.model = genai.GenerativeModel(model_name=name)
        self.chat = self.model.start_chat()
    
    def get_response(self):
        self.response = self.chat.send_message(self.query)
        return True if self.response else False
    
    def format_response(self):
        text = self.response.text

        text = self.f_code_blocks(text)
        text = self.f_numbered_lists(text)
        text = self.f_bold_text(text)
        text = self.f_italicized_text(text)
        text = self.f_general(text)

        self.output = text

    def f_code_blocks(response):
        pattern =  r'```(\w+)(.*?)```'
        replacement = r'\t\1: - - - - -\2\t- - - - - - - - - -' # tab, language name, separator, code, tab, separator
        return re.sub(pattern, replacement, response, flags=re.DOTALL)

    def f_numbered_lists(response):
        pattern = r'\*\*(\d)'
        replacement = r'\t\1' 
        return re.sub(pattern, replacement, response)

    def f_bold_text(response):
        # (for some reason, gemini uses double qoutes for bold)
        pattern = r'(?!\*\*\s)\*\*(.+?)(?!\s\*\*)\*\*'
        replacement = r'\033[39;49;1m\1\033[0m' # ANSI: bold, \1, ANSI: reset
        return re.sub(pattern, replacement, response)

    def f_italicized_text(response):
        # (for some reason, gemini uses single qoutes for italic)
        pattern = r'(?!\*\s)\*(.+?)(?!\s\*)\*'
        replacement = r'\033[39;49;3m\1\033[0m' # ANSI: italic, \1, ANSI: reset
        return re.sub(pattern, replacement, response)

    ## REPLACE THIS FUNCTION WITH SMALLER FUNCTIONS
    def f_general(response):
        return response.replace('\t#', '\t\t').replace("* **", '- ').replace("**", '').replace("\n    *", '\n    -').replace("\n*", '\n\t-').replace("--", '')

class GoogleClient:
    def __init__(self):
        self.query = None
        self.results = None
        self.output = ''

    def get_response(self):
        wait = 0.5
        while not self.results:
                if self.stopped():
                    return False
                else:
                    self.results = google_web.search(self.query)
                    time.sleep(wait)

                    wait += 0.5
                    if wait > 3:
                            break

        return True if self.results else False
    
    def format_response(self):
        response = ''
        num_results = len(self.results)

        for i, result in enumerate(self.results):
            end_of_name = result.name.find("https://")
            if not end_of_name:
                end_of_name = result.name.find("http://")

            name = result.name[:end_of_name]

            response += f"{i+1} {name}\n"
            response += f"\t{result.link}\n"
            if result.description:
                response += f"\n\t{result.description}\n"
            else:
                response += f"\n\tNo Description\n"
            
            if i  < (num_results - 1):
                response += '\n\n'

        self.output = response