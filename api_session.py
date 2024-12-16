import re
import time
import threading
import ui

## Optional
try:
    import googleapi.google
except ModuleNotFoundError:
    pass

try:
    import google.generativeai
except ModuleNotFoundError:
    pass

try:
    import openai
except ModuleNotFoundError:
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
        elif self.type == TYPE_OPENAI:
            self.client = OpenaiClient(client_name)
        elif self.type == TYPE_TEST:
            self.client = TestClient(client_name)
        else:
            self.client = None
            pass ## Throw error?

    def reset(self):
        self.client.reset()

class OpenaiClient:
    def __init__(self, name):
        self._api = openai
        self._model = openai.OpenAI()

        self.stream_enabled = False

        self.sys_message = DEFAULT_SYS_MSG
        self.context = []

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

    def create_message(self, role, text):
        return {"role": role, "content": text}

    def set_query(self, query):
        self.query = query
        message = self.create_message("user", query)
        self.update_context(message)

    def output_stream(self):
        full_response = ''

        for chunk in self.api_response:
            self.format_response(chunk.choices[0].delta.content)
            full_response += self.response + '\n'
            ui.c_out(self.response)
        
        message = self.create_message("assistant", full_response)
        self.update_context(message)

    def update_context(self, message):
        if not self.context:
            self.context.append(self.sys_message)
        
        self.context.append(message)

    def send_request(self):
        self.api_response = self._model.chat.completions.create(
            model=self.name,
            messages=self.context,
            stream=self.stream_enabled
        )

        if self.stream_enabled:
            return True

        return True if self.api_response else False

    def format_response(self, text=None):
        if text:
            response = text
        else:
            response = self.api_response.choices[0].message.content
            message = self.create_message("assistant", response)
            self.update_context(message)

        pass # Format response functions

        self.response = response

class GeminiClient:
    def __init__(self, name):
        self._api = google.generativeai
        self._model = self._api.GenerativeModel(model_name=name)
        self._chat = self._model.start_chat()

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

    def set_query(self, query):
        self.query = query

    def output_stream(self):
        for chunk in self.api_response:
            self.format_response(chunk.text)
            ui.c_out(self.response)

    def send_request(self):
        self.api_response = self._chat.send_message(self.query, stream=self.stream_enabled)

        if self.stream_enabled: # Shoddy error handling. Without this trying to access self.api_response throws error if stream_enabled
            return True

        return True if self.api_response else False
    
    def format_response(self, text=None):
        response = text if text else self.api_response.text

        response = self.f_code_blocks(response)
        response = self.f_numbered_lists(response)
        response = self.f_bold_text(response)
        response = self.f_italicized_text(response)
        response = self.f_general(response)

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
        self._api = googleapi.google

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

    def set_query(self, query):
        self.query = query

    def send_request(self):
        wait = 0.5

        while not self.api_response:
            self.api_response = self._api.search(self.query)

            time.sleep(wait)

            wait += 0.5
            if wait > 3 or self.stopped():
                    break

        return True if self.api_response else False
    
    def left_pad(self, text, line_length):
        lines = []

        start = 0
        end = line_length
        length_of_text = len(text)

        if length_of_text < 1:
            return "\tNo Description"

        for n in range(length_of_text // line_length):
            for i in range(end, 0, -1):
                if text[i] in [" ", ".", "-", ","]:
                    end = i
                    break

            if text[start] == " ":
                start += 1

            lines.append(text[start:end])
            start = end
            end *= 2

            if end > length_of_text:
                if text[start] == " ":
                    start += 1

                while start > length_of_text:
                    start -=1

                lines.append(text[start:])

        formatted = ''
  
        num_lines = len(lines)
        for i, l in enumerate(lines):
            formatted += "\t" + l
            if i < num_lines - 1:
                formatted += '\n'

        for c in formatted:
            if c not in [" ", "\n"]:
                return formatted
            
        return "\tNo Description"

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
            response += f"\033[1m{i+1}. {name}\033[0m\n"
            response += f"\n\t{result.link}\n"
            if result.description:
                description = self.left_pad(result.description, 55)
                response += f"\n{description}\n"
            else:
                response += f"\n\tNo Description\n"

            if i < num_results - 1:
                response += '\n\n'
            else:
                response += '\n'

        self.response = response

class TestClient:
    def __init__(self, name="Test-Client"):
        self._api = None

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