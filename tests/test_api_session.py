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
    
    @classmethod
    def setUpClass(cls):
        cls.session = api_session.Session(GEMINI_FLASH_ID)
        cls.format_response = cls.session.client.format_response

    @classmethod
    def tearDownClass(cls):
        del cls.session

    def setUp(self):
        self.session.reset()

    def func(self, pre):
        ''' The function we are testing. Returns relevant modified variable '''
        self.format_response(text=pre)
        return self.session.client.response

    def compare(self, pre, expected):
        ''' Compares output of function we are testing when 
        passed 'pre' with expected output '''
        return self.assertEqual(self.func(pre), expected)

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

    def test_format_response_top_header(self):
        pre = '\t# This is header'
        expected = '\t\t This is header'

        self.compare(pre, expected)

class TestGeminiFormatFunctions(unittest.TestCase):
    ''' Tests the formatting methods used by GeminiClient.format_response(). '''
    
    texts = {
        'bullet-complex': '* **Text',
        'bullet-indented': '\n    * Text',
        'numbered-lists-item': '**1.'
        }
    f_texts = {
        'bullet-complex': '- Text',
        'bullet-indented': '\n    - Text',
        'numbered-lists-item': '\t1.'
        }

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

                self.assertEqual(post, expected)

    def get_expected(self, function_name, current):
        ''' Returns expected output for each function name. '''

        function_name = function_name.strip('f_')
        function_name = function_name.replace('_', '-')

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

    
if __name__ == '__main__':
    unittest.main(verbosity=2)