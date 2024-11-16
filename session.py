import time
import re
from googleapi import google as google_web
import google.generativeai as genai

# From project folder
from constants import *

class Session:
    def __init__(self, client_name):
        self.name = client_name
        self.type = CLIENT_ID_TO_TYPE[self.name] 

        if self.type == TYPE_GEMINI:
            self.client = GeminiClient(self.name)
        elif self.type == TYPE_GOOGLE:
            self.client = GoogleClient()
        else:
            self.client = None

    def reset(self):
        self.client.api_response = None
        self.client.query = ''
        self.client.response = ''

class GeminiClient:
    def __init__(self, name):
        self.model = genai.GenerativeModel(model_name=name)
        self.chat = self.model.start_chat()

        self.api_response = None
        self.query = ''
        self.response = ''

    def reset(self):
        self.api_response = None
        self.query = ''
        self.response = ''

    def send_request(self):
        self.api_response = self.chat.send_message(self.query)
        return True if self.api_response else False
    
    def format_response(self):
        response = self.api_response.text

        response = self.f_code_blocks(response)
        response = self.f_numbered_lists(response)
        response = self.f_bold_text(response)
        response = self.f_italicized_text(response)
        response = self.f_general(response)

        self.response = response

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
        self.api_response = None
        self.query = ''
        self.response = ''

    def reset(self):
        self.api_response = None
        self.query = ''
        self.response = ''

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        self._stop_event.is_set()

    def send_request(self):
        wait = 0.5
        while not self.api_response:
                self.api_response = google_web.search(self.query)
                time.sleep(wait)

                wait += 0.5
                if wait > 3:
                        break

        return True if self.api_response else False
    
    def format_response(self):
        num_results = len(self.api_response)

        response = ''

        for i, result in enumerate(self.api_response):

            ## Remove link from title of search result
            end_of_name = result.name.find("https://")
            if not end_of_name:
                end_of_name = result.name.find("http://")
            name = result.name[:end_of_name]

            ## Populate response_string
            response += f"{i+1} {name}\n"
            response += f"\t{result.link}\n"
            if result.description:
                response += f"\n\t{result.description}\n"
            else:
                response += f"\n\tNo Description\n"
            
            ## Add newline to end of response_string
            if i  < (num_results - 1):
                response += '\n\n'

        self.response = response