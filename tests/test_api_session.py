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
    bullet_item_bold = '\n* **Boldened Text** Unboldened text.'
    f_bullet_item_bold = '\n\t- \033[39;49;1mBoldened Text\033[22m Unboldened text.'
    bullet_item_bold_italic = '\n* ***Boldened Italic.***'
    f_bullet_item_bold_italic = '\n\t- \033[39;49;1m\033[39;49;3mBoldened Italic.\033[22m\033[23m'
    bullet_item = '\n* Large pot or Dutch oven'
    bullet_item_with_asterisk = '\n* Dial *555'
    f_bullet_item_with_asterisk = '\n\t- Dial *555'
    all_italic_one_bold = '*Text **bold** text*'
    f_all_italic_one_bold = '\033[39;49;3mText \033[39;49;1mbold\033[22m text\033[23m'
    
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
        self.format_response(text=pre)
        return self.session.client.response
        
    def test_multiple_code_blocks(self):
        pre = "```python\nCode\n```\nText\n```C++\nCode\n```\nText"
        expected = "\tpython: - - - - -\nCode\n\t- - - - - - - - - -\nText\n\tC++: - - - - -\nCode\n\t- - - - - - - - - -\nText"

        self.assertEqual(self.func(pre), expected)

    def test_numbered_list_inside_code_block(self):
        pre = "```python\n**1. Item\n```\n **2."
        expected = "\tpython: - - - - -\n**1. Item\n\t- - - - - - - - - -\n \t2."

        self.assertEqual(self.func(pre), expected)

    def test_boldened_inside_code_block(self):
        pre = "```python\n**boldened**\n```**boldened**"
        expected = "\tpython: - - - - -\n**boldened**\n\t- - - - - - - - - -\033[39;49;1mboldened\033[22m"

        self.assertEqual(self.func(pre), expected)

    def test_code_block_with_italic_inside(self):
        pre = "```python\nHey, some *code*\n```"
        expected = "\tpython: - - - - -\nHey, some *code*\n\t- - - - - - - - - -"

        self.assertEqual(self.func(pre), expected)

    def test_bullet_item_with_asterisk(self):
        pre = self.bullet_item_with_asterisk
        expected = self.f_bullet_item_with_asterisk

        self.assertEqual(self.func(pre), expected)
    
    def test_bullet_list(self):
        pre = self.bullet_list
        expected = self.f_bullet_list

        self.assertEqual(self.func(pre), expected)

    def test_bullet_item_bold(self):
        pre = self.bullet_item_bold
        expected = self.f_bullet_item_bold

        self.assertEqual(self.func(pre), expected)

    def test_bullet_item_bold_italic(self):
        pre = self.bullet_item_bold_italic
        expected = self.f_bullet_item_bold_italic

        self.assertEqual(self.func(pre), expected)

    def test_all_italic_one_bold(self):
        pre = self.all_italic_one_bold
        expected = self.f_all_italic_one_bold
        
        self.assertEqual(self.func(pre), expected)

if __name__ == '__main__':
    unittest.main(verbosity=2)