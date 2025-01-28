from init_tests import append_to_path
append_to_path()
import unittest
import api_session
from constants import * 

class TestSession(unittest.TestCase):
    def test_session_client_init(self):
        ''' Test if the attribute client.api matches the expected module. '''
        for client_alias, client_id in ALIAS_TO_CLIENT.items():
            with self.subTest(client_id=client_id):
                session = api_session.Session(client_id)
                
                module_str = str(session.client.api)
                
                # Remove source of import.
                # Example: <module 'x' from '/Library/...
                module_str = module_str.split(' from ')[0]

                if session.type == TYPE_TEST:
                    expected_module_str = 'None'
                elif session.type == TYPE_GEMINI:
                    expected_module_str = "<module 'google.generativeai'"
                elif session.type == TYPE_GOOGLE:
                    expected_module_str = "<module 'googleapi.google'"
                elif session.type == TYPE_OPENAI:
                    expected_module_str = "<module 'openai'"

                self.assertEqual(module_str, expected_module_str)

class _OpenaiAPIResponseMessageObject:
    def __init__(self, text):
        self.content = text

class _OpenaiAPIResponseChoiceObject:
    def __init__(self, text):
        self.message = _OpenaiAPIResponseMessageObject(text)
        self.delta = _OpenaiAPIResponseMessageObject(text)

class _OpenaiAPIResponseObject:
    ''' Doubles as a 'chunk' object. '''
    def __init__(self, text=''):
        choice_object = _OpenaiAPIResponseChoiceObject(text)

        self.choices = [choice_object]

        self.chunks = []
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.chunks:
            return self.chunks.pop(0)
        else:
            raise StopIteration
        
    def create_chunks(self, text):
        split_text = text.split('\n')
        
        for part in split_text:
            part += '\n'
            chunk = _OpenaiAPIResponseObject(part)

            self.chunks.append(chunk)

class TestOpenaiClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.session = api_session.Session(GPT_4O_MINI_ID)
        cls.client = cls.session.client 

    @classmethod
    def tearDownClass(cls):
        del cls.session

    def setUp(self):
        self.session.reset()
        self.client.sys_message = DEFAULT_SYS_MSG
        self.client.previous_sys_message = None
        self.client.context = []

    def tearDown(self):
        pass

    def _create_message_and_compare(self, role, text, expected):
        message = self.client.create_message(role, text)
        self.assertIsInstance(message, dict)
        self.assertEqual(message, expected)

    def test_create_message_single_line(self):
        role = "user"
        text = "I am dog."
        expected = {"role": "user", "content": "I am dog."}
        self._create_message_and_compare(role, text, expected)

    def test_update_sys_message_context(self):
        context = self.client.context
        client = self.client

        sys_message = "First System Message"
        message = "First Message"

        client.sys_message = sys_message
        client.update_context(message)
        expected = [sys_message, message]

        self.assertEqual(context, expected)
        self.assertEqual(client.current_sys_message, "First System Message")

        client.sys_message = sys_message
        message = "Second Message"
        client.update_context(message)
        expected.append(message)

        self.assertEqual(context, expected)
        self.assertEqual(client.current_sys_message, "First System Message")

        sys_message = "Second System Message"
        message = "Third Message"

        client.sys_message = sys_message
        client.update_context(message)
        expected.append(sys_message)
        expected.append(message)

        self.assertEqual(context, expected)
        self.assertEqual(client.current_sys_message, "Second System Message")

        sys_message = "Third System Message"
        message = "Fourth Message"

        client.sys_message = sys_message
        client.update_context(message)
        expected.append(sys_message)
        expected.append(message)

        self.assertEqual(context, expected)
        self.assertEqual(client.current_sys_message, "Third System Message")

    def test_update_context(self):
        context = self.client.context
        client = self.client

        messages = ["first", "second", "third", "fourth"]

        expected = [DEFAULT_SYS_MSG]

        for message in messages:
            client.set_query(f"{message} query")
            expected.append({"role": "user", "content": f"{message} query"})
            self.assertEqual(context, expected)

            client.api_response = _OpenaiAPIResponseObject(f"{message} response")
            client.format_response()
            expected.append({"role": "assistant", "content": f"{message} response"})
            self.assertEqual(context, expected)

    def test_update_context_streaming(self):
        context = self.client.context
        client = self.client

        client.api_response = _OpenaiAPIResponseObject()
        
        full_text = "This is line 1\nThis is line 2\nThis is line 3"
        client.api_response.create_chunks(full_text)

        client.output_stream(format=True)

        full_text += '\n'
        expected = [client.create_message("assistant", full_text)]
        self.assertEqual(context, expected)

class TestGeminiFormatResponse(unittest.TestCase):
    ''' Test GeminiClient.format_response(). '''  

    bullet_list = '''
* 1 cup red lentils, rinsed
* 2 cups water or vegetable broth
* 1 tbsp oil
* 1 tsp ground cumin
* 1 tsp ground coriander
* ½ tsp turmeric powder
* ½ tsp garam masala
* ¼ tsp cayenne pepper (optional)
* 1 small onion, chopped
* 2 cloves garlic, minced
* 1 inch ginger, grated
* Salt to taste
* Fresh cilantro, chopped (for garnish)'''
    f_bullet_list = '''
\t- 1 cup red lentils, rinsed
\t- 2 cups water or vegetable broth
\t- 1 tbsp oil
\t- 1 tsp ground cumin
\t- 1 tsp ground coriander
\t- ½ tsp turmeric powder
\t- ½ tsp garam masala
\t- ¼ tsp cayenne pepper (optional)
\t- 1 small onion, chopped
\t- 2 cloves garlic, minced
\t- 1 inch ginger, grated
\t- Salt to taste
\t- Fresh cilantro, chopped (for garnish)'''
    

    indented_bullet_list = '''1. Test CMake Directly:
   * Install CMake independently of Homebrew (e.g., from the CMake website's official macOS distribution).  
   * Create a simple CMake project (e.g., `CMakeLists.txt` containing `cmake_minimum_required(VERSION 3.10) project(MyProject) add_executable(MyProject main.cpp)`, and `main.cpp` containing a basic "Hello, world!" program).
   * Try to build it using the independently installed CMake from the command line. This helps determine if CMake itself is malfunctioning.'''
    f_indented_bullet_list = '''1. Test CMake Directly:
   - Install CMake independently of Homebrew (e.g., from the CMake website's official macOS distribution).  
   - Create a simple CMake project (e.g., `CMakeLists.txt` containing `cmake_minimum_required(VERSION 3.10) project(MyProject) add_executable(MyProject main.cpp)`, and `main.cpp` containing a basic "Hello, world!" program).
   - Try to build it using the independently installed CMake from the command line. This helps determine if CMake itself is malfunctioning.'''

    @classmethod
    def setUpClass(cls):
        cls.session = api_session.Session(GEMINI_FLASH_ID)
        cls.format_response = cls.session.client.format_response

    @classmethod
    def tearDownClass(cls):
        del cls.session

    def func(self, pre):
        ''' The function we are testing. Returns relevant modified variable '''
        self.format_response(text=pre)
        return self.session.client.response

    def compare(self, pre, expected):
        ''' Compares output of function we are testing when 
        passed 'pre' with expected output '''
        return self.assertEqual(self.func(pre), expected)

    def test_format_response_indented_bullet_list(self):
        pre = self.indented_bullet_list
        expected = self.f_indented_bullet_list
    
        self.compare(pre, expected)

    def test_format_response_bullet_item(self):
        pre = '\n* Large pot or Dutch oven'
        expected = '\n\t- Large pot or Dutch oven'

        self.compare(pre, expected)

    def test_format_response_bullet_item_followed_by_boldened_text(self):
        pre = '\n* **Boldened Text** Unboldened text.'
        expected = '\n\t- \033[39;49;1mBoldened Text\033[22m Unboldened text.'

        self.compare(pre, expected)

    def test_format_response_bullet_item_followed_by_boldened_italicized_text(self):
        pre = '\n* ***Boldened Italic.***'
        expected = '\n\t- \033[39;49;1m\033[39;49;3mBoldened Italic.\033[22m\033[23m'

        self.compare(pre, expected)

    def test_format_response_bullet_item_followed_by_boldened_text_and_asterisks(self):
        pre = '\n* * **Boldened NOT Italic.** *'
        expected = '\n\t- * \033[39;49;1mBoldened NOT Italic.\033[22m *'

        self.compare(pre, expected)

    def test_format_response_bullet_item_indented(self):
        pre = '\n    * A'
        expected = '\n    - A'

        self.compare(pre, expected)

    def test_format_response_bullet_item_complex(self):
        pre = '* **A'
        expected = '- A'

        self.compare(pre, expected)

    def test_format_response_bullet_item_followed_by_asterisk(self):
        pre = '\n* Dial *555'
        expected = '\n\t- Dial *555'

        self.compare(pre, expected)
   
    def test_format_response_bullet_list(self):
        ''' Complete multi-line bullet list '''
        pre = self.bullet_list
        expected = self.f_bullet_list

        self.compare(pre, expected)

    def test_format_response_code_blocks(self):
        pre = "```python\nCode\n```\nText\n```C++\nCode\n```\nText"
        expected = "\tpython: - - - - -\nCode\n\t- - - - - - - - - -\nText\n\tC++: - - - - -\nCode\n\t- - - - - - - - - -\nText"

        self.compare(pre, expected)

    def test_format_response_code_block_containing_numbered_list(self):
        pre = "```python\n**1. Item\n```\n **2."
        expected = "\tpython: - - - - -\n**1. Item\n\t- - - - - - - - - -\n \t2."

        self.compare(pre, expected)

    def test_format_response_code_block_containing_boldened_text(self):
        pre = "```python\n**boldened**\n```**boldened**"
        expected = "\tpython: - - - - -\n**boldened**\n\t- - - - - - - - - -\033[39;49;1mboldened\033[22m"

        self.compare(pre, expected)

    def test_format_response_code_block_containing_italicized_text(self):
        pre = "```python\nHey, some *code*\n```"
        expected = "\tpython: - - - - -\nHey, some *code*\n\t- - - - - - - - - -"

        self.compare(pre, expected)

    def test_format_response_bold_text_containing_italic_text(self):
        pre = '*Text **bold** text*'
        expected = '\033[39;49;3mText \033[39;49;1mbold\033[22m text\033[23m'
        
        self.compare(pre, expected)

    def test_format_bold_after_complex_numbered_list_item(self):
        pre = '* ** **Text**'
        expected = '- \033[39;49;1mText\033[22m'

    def test_format_response_top_header(self):
        pre = '\t# This is header'
        expected = '\t\t This is header'

        self.compare(pre, expected)

class TestGeminiFormatHelperFunctions(unittest.TestCase):
    ''' Tests the formatting methods used by GeminiClient.format_response(). '''
    
    texts = {
        'bullet-complex': '* **Text',
        'bullet-streamed': '*\nText',
        'bullet-streamed-multiline': '*\nText\n* Text\n*\n Text',
        'bullet-indented': '\n    * Text',
        'numbered_lists-item': '**1.',
        'numbered_lists-list': '**1. Text\n**2. Text',
        'header-1': '\t# Header 1 #',
        'header-1-not': '\t # Header',
        'bold_text-simple': '**Text**',
        'bold_text-complex': '** * Text * ***',
        'simple_math-mult-A': '5 * 10 = 9',
        'simple_math-mult-B': '5*10 = 9',
        'simple_math-mult-B': '5*10 * 3 = 9',
        'simple_math-mult-C': '5*10*3 = 9',
        'italicized_text-sentence-with-asterisks': 'Hey * this is not * italicized',
        'italicized_text-sentence-with-asterisks-B': 'Hey *this is not * italicized',
        'italicized_text-sentence': 'Hey *this is* italicized',
        'italicized_text-sentence-with-asterisk': 'Hey *this is* also* italicized'
        }
    f_texts = {
        'bullet-complex': '- Text',
        'bullet-streamed': '\t- Text',
        'bullet-streamed-multiline': '\t- Text\n\t- Text\n\t-\n Text',
        'bullet-indented': '\n    - Text',
        'numbered_lists-item': '\t1.',
        'numbered_lists-list': '\t1. Text\n\t2. Text',
        'header-1': '\t\t Header 1 #',
        'header-1-not': '\t # Header',
        'bold_text-simple': '\033[39;49;1mText\033[22m',
        'bold_text-complex': '\033[39;49;1m* Text *\033[22m*',
        'simple_math-mult-A': '5 * 10 = 9',
        'simple_math-mult-B': '5*10 = 9',
        'simple_math-mult-B': '5*10 * 3 = 9',
        'simple_math-mult-C': '5*10*3 = 9',
        'italicized_text-sentence-with-asterisks': 'Hey * this is not * italicized',
        'italicized_text-sentence-with-asterisks-B': 'Hey *this is not * italicized',
        'italicized_text-sentence': 'Hey \033[39;49;3mthis is\033[23m italicized',
        'italicized_text-sentence-with-asterisk': 'Hey \033[39;49;3mthis is\033[23m also* italicized'
        }

    expected_failures = [
        ['f_bullet', 'numbered_lists-list'],
        ['f_bullet', 'bold_text-complex'],
        ['f_bold_text', 'bold_text-complex'], # AOI-1
        ['f_italicized_text', 'simple_math-mult-C'],
        ['f_italicized_text', 'bold_text-complex'],
        ['f_italicized_text', 'bold_text-simple']
        ]

    @classmethod
    def setUpClass(cls):
        cls.session = api_session.Session(GEMINI_FLASH_ID)
        cls.format_response = cls.session.client.format_response

    @classmethod
    def tearDownClass(cls):
        del cls.session

    def run_tests(self, function_name):
        func = getattr(self.session.client, function_name)

        for key in self.texts:
            with self.subTest(key=key):
                expected = self.get_expected(function_name, key)
                pre = self.texts[key]

                post = func(pre)

                pair = [function_name, key]
                
                if pair in self.expected_failures:
                    self.assertNotEqual(post, expected)
                else:
                    self.assertEqual(post, expected)

    def get_expected(self, function_name, current):
        ''' Returns expected output for each function name. '''

        function_name = function_name.strip('f_')

        if current.startswith(function_name):
            return self.f_texts[current]
        else:
            return self.texts[current]

    def test_f_bullet(self):
        function_name = 'f_bullet'

        self.run_tests(function_name)

    def test_f_numbered_lists(self):
        function_name = 'f_numbered_lists'

        self.run_tests(function_name)

    def test_f_header(self):
        function_name = 'f_header'

        self.run_tests(function_name)

    def test_f_bold_text(self):
        function_name = 'f_bold_text'

        self.run_tests(function_name)
    
    def test_f_italicized_text(self):
        function_name = 'f_italicized_text'
        
        self.run_tests(function_name)

if __name__ == '__main__':
    unittest.main(verbosity=2)