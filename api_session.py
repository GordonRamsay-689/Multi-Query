import re
import time
import threading
import ui

## Contidional
try:
    import googleapi.google
except:
    pass

try:
    import google.generativeai
except:
    pass

## Global constants
from constants import * 

class Session:
    def __init__(self, client_name):
        self.type = CLIENT_ID_TO_TYPE[client_name] 

        if self.type == TYPE_GEMINI:
            self.client = GeminiClient(client_name)
        elif self.type == TYPE_GOOGLE:
            self.client = GoogleClient(client_name)
        elif self.type == TYPE_TEST:
            self.client = TestClient(client_name)
        else:
            self.client = None
            pass ## Throw error?

    def reset(self):
        self.client.reset()

class GeminiClient:
    def __init__(self, name):
        self.api = google.generativeai
        self.model = self.api.GenerativeModel(model_name=name)
        self.chat = self.model.start_chat()

        self.stream_enabled = False

        self.name = name
        self.api_response = None
        self.query = ''
        self.response = ''

    def reset(self):
        self.api_response = None
        self.query = ''
        self.response = ''

    def stop(self):
        pass
    
    def stopped(self):
        pass

    def send_request(self):
        self.api_response = self.chat.send_message(self.query, stream=self.stream_enabled)

        return True if self.api_response else False
    
    def format_response(self, text=None):
        response = text if text else self.api_response.text

        response = self.f_code_blocks(response)
        response = self.f_numbered_lists(response)
        response = self.f_bold_text(response)
        response = self.f_italicized_text(response)
        response = self.f_general(response)

        if text:
            return response
        else:
            self.response = response

    def f_code_blocks(self, response):
        pattern =  r'```(\w+)(.*?)```'
        replacement = r'\t\1: - - - - -\2\t- - - - - - - - - -' # tab, language name, separator, code, tab, separator
        return re.sub(pattern, replacement, response, flags=re.DOTALL)

    def f_numbered_lists(self, response):
        pattern = r'\*\*(\d)'
        replacement = r'\t\1' 
        return re.sub(pattern, replacement, response)

    def f_bold_text(self, response):
        pattern = r'(?!\*\*\s)\*\*(.+?)(?!\s\*\*)\*\*'
        replacement = r'\033[39;49;1m\1\033[0m' # ANSI: bold, \1, ANSI: reset
        return re.sub(pattern, replacement, response)

    def f_italicized_text(self, response):
        pattern = r'(?!\*\s)\*(.+?)(?!\s\*)\*'
        replacement = r'\033[39;49;3m\1\033[0m' # ANSI: italic, \1, ANSI: reset
        return re.sub(pattern, replacement, response)

    ## REPLACE THIS FUNCTION WITH SMALLER FUNCTIONS
    def f_general(self, response):
        return response.replace('\t#', '\t\t').replace("* **", '- ').replace("**", '').replace("\n    *", '\n    -').replace("\n*", '\n\t-').replace("--", '')

class GoogleClient:
    def __init__(self, name):
        self.api = googleapi.google

        self._stop_event = threading.Event()

        self.name = name
        self.api_response = None
        self.query = ''
        self.response = ''

    def reset(self):
        self._stop_event.clear()
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
            self.api_response = self.api.search(self.query)

            time.sleep(wait)

            wait += 0.5
            if wait > 3 or self.stopped():
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

class TestClient:
    def __init__(self, name="Test-Client"):
        self.api = None

        self._stop_event = threading.Event()

        self.name = name
        self.api_response = None
        self.query = ''
        self.response = ''

    def reset(self):
        self._stop_event.clear()
        self.api_response = None
        self.query = ''
        self.response = ''
        
    def stop(self):
        self._stop_event.set()

    def stopped(self):
        self._stop_event.is_set()
        
    def send_request(self):
        self.api_response = f"Query recieved: {self.query}\nTest response: {TEST_RESPONSE}"
        return True if self.api_response else False
    
    def format_response(self):
        self.response = str(self.api_response) 