# TODO: 
# - Remove \t from bullet list formatting
# - Shared variables for non-unique regex patterns.
# - Shared variables for non-unique regex replacements.

import re
import time
import threading
import ui
import os
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

REGEX_MD_BOLD = r'(?!\*\*\s)\*\*(.+?\S)(?!\s\*\*)\*\*'
REGEX_MD_BOLD_SUB = r'\033[39;49;1m\1\033[22m' # ANSI: bold, \1, ANSI: reset

REGEX_MD_ITALIC = r'(?!\*\s)\*([^*]+\S)\*(?![a-zA-Z0-9]+)'
REGEX_MD_ITALIC_SUB = r'\033[39;49;3m\1\033[23m' # ANSI: italic, \1, ANSI: reset

REGEX_MD_CODE_BLOCK = r'```(\S+)(.*?)```'
REGEX_MD_CODE_BLOCK_SUB = r'\t\1: - - - - -\2\t- - - - - - - - - -' # tab, language name, separator, code, tab, separator

def format_response(client, response):
    parts = re.split(r'(```\S+.*?```)', response, flags=re.DOTALL)

    result = []

    for part in parts:
        if part.startswith('```'):
            part = client.f_code_blocks(part)
        else:
            part = client.f_numbered_lists(part)
            part = client.f_bold_text(part)
            part = client.f_italicized_text(part)
            part = client.f_header(part)
            part = client.f_bullet(part)
            part = client.f_general(part)
        result.append(part)

    response = ''.join(result)
    return response 

class Session:
    def __init__(self, client_id, sys_message=None):
        self.type = CLIENT_ID_TO_TYPE[client_id] 

        if self.type == TYPE_GEMINI:
            self.client = GeminiClient(client_id, sys_message)
        elif self.type == TYPE_GOOGLE:
            self.client = GoogleClient(client_id, sys_message)
        elif self.type == TYPE_OPENAI or self.type == TYPE_DEEPSEEK:
            self.client = OpenaiClient(client_id, sys_message)
        elif self.type == TYPE_TEST:
            self.client = TestClient(client_id, sys_message)
        else:
            self.client = None
            pass ## Throw error?

    def reset(self):
        self.client.reset()

class OpenaiClient:
    def __init__(self, client_id, sys_message):
        self.api = openai

        if CLIENT_ID_TO_TYPE[client_id] == TYPE_DEEPSEEK:
            self.model = openai.OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.environ["OPENROUTER_API"])   
        else:
            self.model = openai.OpenAI()

        self.stream_enabled = False

        if sys_message:
            self.sys_message = self.create_message("system", sys_message)
        else:
            self.sys_message = None

        self.current_sys_message = None
        self.context = []

        self.name = client_id
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

    def output_stream(self, format):
        full_response = ''

        for chunk in self.api_response:
            chunk_text = chunk.choices[0].delta.content
            
            if not chunk_text:
                continue

            self.format_response(text=chunk_text, format=format)

            full_response += self.response
            ui.c_out(self.response, endline=False)
        ui.c_out('')
        
        message = self.create_message("assistant", full_response)
        self.update_context(message)

    def update_context(self, message):
        if self.sys_message != self.current_sys_message:
            self.context.append(self.sys_message)
            self.current_sys_message = self.sys_message
       
        self.context.append(message)

    def send_request(self):
        self.api_response = self.model.chat.completions.create(
            model=self.name,
            messages=self.context,
            stream=self.stream_enabled
        )

        if self.stream_enabled:
            return True

        return True if self.api_response.choices else False

    def format_response(self, text=None, format=True):
        if text:
            response = text
        else:
            response = self.api_response.choices[0].message.content
            message = self.create_message("assistant", response)
            self.update_context(message)

        if format:
            response = format_response(self, response)

        self.response = response

    def f_code_blocks(self, response):
        pattern =  REGEX_MD_CODE_BLOCK
        replacement = REGEX_MD_CODE_BLOCK_SUB
        return re.sub(pattern, replacement, response, flags=re.DOTALL)

    def f_numbered_lists(self, response):
        return response 

    def f_bold_text(self, response):
        pattern = REGEX_MD_BOLD
        replacement = REGEX_MD_BOLD_SUB
        return re.sub(pattern, replacement, response)

    def f_italicized_text(self, response):
        pattern = REGEX_MD_ITALIC
        replacement = REGEX_MD_ITALIC_SUB
        return re.sub(pattern, replacement, response)

    def f_header(self, response):
        pattern = r'### (.*?)\n'
        replacement = r'\033[39;49;1m-- \1\033[22m\n'
        return re.sub(pattern, replacement, response)
    
    def f_bullet(self, response):
        return response

    def f_general(self, response):
        return response
  
class GeminiClient:
    def __init__(self, client_id, sys_message):
        self.api = google.generativeai

        self.sys_message = sys_message
        self.model = self.api.GenerativeModel(model_name=client_id, 
                                                system_instruction=self.sys_message)
        self.chat = self.model.start_chat()

        self.stream_enabled = False

        self.name = client_id
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

    def output_stream(self, format):
        for chunk in self.api_response:
            self.format_response(text=chunk.text, format=format)
            ui.c_out(self.response, endline=False)
        ui.c_out('')

    def send_request(self):
        self.api_response = self.chat.send_message(self.query, stream=self.stream_enabled)

        if self.stream_enabled: # Shoddy error handling. Without this trying to access self.api_response throws error if stream_enabled
            return True

        return True if self.api_response else False
    
    def format_response(self, text=None, format=True):
        response = text if text else self.api_response.text

        if format:    
            response = format_response(self, response)
        
        self.response = response

    def f_code_blocks(self, response):
        pattern = REGEX_MD_CODE_BLOCK
        replacement = REGEX_MD_CODE_BLOCK_SUB
        return re.sub(pattern, replacement, response, flags=re.DOTALL)

    def f_numbered_lists(self, response):
        pattern = r'\*\*(\d)\s\s\s\s' # New signature for flash 2.0
        replacement = r'\t\1 ' 
        response = re.sub(pattern, replacement, response)

        pattern = r'\*\*(\d)'
        replacement = r'\t\1' 
        response = re.sub(pattern, replacement, response)

        return response 

    def f_bold_text(self, response):
        pattern = REGEX_MD_BOLD
        replacement = REGEX_MD_BOLD_SUB
        return re.sub(pattern, replacement, response)

    def f_italicized_text(self, response):
        pass # write pattern for (rare) underscore enclosed italics

        pattern = REGEX_MD_ITALIC
        replacement = REGEX_MD_ITALIC_SUB
        return re.sub(pattern, replacement, response)

    def f_header(self, response):
        return response.replace('\t#', '\t\t')
    
    def f_bullet(self, response):
        response = response.replace("* **", '- ')

        # Streaming sometimes generates just the bullet and newline.
        pattern = r'^\*\n'
        response = re.sub(pattern, r"\t- ", response, re.MULTILINE)

        response = response.replace("*   ", '- ') # New signature for flash 2.0
        
        # Replace with regex ^\s
        response = response.replace("\n    *", '\n    -')
        response = response.replace("\n   *", '\n   -')
        response = response.replace("\t* ", '\t- ')
        return response.replace("\n*", '\n\t-')

    def f_general(self, response):
        pass # remove "    " quad whitespace from gflash 2.0
        response = response.replace("**", '') # Odd unknown. Used for emphasis sometimes, doesn't seem to
        return response

class GoogleClient:
    def __init__(self, client_id, sys_message):
        self.api = googleapi.google

        self._stop_event = threading.Event()

        self.name = client_id
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
            self.api_response = self.api.search(self.query)

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

    def format_response(self, format=True):
        num_results = len(self.api_response)

        response = ''

        for i, result in enumerate(self.api_response):

            ## Remove link from title of search result
            end_of_name = result.name.find("https://")
            if not end_of_name:
                end_of_name = result.name.find("http://")
            name = result.name[:end_of_name]

            ## Populate response_string
            response += f"\033[1m{i+1}. {name}\033[22m\n"
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
    def __init__(self, client_id, sys_message):
        self.api = None

        self._stop_event = threading.Event()
        
        self.name = client_id
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
        self.api_response = f'Query recieved:\n"{self.query}"\n\nTest response: \n"{TEST_RESPONSE}"'
        return True if self.api_response else False
    
    def format_response(self, text=None, format=True):
        self.response = str(self.api_response) 